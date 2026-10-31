"""Validador/humo y cuatro partidas técnicas: APIs oficiales sin limpieza global."""
from __future__ import annotations

import argparse
from dataclasses import asdict
import json
import os
from pathlib import Path
import sys
import time
import uuid

from fase8a_soporte import ROOT, TEAM, sha, save
from fase8b2_control import OUT, IMAGE, require_gate


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('step',choices=['humo','tecnicas'])
    parser.add_argument('--ventana',required=True)
    args=parser.parse_args();require_gate(args.ventana)
    runtime=json.loads((OUT/'RUNTIME_EN_PRUEBA.json').read_text());participant=Path(runtime['participant'])
    frozen=json.loads((OUT/'CONGELADO.json').read_text())
    assert all(sha(participant/name)==info['sha256'] for name,info in runtime['files'].items())
    assert json.loads((OUT/'FRIO_FINAL.json').read_text())['all_passed']
    assert json.loads((OUT/'FUNCIONAL_LINUX.json').read_text())['functional']['passed']==9
    attempt=OUT/('humo_oficial_01' if args.step=='humo' else 'tecnicas_01')
    attempt.mkdir(exist_ok=False)
    host_cache=attempt/'cache_arbitro_host';host_cache.mkdir()
    os.environ['NUMBA_CACHE_DIR']=str(host_cache)
    os.environ.pop('NUMBA_DISABLE_JIT',None)
    for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','NUMBA_NUM_THREADS']:os.environ[key]='1'
    sys.dont_write_bytecode=True;sys.path.insert(0,str(ROOT/'sistema'))
    from config import cargar_limites
    from arbitro.procesos import BotDocker
    from arbitro import partida,registro
    from arbitro.azar import Dados,semilla_bots
    from validador import validar as official
    limits=cargar_limites(ROOT/'sistema/limites.toml')
    helper=TEAM/'herramientas/fase8b2_runner_telemetria.py'
    objects=[]

    class MeasuredBot(BotDocker):
        IMAGEN_COMANDO=('python','/medicion/runner_telemetria.py','/bot')

        def __init__(self,folder,public):
            super().__init__(folder,IMAGE,None,public)
            self.nombre='8b2-i0-'+uuid.uuid4().hex[:12]
            self.telemetry={'name':self.nombre,'folder':str(folder),'image':IMAGE,'prepare_s':None,'cgroup_adios':None,'messages':[]}
            objects.append(self)

        def argumentos(self):
            argv=super().argumentos()
            index=argv.index(self.imagen)
            argv[index:index]=['--label','codex.experimento=8B2-I0-20261029','-v',str(helper)+':/medicion/runner_telemetria.py:ro']
            self.telemetry['docker_command']=argv
            return argv

        def enviar(self,message):
            self.telemetry['messages'].append({'direction':'to_runner','message':message})
            return super().enviar(message)

        def recibir(self,timeout_s):
            message=super().recibir(timeout_s)
            if message is not None:
                self.telemetry['messages'].append({'direction':'from_runner','message':message})
                if message.get('tipo')=='adios':
                    self.telemetry['cgroup_adios']=message.get('cgroup_8B2')
                    self.telemetry['loaded_adios']=message.get('loaded_8B2')
            return message

        def terminar(self):
            if self._proc is not None:
                inspected=self._inspeccionar()
                if inspected:
                    assert inspected['Config']['Labels'].get('codex.experimento')=='8B2-I0-20261029'
                    assert self.nombre.startswith('8b2-i0-')
                    self.telemetry['inspect_before_owned_remove']={key:inspected[key] for key in ['Id','Name','Image','HostConfig','Mounts','State']}
            return super().terminar()

    turn_original=partida._Arbitro._turno
    smoke_factory_original=official._bot
    play_original=official.jugar_partida
    games=[]

    def timed_turn(self,color,message,limit,invalido):
        result=turn_original(self,color,message,limit,invalido)
        if message.get('tipo')=='preparar' and isinstance(self.bots[color],MeasuredBot):
            self.bots[color].telemetry['prepare_s']=result[1]
        return result

    def store_game(result,index,own_color,seed,game,created):
        meta={'blancas':'iacasitegano' if own_color=='blancas' else 'random',
              'negras':'iacasitegano' if own_color=='negras' else 'random','pareja':0,'juego':game,'semilla_maestra':seed}
        raw=registro.a_json(result,meta)
        save(attempt/f'partida_{index:02d}.json',raw)
        telemetry=[obj.telemetry for obj in created]
        save(attempt/f'telemetria_{index:02d}.json',telemetry)
        own=next(obj for obj in created if obj.carpeta==participant)
        cg=own.telemetry['cgroup_adios']
        peak=int(cg['/sys/fs/cgroup/memory.peak']) if cg and '/sys/fs/cgroup/memory.peak' in cg else None
        summary={'index':index,'own_color':own_color,'seed':seed,'game':game,'winner':result.ganador,'reason':result.motivo,
                 'infrastructure_failure':result.falla_infraestructura,'prepare_s':own.telemetry['prepare_s'],
                 'clock_s':result.reloj_usado.get(own_color),'cgroup_peak_bytes':peak,
                 'own_error':result.motivo in ['error','ilegal','preparar','memoria','reloj'] and result.ganador!=own_color,
                 'record_sha256':sha(attempt/f'partida_{index:02d}.json')}
        games.append(summary);save(attempt/'progreso.json',{'completed':len(games),'games':games})
        return summary

    try:
        partida._Arbitro._turno=timed_turn
        if args.step=='humo':
            def factory(folder,image,public,docker):
                assert docker
                return MeasuredBot(Path(folder).resolve(),public)

            def smoke_play(white,black,dice,public,effective,bot_seed,*other,**kwargs):
                index=len(games)+1
                own_color='blancas' if white.carpeta==participant else 'negras'
                result=play_original(white,black,dice,public,effective,bot_seed,*other,**kwargs)
                store_game(result,index,own_color,2026,index-1,[white,black])
                return result

            official._bot=factory;official.jugar_partida=smoke_play
            report=official.validar_equipo(participant,limits,jugar_humo=True,docker=True,oficial=False,entrega=True)
            save(attempt/'VALIDADOR_OFICIAL.json',asdict(report))
            assert report.ok and report.humo_jugado and len(games)==2
            assert not any(row['own_error'] for row in games), 'Error propio/humo: conservar evidencia y bloquear cierre'
        else:
            audit=json.loads((OUT/'AUDITORIA_SEMILLA_20261221.json').read_text())
            assert audit['available_in_audited_scope'] and audit['seed']==20261221
            smoke=json.loads((OUT/'humo_oficial_01/VALIDADOR_OFICIAL.json').read_text())
            assert smoke['ok'] and smoke['humo_jugado']
            # Congelado ANTES de iniciar la primera partida de la tanda.
            plan={'seed':20261221,'seed_audit_sha256':sha(OUT/'AUDITORIA_SEMILLA_20261221.json'),
                  'order':['blancas','negras','blancas','negras'],'games':[0,0,1,1],'pair':0,
                  'participant':runtime,'image':IMAGE,'random_sources':{str(p):sha(p) for p in sorted((ROOT/'estudiantes/random').glob('*')) if p.is_file()},
                  'limits':asdict(limits),'protocol_sha256':sha(OUT/'PROTOCOLO.md'),'telemetry_helper_sha256':sha(helper),
                  'no_expansion_or_strength_selection':True}
            save(attempt/'ANTES_DE_PARTIDAS.json',plan)
            for index,(color,game) in enumerate(zip(plan['order'],plan['games']),1):
                own=MeasuredBot(participant,limits);rival=MeasuredBot(ROOT/'estudiantes/random',limits)
                white,black=(own,rival) if color=='blancas' else (rival,own)
                result=partida.jugar_partida(white,black,Dados(20261221,0,game),limits,limits.efectivos(),semilla_bots(20261221,0,game))
                summary=store_game(result,index,color,20261221,game,[own,rival])
                print(json.dumps(summary),flush=True)
                assert not summary['infrastructure_failure'] and not summary['own_error']
                assert summary['reason'] in ['puntos','sin_jugadas']
                assert summary['prepare_s'] is not None and summary['prepare_s']<10.0
                assert summary['clock_s'] is not None and summary['clock_s']<30.0
                assert summary['cgroup_peak_bytes'] is not None and summary['cgroup_peak_bytes']<1024**3
        summary={'step':args.step,'games':games,'count':len(games),'image':IMAGE,'participant':str(participant),
                 'max_prepare_s':max(g['prepare_s'] or 0 for g in games),'max_clock_s':max(g['clock_s'] or 0 for g in games),
                 'max_cgroup_peak_bytes':max(g['cgroup_peak_bytes'] or 0 for g in games),'no_foreign_cleanup':True,
                 'telemetry_only_outside_clock':True,'technical_not_strength':True}
        save(attempt/'RESUMEN.json',summary)
        print(json.dumps({'step':args.step,'completed':len(games),'max_prepare_s':summary['max_prepare_s'],
                          'max_clock_s':summary['max_clock_s'],'max_cgroup_peak_bytes':summary['max_cgroup_peak_bytes']},indent=2))
    finally:
        partida._Arbitro._turno=turn_original
        official._bot=smoke_factory_original;official.jugar_partida=play_original
        for obj in objects:
            if obj._proc is not None and obj._proc.poll() is None:
                obj.terminar()


if __name__=='__main__':main()
