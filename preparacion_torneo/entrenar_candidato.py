import argparse
import json
import sys
from pathlib import Path

import numpy as np

team = Path('/torneo/estudiantes/iacasitegano')
sys.path[:0] = [str(team), str(team / 'herramientas'), '/torneo/sistema']
import entrenar  # noqa: E402

parser = argparse.ArgumentParser()
parser.add_argument('--partidas', type=int, default=100)
parser.add_argument('--semillas', type=int, nargs='+', required=True)
parser.add_argument('--salida', type=Path, required=True)
args = parser.parse_args()

xs, ys = [], []
for seed in args.semillas:
    x, y = entrenar.generar_datos(args.partidas, seed)
    xs.append(x)
    ys.append(y)
X = np.concatenate(xs)
Y = np.concatenate(ys)
weights = entrenar.ajustar_pesos(X, Y, entrenar.LAMBDA_RIDGE)
args.salida.parent.mkdir(parents=True, exist_ok=True)
np.save(args.salida, weights)
args.salida.with_suffix('.json').write_text(json.dumps({
    'partidas_por_semilla': args.partidas,
    'semillas': args.semillas,
    'posiciones': int(len(Y)),
    'salida': str(args.salida),
    'pesos': weights.tolist(),
}, indent=2), encoding='utf-8')
print(f'Candidato terminado: {args.salida}', flush=True)
