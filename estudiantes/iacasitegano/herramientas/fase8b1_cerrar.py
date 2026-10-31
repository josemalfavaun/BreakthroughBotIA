"""Certifica 8B.1 desde archivos, sin repetir suites ni iniciar cargas posteriores."""
from __future__ import annotations

from collections import Counter
from datetime import datetime
import importlib.metadata
import json
from pathlib import Path
import platform
import re
import subprocess
import sys
import tarfile

from fase8a_soporte import ROOT, TEAM, Budget, sha, save

OUT = ROOT/'resultados/medicion/fase8B1_paquete_20261029'
NOTE = ROOT/'obsidian/Experimentos/2026-10-29-Fase8B1-paquete.md'


def link(label, path):
    return f'[{label}](<{path}>)'


def main():
    budget = Budget()
    before = json.loads((OUT/'antes.json').read_text())
    initial = json.loads((OUT/'manifiesto_inicial.json').read_text())
    fixture = json.loads((OUT/'COMPOSICION_FUNCIONAL.json').read_text())
    static = json.loads((OUT/'ESTATICO_I0.json').read_text())
    risks = json.loads((OUT/'PRUEBAS_CONSTRUCTOR.json').read_text())
    package = OUT/'paquete_I0'
    manifest = json.loads((package/'manifiesto.json').read_text())
    recipe = json.loads((OUT/'receta_I0/receta.json').read_text())
    participant = package/manifest['game_tree']
    checks = {group: {p: sha(Path(p), budget) == expected for p, expected in initial[key].items()}
              for group, key in [('runtime','runtime'),('phase5','phase5_sources'),('active_cache','active_cache'),
                                  ('origins','origins'),('phase8A','phase8A_artifacts'),('patches','patches')]}
    assert all(all(values.values()) for values in checks.values())
    assert {str(p) for p in (TEAM/'data/numba_cache').rglob('*') if p.is_file()} == set(initial['active_cache'])
    assert sha(OUT/'PROTOCOLO.md') == initial['protocol_sha256']
    assert len(checks['phase5']) == 17
    assert all(sha(Path(initial['I0_root'])/name, budget) == expected for name, expected in initial['I0_files'].items())
    assert all(sha(participant/name, budget) == info['sha256'] == initial['I0_files'][name] for name, info in manifest['files'].items())
    assert recipe['constructor_sha256'] == sha(TEAM/'herramientas/fase8b1_paquete.py')
    assert sha(package/'participante.tar', budget) == manifest['archive_sha256']
    assert len(manifest['files']) == 8 and static['files'] == 8 and static['total_bytes'] == 74599
    assert static['official_static_report'] == {'ok':True,'errores':[],'avisos':[],'humo_jugado':False}
    assert static['smoke_guard_calls'] == 0 and not static['official_validation_approval']
    assert fixture['passed'] == 4 and fixture['failures'] == 0 and fixture['globals_and_aliases_restored']
    assert Counter(c['kind'] for c in fixture['cases']) == {'TT_shared_window':2,'safe_win_before_book':2}
    assert risks['risk_checks_passed'] == 6 and risks['failures'] == 0 and risks['tar_bytes_identical']
    assert (package/'participante.tar').read_bytes() == (OUT/'pruebas_constructor/paquete_repetido/participante.tar').read_bytes()
    assert (package/'manifiesto.json').read_bytes() == (OUT/'pruebas_constructor/paquete_repetido/manifiesto.json').read_bytes()
    assert not any(p.is_symlink() for p in OUT.rglob('*'))
    assert all(sha(Path(m['file'])) == m['sha256'] and Path(m['file']).is_relative_to(Path(initial['I0_root']))
               and all(Path(f) == Path(m['file']) for f in m['function_code_files']) for m in fixture['loaded'])
    # Inspección adicional de metadatos de texto dentro del NPZ, sin tocar modelo.
    for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','NUMBA_NUM_THREADS','NUMBA_DISABLE_JIT']:
        import os
        os.environ[name] = '1'
    sys.dont_write_bytecode = True
    import numpy as np
    string_fields = {}
    with np.load(participant/'data/pesos_eval3_ligero.npz', allow_pickle=False) as data:
        for key in data.files:
            array = data[key]
            if array.dtype.kind in ['U','S']:
                strings = [str(x) for x in array.reshape(-1)]
                assert all('/Users/' not in x and '/home/' not in x and 'file://' not in x for x in strings)
                string_fields[key] = strings
    reviewed8b2 = [TEAM/'herramientas/cache_numba_build.py', TEAM/'herramientas/regenerar_cache_numba.sh',
                  TEAM/'herramientas/verificar_preparar_cache.py', ROOT/'sistema/cli/comun.py', ROOT/'sistema/cli/imagenes.py']
    additional_sources = {str(p): sha(p, budget) for p in reviewed8b2}
    head = subprocess.check_output(['rtk','proxy','git','rev-parse','HEAD'], text=True).strip()
    assert head == before['HEAD']
    handoff = ('8B.1 completada: I0 de ensayo compone exactamente TT_A cc888a3c y prioridad de victoria segura 88ce9d47 desde P, '
               'con eval/NPZ/libro de respaldo intactos. Pasan cuatro fixtures mínimos de composición, sin repetir suites. '
               'Constructor nuevo de participante tras descartar empaquetadores de laboratorio; receta, manifiesto y tar reproducibles, '
               'ocho archivos/74.599 bytes sin rutas Mac, cachés ni entrenamiento; informe experimental propio, no informe final. '
               'API estática oficial sin humo: cero errores/avisos; seis riesgos del constructor comprobados, sin JIT/mediciones/partidas. '
               'Principal/caché y17 fuentes congeladas de5 intactos. No selección de modelo, sustitución de U ni cambio de su serie U/V. '
               '8B.2 espera decisión explícita de modelo, adaptación de regresión si cambia escala, Linux/ABI/caché/frío/seguridad y ventana exclusiva; '
               'fase8 abierta. Evidencia: resultados/medicion/fase8B1_paquete_20261029/CIERRE_8B1.md.')
    handoff = handoff.replace('y17','y 17').replace('de5','de 5').replace('fase8 abierta','fase 8 abierta')
    inventory_rows = '\n'.join(f"| {name} | {info['bytes']} | `{info['sha256']}` |" for name, info in manifest['files'].items())
    text = f'''# Cierre del subencargo 8B.1 — composición aislada y paquete

**8B.1 completada en su alcance. I0 es ensayo con respaldo, no finalista ni selección de modelo. Fase 8 permanece abierta.** Ninguna fuente activa fue sustituida. No se recibió en este encargo una decisión explícita posterior de modelo; no se inspeccionaron métricas/test ni se eligió V.

## Composición exacta y preservación

Rama `{before['branch']}`, HEAD `{head}`; snapshots inicial/final en antes.json y MANIFIESTO_FINAL.json. Cambios existentes conservados, sin commit/merge/push/promoción ni notas globales. Fuentes nuevas solo en herramientas/ y artefactos propios aquí. Las 17 fuentes de PROTOCOLO.json de fase5 y los archivos runtime/motor/libro/pesos/caché activos se verificaron antes y después; 30 archivos de caché sin cambios ni altas. Flujo5 y sus datos/pesos/locks no se modificaron o detuvieron; no se consultaron estados/test nuevos. Que el flujo cambie de estado no dispara trabajo desde este encargo.

Raíz I0 real: `{initial['I0_root']}`. Parte de los cinco archivos P congelados en8A, aplica los dos parches originales preservados aquí con patch/fuzz0 sin offsets. Búsqueda `{initial['I0_files']['busqueda_eval3.py']}` idéntica byte a byte a TT_A; estrategia `{initial['I0_files']['strategy.py']}` idéntica a PRIORIDAD_LIBRO. Eval `{initial['I0_files']['eval3.py']}`, NPZ `{initial['I0_files']['data/pesos_eval3_ligero.npz']}` y libro `{initial['I0_files']['data/libro.json']}` intactos respecto a P. No incorpora pistas TT, nuevos finales, utilidad, reloj, pesos o entradas de libro.

{link('Aplicación de parches', OUT/'aplicacion_parches.json')} · {link('Manifiesto inicial y originales', OUT/'manifiesto_inicial.json')}. Los 35 artefactos8A referenciados conservan sus hashes; no se editó ninguna herramienta/evidencia cerrada. I0 no sustituye U (que ya contiene TT corregida y utilidad) ni se inserta en U/V de5. P activo conserva los defectos originales; tener I0 no lo corrige.

## Cuatro comprobaciones mínimas de composición

{link('COMPOSICION_FUNCIONAL.json', OUT/'COMPOSICION_FUNCIONAL.json')}: dos contraejemplos TT/perspectivas tomados del JSON8A, mismo estado a3/e4 frente b7/g6,D2,puntos0–0 y ventanas extremas; consulta estrecha seguida de amplia en tabla compartida devuelve los oráculos certificados ±1.3877787807814457e-17 en lugar de los ±210.20324999290867 de P. Dos decisiones de prioridad de libro, ambos colores, devuelven victoria segura antes del ataque de libro con solo una rama ganadora.

Código realmente cargado desde I0, tres módulos con ruta absoluta/SHA/spec.origin/co_filename; búsqueda y estrategia enlazadas entre sí dentro de I0. Globals y alias/sys.path restaurados. Loader8A reutilizado por parámetros, sin editar evidencia previa. JIT desactivado antes de imports, Python -B/hilos1/nice19 MÁS limitador adaptativo CPU≤12%, D2/tabla256/tope5000 por consulta. No calentar/preparar ni búsqueda cronometrada; oráculo8A reutilizado sin recalcular su suite. Estas cuatro pruebas comprueban composición, no toda seguridad de ejecución.

## Constructor, receta y contenido de juego

Se revisaron fase5_empaquetar.py, fase5_empaquetar_sesion.py y pc/empaquetar.py: paquetes de laboratorio que incluyen entrenamiento/datasets, no adecuados para preparar el participante. comparar_entrega.py compara Git/PR, no construye desde fuentes locales seleccionadas. Se conserva su fuente por referencia/SHA; no se ejecutaron ni editaron. Herramienta nueva mínima {link('fase8b1_paquete.py', TEAM/'herramientas/fase8b1_paquete.py')}, que reutiliza las reglas/API estática oficiales en vez de duplicarlas.

Interfaz explícita de raíz aislada/buscador/NPZ/libro/salida. Etapa congelar fija hashes del constructor/soporte, todas las fuentes seleccionadas, modelo/libro, dependencias y reglas. Construir compara contra receta ANTES de crear salida; rechaza cambios, rutas/enlaces fuera de raíz y salida existente. Selecciona módulos por imports AST, metadatos obligatorios y datos explícitos; la permisibilidad se comprueba con reglas/validador vigentes, no por una lista inventada de extensiones. Entorno, Git, credenciales, motor/sistema, herramientas offline/entrenamiento/resultados y caché Mac no se copian.

Datos de juego: `{participant}` y {link('participante.tar', package/'participante.tar')}. El tar contiene solo estudiantes/iacasitegano; receta/manifiesto/procedencia permanecen FUERA de ese árbol y del tar. Referencias absolutas del host únicamente en procedencia externa. Tar ordenado con uid/gid/mtime0,modo0644, sin links. SHA tar `{manifest['archive_sha256']}`, {manifest['archive_bytes']} bytes. Dos builds en raíces y destinos diferentes producen exactamente el mismo manifiesto/tar/inventario. No se presume reproducibilidad de un caché/imagen Linux no construidos.

INFORME.md activo se conserva por SHA pero no se copia: contiene rutas Mac y describe evidencia histórica. I0 tiene un informe experimental nuevo de nueve secciones, sin esas rutas ni resultados inventados y expresamente sin aprobación deportiva. Metadatos equipo/requirements originales por copia. No se reescribió informe o runtime activo para pasar el validador; informe final del modelo seleccionado sigue pendiente de8B.2.

| Archivo de juego | Bytes | SHA256 |
|---|---:|---|
{inventory_rows}

Total: **8 archivos, 74.599 bytes**. Dependencias declaradas: biblioteca estándar, NumPy/Numba preinstalados y API motor del torneo. Requirements no declara extras instalables. Fuentes/reglas por SHA en receta. NPZ conserva metadatos de texto sin paths de host: {json.dumps(string_fields,ensure_ascii=False)}.

## Pase estático ejecutado, sin aprobación oficial

{link('ESTATICO_I0.json', OUT/'ESTATICO_I0.json')}: API `validar_equipo(participante,limites,jugar_humo=False,docker=False,oficial=False,entrega=True)` devuelve0errores/0avisos, humo=False. Guardia temporal falla ante intento de `_jugar_humo`:0 invocaciones y función restaurada. No se invoca CLI completo, no se construye imagen ni se ejecuta participante/preparar/partida durante esta auditoría.

Comprobaciones oficiales: nombre/equipo e integrantes, nueve secciones del informe, firma/extension de binarios, permisos/links, sintaxis e imports de Python, preparar/jugar definidos, requirements y límites de100MiB total/50MiB archivo/2000 archivos. Adicionales: inventario exacto/SHA y correspondencia de cada miembro del tar, imports locales cerrados, paths Mac ausentes, NPZ275 float64 finito, ocho banderas0/1 y pesos nulos en familias apagadas, claves decimales uint64 y pares/rangos/geometría del libro.

Banderas actuales: patrones=1,marcador=1; amenaza/libres/movilidad/extra/material/exposición=0. Puntos/filas incondicionales como eval3. Libro:8 entradas, esquema correcto; legalidad contextual permanece limitada a la evidencia7A (no se repitió cobertura/replay). Campos del NPZ/modelo no son una decisión de fuerza.

NO cubre instalación real de dependencias, compilación/JIT, humo oficial, ABI/Linux/portabilidad, arranque frío, reloj/preparación, memoria pico, legalidad bajo reloj ni fuerza. El resultado estático ok=True no es aprobación oficial de entrega. Cache opcional ausente: strategy puede compilar; que termine dentro de10s está sin medir. El paquete final podría necesitar un paso explícito de caché Linux y nueva receta/manifiesto en8B.2; este constructor nunca la añade silenciosamente.

## Riesgos del constructor verificados

{link('PRUEBAS_CONSTRUCTOR.json', OUT/'PRUEBAS_CONSTRUCTOR.json')}:6 riesgos,7 invocaciones CLI. Salida existente intacta; ruta externa y enlace de escape rechazados antes de crear salida; fuente modificada y NPZ modificado después de receta rechazados; reproducción byte a byte en otra raíz/destino. Intentos negativos conservados; no hay salida rechazada ni symlink residual. Fixtures originales restaurados, I0/paquete original intactos. No se multiplicaron pruebas que solo reflejen la implementación.

## Pendientes 8B.2 y parada

{link('8B2_PENDIENTE.md', OUT/'8B2_PENDIENTE.md')} contiene reconstrucción con variables obligatorias y sin I0 por defecto, decisión explícita de modelo/fuentes/escala, comandos condicionados de suite extendida/JIT, Linux/ABI/caché, validador completo, frío/seguridad/costo y protocolo previo de comparación. La regresión original compara P/logits: para selección U/V u otra escala/modelo se debe cualificar el adaptador en8B.2, sin sustituir U por A ni alterar los controles originales. No se asignaron/consumieron semillas deportivas, reservas o examen9.

No se lanzó ninguna carga pesada ni se continuará automáticamente. No falta trabajo estático ligero de8B.1. Fase8 permanece abierta hasta decisión real de5/composición final, informe, controles compilados/oficiales y comparación fijada antes de jugar con ventana exclusiva. Los comandos de imágenes/CLI requieren revisar su alcance y evitar limpieza o modificación de servicios ajenos.

## Evidencia, comandos y traspaso

{link('Protocolo previo', OUT/'PROTOCOLO.md')} · {link('Receta portátil', OUT/'receta_I0/receta.json')} · {link('Manifiesto del paquete', package/'manifiesto.json')} · {link('LEEME y comandos ejecutados', OUT/'LEEME.md')}. MANIFIESTO_FINAL.json y SHA256SUMS conservan versiones, fuentes, copias, herramientas, entorno, hashes y estado recuperable. Para repetir un build usar destino nuevo; no sobrescribir ni descartar intentos. Solo nota específica en Obsidian, sin editar Estado/Bitácora/Plan.

## Párrafo de traspaso

{handoff}
'''
    # Ajustes solo de texto puntual, nunca sustituciones globales de nombres de rutas.
    for old, new in {'en8A':'en 8A', 'artefactos8A':'artefactos 8A', 'de5':'de 5', 'JSON8A':'JSON 8A',
                     'g6,D2,puntos0–0':'g6, D2, puntos 0–0', 'oráculo8A':'oráculo 8A', 'Loader8A':'Loader 8A',
                     'uid/gid/mtime0,modo0644':'uid/gid/mtime 0, modo 0644', 'de8B.2':'de 8B.2',
                     'devuelve0errores/0avisos':'devuelve 0 errores/0 avisos', ':0 invocaciones':': 0 invocaciones',
                     'de100MiB':'de 100 MiB', 'total/50MiB':'total/50 MiB', 'banderas0/1':'banderas 0/1',
                     'patrones=1,marcador=1':'patrones=1, marcador=1', 'Libro:8':'Libro: 8', 'evidencia7A':'evidencia 7A',
                     'de10s':'de 10s', 'en8B.2':'en 8B.2', '):6 riesgos':'): 6 riesgos', ':6 riesgos':': 6 riesgos', ',7 invocaciones':', 7 invocaciones',
                     'de8B.1':'de 8B.1', 'Fase8 permanece':'Fase 8 permanece'}.items():
        text = text.replace(old, new)
    (OUT/'CIERRE_8B1.md').write_text(text)
    note = f'''---
tipo: experimento
estado: 8B1-completa-estatica-8B2-pendiente
fecha: 2026-10-29
baseline_commit: {head}
---

# 8B.1 — composición I0 y paquete de ensayo

8B.1 completada en su alcance. I0 combina TT_A cc888a3c y prioridad de victoria segura 88ce9d47 desde P; eval, NPZ y libro de respaldo intactos. No finalista, selección de modelo, sustitución de U o cierre de fase8.

Cuatro fixtures mínimos de composición pasan, con rutas/SHA/co_filename reales y globals restaurados; sin repetir suites8A. Constructor mínimo con receta congelada, entradas explícitas y procedencia fuera del árbol de juego; ocho archivos/74.599bytes, sin caché Mac/rutas de host/entrenamiento. Informe I0 experimental propio; informe activo intacto.

API estática oficial sin humo: cero errores/avisos; NPZ275/banderas/libro/imports/inventario/tamaños correctos. Seis riesgos del constructor pasados, incluido manifiesto/tar reproducibles en otra raíz/destino. No aprobación oficial, JIT, frío, reloj, memoria o fuerza.

{link('Certificado y traspaso', OUT/'CIERRE_8B1.md')} · {link('Paquete experimental', package/'participante.tar')} · {link('Estático', OUT/'ESTATICO_I0.json')} · {link('Comandos condicionados 8B.2', OUT/'8B2_PENDIENTE.md')} · {link('Reproducción', OUT/'LEEME.md')}.

Principal/caché y17 fuentes5 intactos. Pendientes: decisión explícita de5, selección de buscador/escala sin doble parche TT en U, adaptación de regresión si cambia escala, Linux/ABI/caché/frío/seguridad, informe final y protocolo de comparación con ventana exclusiva. U/V de5 mantiene estrategias/libros idénticos. Sin test nuevo, reservas/examen9 o carga pesada; no continuar automáticamente al terminar5. Notas globales intactas.
'''
    for old, new in {'de fase8':'de fase 8','suites8A':'suites 8A','74.599bytes':'74.599 bytes','y17 fuentes5':'y 17 fuentes de 5',
                     'de5':'de 5','terminar5':'terminar 5'}.items():
        note = note.replace(old,new)
    NOTE.write_text(note)
    for file in [OUT/'CIERRE_8B1.md',NOTE]:
        assert all(Path(target).exists() for target in re.findall(r'\]\(<([^>]+)>\)', file.read_text()))
    processes = subprocess.check_output(['rtk','proxy','ps','-axo','pid,ppid,%cpu,command'], text=True)
    tools = [TEAM/'herramientas'/name for name in ['fase8b1_preparar.py','fase8b1_verificar.py','fase8b1_paquete.py',
                                                  'test_fase8b1_constructor.py','fase8b1_cerrar.py']]
    final = {'at':datetime.now().astimezone().isoformat(),'branch':before['branch'],'HEAD':head,
             'status':subprocess.check_output(['rtk','proxy','git','status','--short','--branch'],text=True),
             'checks':checks,'I0_root':initial['I0_root'],'I0_files':initial['I0_files'],'package_manifest_sha256':sha(package/'manifiesto.json'),
             'archive_sha256':manifest['archive_sha256'],'recipe_sha256':sha(OUT/'receta_I0/receta.json'),
             'package_files':8,'game_bytes':74599,'composition_checks':4,'constructor_risks':6,
             'official_static_ok':True,'official_smoke_played':False,'official_approval':False,
             'tools':{str(p):sha(p,budget) for p in tools},'additional_sources_reviewed_for8B2':additional_sources,
             'numpy_text_metadata_host_paths_absent':True,'npz_text_metadata':string_fields,
             'note':str(NOTE),'note_sha256':sha(NOTE),'protocol_sha256':sha(OUT/'PROTOCOLO.md'),
             'handoff':handoff,'decision':'8B1_complete_8B2_pending','phase8_closed':False,'selected_model5':False,
             'active_replacement':False,'JIT':False,'Docker_build':False,'benchmark':False,'official_games':0,
             'new_test_read':False,'new_sport_seeds':[],
             'pending_8B2':['explicit_model_decision','selected_scale_regression_adapter','Linux_ABI_cache','cold_start_cost_safety',
                            'final_report','official_validation_and_prefixed_comparison','exclusive_CPU_window'],
             'environment':{'python':sys.version,'numpy':importlib.metadata.version('numpy'),'numba':importlib.metadata.version('numba'),
                            'architecture':platform.machine(),'functional_mode':'no_JIT,-B,threads1,nice19,adaptive_CPU0.12'},
             'phase5_process_commands_observed':[line for line in processes.splitlines() if any(x in line for x in
                   ['continuar_fase5.py','fase5_generar_robusto.py','entrenar_replay.py'])]}
    save(OUT/'MANIFIESTO_FINAL.json',final)
    save(OUT/'progreso.json',{'status':'8B1_complete_8B2_pending','required_8B1_work_remaining':[],
                            'heavy_work_launched':False,'auto_continue_on_phase5_completion':False,'pending_8B2':final['pending_8B2']})
    files = sorted(p for p in OUT.rglob('*') if p.is_file() and p.name!='SHA256SUMS')
    (OUT/'SHA256SUMS').write_text(''.join(sha(p,budget)+'  '+str(p.relative_to(OUT))+'\n' for p in files))
    budget.wait()
    print(json.dumps({'status':final['decision'],'files_hashed':len(files),'game_files':8,'game_bytes':74599,
                      'static_ok':True,'humo_jugado':False,'phase5_sources_preserved':17,'runtime_preserved':True,
                      'archive_sha256':manifest['archive_sha256']},indent=2))


if __name__ == '__main__':
    main()
