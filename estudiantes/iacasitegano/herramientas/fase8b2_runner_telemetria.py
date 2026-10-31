"""Runner oficial intacto con lectura cgroup SOLO al enviar adios (fuera del reloj).

No altera jugadas, probabilidades, preparación, reloj, límites o archivos del bot.
Se monta fuera del participante. El controlador conserva el campo adicional.
"""
import hashlib
from pathlib import Path
import sys

from arbitro import runner

original=runner.Canal.enviar


def enviar(self,message):
    if message.get('tipo')=='adios':
        fields={p:Path(p).read_text().strip() for p in ['/sys/fs/cgroup/memory.peak','/sys/fs/cgroup/memory.max',
                '/sys/fs/cgroup/cpu.max','/sys/fs/cgroup/memory.events'] if Path(p).is_file()}
        strategy=sys.modules.get('strategy')
        loaded={}
        if strategy is not None:
            loaded={'strategy_file':strategy.__file__,'jugar_code_file':strategy.jugar.__code__.co_filename,
                    'strategy_sha256':hashlib.sha256(Path(strategy.__file__).read_bytes()).hexdigest()}
            search=getattr(strategy,'_busqueda',None)
            if search is not None:
                loaded.update(search_file=search.__file__,search_sha256=hashlib.sha256(Path(search.__file__).read_bytes()).hexdigest())
        message={**message,'cgroup_8B2':fields,'loaded_8B2':loaded}
    return original(self,message)


runner.Canal.enviar=enviar
runner.main(sys.argv)
