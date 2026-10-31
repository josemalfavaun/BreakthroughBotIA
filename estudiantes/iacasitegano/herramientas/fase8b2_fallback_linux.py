"""Forzar aborto real por nodos en elegir y verificar respaldo legal, ambos colores."""
import hashlib
import json
from pathlib import Path
import time

from arbitro import runner

runner.copiar_cache_numba();runner.calentar_motor()
strategy=runner.cargar_estrategia(Path('/bot'))
strategy.preparar(runner.Config('blancas',0,Path('/bot/data'),30.0))
from motor import Estado

search=strategy._busqueda
saved=(search.PROFUNDIDAD_MAXIMA,search.TOPE_PRIMERA_PROFUNDIDAD,dict(search.ULTIMA_BUSQUEDA))
rows=[]
try:
    search.PROFUNDIDAD_MAXIMA=1
    search.TOPE_PRIMERA_PROFUNDIDAD=1
    for color in ['blancas','negras']:
        state=Estado.inicial().a_dict();state['turno']=color;state=Estado.desde_dict(state)
        chosen,value,depth=search.elegir(state,color,time.perf_counter()+1.0)
        diagnostic=dict(search.ULTIMA_BUSQUEDA)
        assert chosen in state.jugadas() and depth==0 and diagnostic['abortos']==1 and diagnostic['parciales']==0
        rows.append({'color':color,'move':[chosen.origen,chosen.destino],'legal':True,'depth_complete':depth,
                     'partial_value_not_used':True,'diagnostic':diagnostic})
finally:
    search.PROFUNDIDAD_MAXIMA,search.TOPE_PRIMERA_PROFUNDIDAD=saved[:2]
    search.ULTIMA_BUSQUEDA.clear();search.ULTIMA_BUSQUEDA.update(saved[2])
print(json.dumps({'passed':2,'rows':rows,'globals_restored':True,'search_file':search.__file__,
                 'search_sha256':hashlib.sha256(Path(search.__file__).read_bytes()).hexdigest()}))
