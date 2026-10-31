"""Contenedores propios para ABI, frío y caché Linux explícita de I0."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tarfile

from fase8a_soporte import ROOT, TEAM, Budget, sha, save
from fase8b2_control import OUT, IMAGE, command, require_gate

PROBE=TEAM/'herramientas/fase8b2_probe_linux.py'


def args_for(name, participant, helper=PROBE, cache_output=None):
    args=['rtk','proxy','docker','run','--rm','--name','8b2-i0-'+name,'--label','codex.experimento=8B2-I0-20261029',
          '--cpus=1','--memory=1024m','--memory-swap=1024m','--pids-limit=64','--network=none','--read-only',
          '--user','65534:65534','--cap-drop=ALL','--security-opt','no-new-privileges',
          '-v',str(participant)+':/bot:ro','-v',str(helper)+':/medicion/helper.py:ro',
          '-v','torneo_numba_arm64:/opt/numba_listo:ro','-e','NUMBA_CACHE_DIR=/tmp/numba','-e','NUMBA_DISABLE_JIT=0',
          '-e','OMP_NUM_THREADS=1','-e','OPENBLAS_NUM_THREADS=1','-e','NUMBA_NUM_THREADS=1','-e','PYTHONDONTWRITEBYTECODE=1']
    if cache_output:
        args+=['-v',str(cache_output)+':/tmp/numba:rw']
    else:
        args+=['--tmpfs','/tmp/numba:size=64m,noexec,mode=1777']
    return args+['--entrypoint','python',IMAGE,'-B','/medicion/helper.py']


def probe(name,participant,mode):
    destination=OUT/'linux'/name
    result=command(args_for(name,participant)+['--mode',mode],destination,timeout=120)
    if result:raise RuntimeError('Probe falló; conservar salida y detener rama')
    payload=json.loads((destination/'stdout.log').read_text().strip().splitlines()[-1])
    save(destination/'probe.json',payload)
    frozen=json.loads((OUT/'CONGELADO.json').read_text())
    expected=frozen['decision_files']
    assert all(payload['identity']['files'][name]==expected[name]['sha256'] for name in payload['identity']['files'])
    assert payload['identity']['motor_sha256']==frozen['runtime'][str(ROOT/'sistema/motor/nucleo.py')]
    assert payload['identity']['platform']=='linux' and payload['identity']['architecture']=='aarch64'
    return payload


def runtime_record(participant,label):
    budget=Budget()
    frozen=json.loads((OUT/'CONGELADO.json').read_text())
    for name,info in frozen['decision_files'].items():assert sha(participant/name,budget)==info['sha256']
    files={str(p.relative_to(participant)):{'sha256':sha(p,budget),'bytes':p.stat().st_size,'mtime_ns':p.stat().st_mtime_ns}
           for p in sorted(participant.rglob('*')) if p.is_file()}
    assert not any(p.is_symlink() for p in participant.rglob('*'))
    manifest={'label':label,'participant':str(participant),'files':files,'base8_files_unchanged':True,
              'image':IMAGE,'model_changed':False,'cache_included':(participant/'data/numba_cache').is_dir(),
              'size_bytes':sum(info['bytes'] for info in files.values()),'timestamp_policy':'preserve_sources_and_cache_for_numba_index_stamp'}
    save(OUT/'RUNTIME_EN_PRUEBA.json',manifest)
    return manifest


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('step',choices=['abi','sin_cache','cache','frio_final','funcional','aborto'])
    parser.add_argument('--ventana',required=True)
    args=parser.parse_args();require_gate(args.ventana)
    frozen=json.loads((OUT/'CONGELADO.json').read_text());stage=Path(frozen['stage'])
    info=json.loads(subprocess.check_output(['rtk','proxy','docker','image','inspect',IMAGE],text=True))[0]
    assert info['Id']==IMAGE and info['Os']=='linux' and info['Architecture']=='arm64'
    subprocess.run(['rtk','proxy','docker','volume','inspect','torneo_numba_arm64'],check=True,capture_output=True)
    if args.step=='abi':
        data=probe('abi_01',stage,'abi');print(json.dumps(data,indent=2));return
    if args.step=='sin_cache':
        data=probe('frio_sin_cache_01',stage,'cold')
        if data['ok']:runtime_record(stage,'I0_sin_cache')
        progress=json.loads((OUT/'progreso.json').read_text());progress['cold_without_cache']='passed' if data['ok'] else 'failed_preserved_needs_Linux_cache';save(OUT/'progreso.json',progress)
        print(json.dumps({'no_cache_ok':data['ok'],'total_prepare_s':data['total_prepare_s'],'error':data['error']},indent=2));return
    if args.step=='cache':
        previous=json.loads((OUT/'linux/frio_sin_cache_01/probe.json').read_text())
        if previous['ok']:raise RuntimeError('Caché no justificada por fallo de paquete sin caché')
        target=OUT/'linux/paquete_cache_01/estudiantes/iacasitegano'
        shutil.copytree(stage,target,copy_function=shutil.copy2)
        cache=OUT/'linux/cache_generada_01';cache.mkdir(exist_ok=False);cache.chmod(0o777)
        helper=TEAM/'herramientas/cache_numba_build.py'
        exitcode=command(args_for('cache-build-01',target,helper,cache),OUT/'linux/construccion_cache_01',timeout=300)
        if exitcode:raise RuntimeError('Fallo al construir caché; detener rama')
        cm=json.loads((cache/'manifest.json').read_text());abi=json.loads((OUT/'linux/abi_01/probe.json').read_text())['identity']
        assert cm['arquitectura']==abi['architecture'] and cm['numba']==abi['numba'] and cm['numpy']==abi['numpy']
        assert all(cm['fuentes_sha256'][name]==frozen['decision_files'][name]['sha256'] for name in ['strategy.py','eval3.py','busqueda_eval3.py'])
        assert cm['fuentes_sha256']['motor/nucleo.py']==abi['motor_sha256']
        shutil.copytree(cache,target/'data/numba_cache',copy_function=shutil.copy2)
        # Archivo nuevo explícito; preservar stamps de fuentes requeridos por índice Numba.
        archive=OUT/'linux/I0_cache_Linux_01.tar'
        with tarfile.open(archive,'x',format=tarfile.PAX_FORMAT) as tar:
            for path in sorted(target.rglob('*')):
                if path.is_file():
                    item=tar.gettarinfo(str(path),arcname='estudiantes/iacasitegano/'+str(path.relative_to(target)))
                    item.uid=item.gid=0;item.uname=item.gname='';item.mode=0o644
                    with path.open('rb') as stream:tar.addfile(item,stream)
        extracted=OUT/'linux/extraido_cache_01';extracted.mkdir(exist_ok=False)
        with tarfile.open(archive) as tar:
            assert all(i.isfile() and not Path(i.name).is_absolute() and '..' not in Path(i.name).parts for i in tar)
            tar.extractall(extracted,filter='data')
        extracted=extracted/'estudiantes/iacasitegano'
        for path in target.rglob('*'):
            if path.is_file():assert sha(path)==sha(extracted/path.relative_to(target))
        manifest=runtime_record(extracted,'I0_cache_Linux_extraido')
        manifest.update(archive=str(archive),archive_sha256=sha(archive),cache_manifest=cm,helper_sha256=sha(helper),
                        only_added_files=[name for name in manifest['files'] if name not in frozen['decision_files']])
        save(OUT/'linux/RECETA_CACHE_EXPLICITA.json',manifest)
        print(json.dumps({'cache_files':len(manifest['only_added_files']),'archive_sha256':manifest['archive_sha256'],'base8_unchanged':True},indent=2));return
    selected=json.loads((OUT/'RUNTIME_EN_PRUEBA.json').read_text());participant=Path(selected['participant'])
    if args.step=='aborto':
        destination=OUT/'linux/fallback_aborto_01'
        helper=TEAM/'herramientas/fase8b2_fallback_linux.py'
        exitcode=command(args_for('fallback-aborto-01',participant,helper),destination,timeout=120)
        if exitcode:raise RuntimeError('Fallo de respaldo con aborto real')
        data=json.loads((destination/'stdout.log').read_text().strip().splitlines()[-1])
        assert data['passed']==2 and data['search_sha256']==frozen['decision_files']['busqueda_eval3.py']['sha256']
        save(OUT/'FALLBACK_ABORTO_LINUX.json',data)
        print(json.dumps({'fallbacks_passed':2},indent=2));return
    if args.step=='frio_final':
        rows=[]
        for index in range(1,4):
            data=probe('frio_final_'+str(index).zfill(2),participant,'cold');rows.append(data)
            if not data['ok']:raise RuntimeError('Fallo frío final: no ampliar ni fingir aprobación')
            peak=int(data['cgroup']['/sys/fs/cgroup/memory.peak'])
            assert peak<1024*1024*1024 and data['cgroup']['/sys/fs/cgroup/memory.max']=='1073741824'
            quota,period=map(int,data['cgroup']['/sys/fs/cgroup/cpu.max'].split());assert quota==period
        save(OUT/'FRIO_FINAL.json',{'trials':3,'all_passed':True,'max_prepare_s':max(d['total_prepare_s'] for d in rows),
             'max_cgroup_peak_bytes':max(int(d['cgroup']['/sys/fs/cgroup/memory.peak']) for d in rows),
             'new_containers_each_trial':True,'participant':str(participant),'data':rows})
        print(json.dumps({'cold_passed':3,'max_prepare_s':max(d['total_prepare_s'] for d in rows)},indent=2));return
    data=probe('funcional_Linux_01',participant,'functional')
    assert data['ok'] and data['functional']['passed']==9
    save(OUT/'FUNCIONAL_LINUX.json',data)
    print(json.dumps({'functional_passed':data['functional']['passed'],'gain':data['loaded']['gain']},indent=2))


if __name__=='__main__':main()
