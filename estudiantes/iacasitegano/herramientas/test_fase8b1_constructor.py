"""Seis riesgos reales del constructor; sin repetir lógica interna ni jugar partidas."""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys

from fase8a_soporte import ROOT, Budget, sha, save
from fase8b1_paquete import setup

OUT = ROOT/'resultados/medicion/fase8B1_paquete_20261029'


def inventory(folder):
    return {str(p.relative_to(folder)): sha(p) for p in sorted(folder.rglob('*')) if p.is_file()}


def main():
    setup()
    import numpy as np
    budget = Budget()
    trials = OUT/'pruebas_constructor'
    trials.mkdir(exist_ok=False)
    original = OUT/'I0/estudiantes/iacasitegano'
    untouched = inventory(original)
    package = OUT/'paquete_I0'
    original_package = inventory(package)
    root = trials/'fuente/iacasitegano'
    shutil.copytree(original, root)
    tool = Path(__file__).with_name('fase8b1_paquete.py')
    results = []

    def run(command, expected_success, reason):
        result = subprocess.run(['rtk','proxy',sys.executable,'-B',str(tool),*command], capture_output=True, text=True)
        assert (result.returncode == 0) == expected_success, result.stderr
        row = {'case': reason, 'command': result.args, 'exit': result.returncode,
               'stdout': result.stdout, 'stderr': result.stderr, 'expected_success': expected_success}
        results.append(row)
        save(trials/'intentos.json', results)
        budget.wait()
        return result

    def arguments(command, source, output, recipe=None):
        cmd = [command,'--raiz-participante',str(source),'--buscador','busqueda_eval3.py',
               '--pesos','data/pesos_eval3_ligero.npz','--libro','data/libro.json','--salida',str(output)]
        if recipe:
            cmd += ['--receta', str(recipe)]
        return cmd

    original_recipe = OUT/'receta_I0/receta.json'
    rejection = run(arguments('construir', original, package, original_recipe), False, 'salida_existente')
    assert 'Salida existente' in rejection.stderr and inventory(package) == original_package

    outside = trials/'fuera/busqueda_eval3.py'
    outside.parent.mkdir()
    outside.write_text('# Fixture externo inerte; no se ejecuta\n')
    cmd = arguments('congelar', root, trials/'rechazo_fuera')
    cmd[cmd.index('--buscador')+1] = str(outside)
    rejection = run(cmd, False, 'ruta_fuera_de_raiz')
    assert 'fuera de la raíz' in rejection.stderr and not (trials/'rechazo_fuera').exists()

    source = root/'busqueda_eval3.py'
    original_source = source.read_bytes()
    source.unlink()
    source.symlink_to(outside)
    try:
        rejection = run(arguments('congelar', root, trials/'rechazo_enlace'), False, 'enlace_escape_fuera_de_raiz')
        assert 'enlace simbólico' in rejection.stderr and not (trials/'rechazo_enlace').exists()
    finally:
        source.unlink()
        source.write_bytes(original_source)
    assert not source.is_symlink()

    run(arguments('congelar', root, trials/'receta_fixture'), True, 'precondicion_receta_fixture')
    fixture_recipe = trials/'receta_fixture/receta.json'
    source.write_bytes(original_source + b'\n# Alteracion de fixture despues de congelar\n')
    try:
        rejection = run(arguments('construir', root, trials/'rechazo_fuente', fixture_recipe), False, 'fuente_modificada_tras_receta')
        assert 'Receta rechazada' in rejection.stderr and not (trials/'rechazo_fuente').exists()
    finally:
        source.write_bytes(original_source)

    weights = root/'data/pesos_eval3_ligero.npz'
    original_weights = weights.read_bytes()
    with np.load(weights, allow_pickle=False) as data:
        changed = data['pesos'].copy()
    changed[0] += 1e-8
    np.savez(weights, pesos=changed)
    try:
        rejection = run(arguments('construir', root, trials/'rechazo_modelo', fixture_recipe), False, 'modelo_modificado_tras_receta')
        assert 'Receta rechazada' in rejection.stderr and not (trials/'rechazo_modelo').exists()
    finally:
        weights.write_bytes(original_weights)
    assert inventory(root) == untouched

    repeated = trials/'paquete_repetido'
    run(arguments('construir', root, repeated, fixture_recipe), True, 'reproduccion_otro_destino_y_raiz')
    assert (package/'manifiesto.json').read_bytes() == (repeated/'manifiesto.json').read_bytes()
    assert (package/'participante.tar').read_bytes() == (repeated/'participante.tar').read_bytes()
    assert inventory(package/'estudiantes/iacasitegano') == inventory(repeated/'estudiantes/iacasitegano')
    assert inventory(original) == untouched and inventory(package) == original_package
    assert not any(p.is_symlink() for p in trials.rglob('*'))
    save(OUT/'PRUEBAS_CONSTRUCTOR.json', {'risk_checks_passed': 6, 'failures': 0, 'cli_invocations': len(results),
             'cases': results, 'all_negative_outputs_absent': True, 'I0_and_original_package_preserved': True,
             'portable_manifest_bytes_identical': True, 'tar_bytes_identical': True, 'game_inventory_identical': True,
             'fixture_sources_restored': True, 'fixture_escape_symlink_removed': True,
             'no_performance_or_strength_claim': True})
    budget.wait()
    print(json.dumps({'risks_passed': 6, 'failures': 0, 'cli_invocations': len(results)}, indent=2))


if __name__ == '__main__':
    main()
