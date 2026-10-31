import argparse
import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path

import numpy as np

team = Path('/torneo/estudiantes/iacasitegano')
sys.path[:0] = [str(team), str(team / 'herramientas'), '/torneo/sistema']
import eval as ev  # noqa: E402
import liga_interna as league  # noqa: E402

parser = argparse.ArgumentParser()
parser.add_argument('--pesos', type=Path, required=True)
parser.add_argument('--salida', type=Path, required=True)
parser.add_argument('--partidas', type=int, default=40)
parser.add_argument('--semilla', type=int, required=True)
args = parser.parse_args()

ev.cargar_pesos(np.load(args.pesos))
weights = np.ascontiguousarray(ev.PESOS, dtype=np.float64)
gain = ev.cota() + 100.0

def candidate(_color, _seed):
    return league._jugador_con_pesos(weights, 4, gain)

results = {}
for rival_name in ('montecarlo', 'minimax2'):
    rival_module = league._cargar_strategy(rival_name)

    def rival(color, seed, module=rival_module):
        return league._jugador_rival(module, color, seed)

    output = io.StringIO()
    with redirect_stdout(output):
        league.jugar_liga('candidato', candidate, rival_name, rival,
                           args.partidas, args.semilla)
    line = output.getvalue().strip()
    print(line, flush=True)
    results[rival_name] = line

args.salida.parent.mkdir(parents=True, exist_ok=True)
args.salida.write_text(json.dumps(results, indent=2), encoding='utf-8')
