"""Constructor mínimo de participante: receta congelada y pase estático sin humo.

No construye Docker, compila JIT, importa al participante ni elige un modelo.
La procedencia absoluta queda fuera de estudiantes/<equipo> y del tar de juego.
"""
from __future__ import annotations

import argparse
import ast
from dataclasses import asdict
import hashlib
import io
import json
import operator
import os
from pathlib import Path
import stat
import sys
import tarfile
import tomllib

from fase8a_soporte import ROOT, TEAM, Budget, sha, save

FORMAT = 1


def setup():
    sys.dont_write_bytecode = True
    for name in ['NUMBA_DISABLE_JIT', 'NUMBA_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS']:
        os.environ[name] = '1'
    sys.path.insert(0, str(ROOT / 'sistema'))


def checked_root(path):
    path = Path(path).absolute()
    if '..' in path.parts or any(p.is_symlink() for p in [path, *path.parents]):
        raise ValueError('Raíz con enlace o recorrido padre')
    if not path.is_dir() or path.resolve() == TEAM.resolve():
        raise ValueError('Se requiere raíz aislada existente; no participante activo')
    return path.resolve()


def input_path(root, path):
    path = Path(path)
    if '..' in path.parts:
        raise ValueError('Recorrido padre no permitido')
    path = path if path.is_absolute() else root / path
    try:
        relative = path.relative_to(root)
    except ValueError:
        raise ValueError('Entrada fuera de la raíz explícita') from None
    if any((root / Path(*relative.parts[:i])).is_symlink() for i in range(1, len(relative.parts) + 1)):
        raise ValueError('Entrada por enlace simbólico')
    if not path.is_file() or not stat.S_ISREG(path.lstat().st_mode):
        raise ValueError('Entrada no es archivo regular')
    return path


def fresh_output(path, root):
    path = Path(path).absolute()
    if path.exists() or path.is_symlink():
        raise FileExistsError('Salida existente: no sobrescribir')
    if '..' in path.parts or any(p.is_symlink() for p in path.parents):
        raise ValueError('Salida por enlace/recorrido padre')
    resolved = path.resolve()
    if resolved == root or root in resolved.parents or resolved == TEAM or TEAM in resolved.parents:
        raise ValueError('Salida dentro de raíz fuente/activa')
    return path


def constants(tree, initial=None):
    """Evaluar solo expresiones de constantes AST; nunca exec/eval de fuentes."""
    values = dict(initial or {})
    operations = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Pow: operator.pow}

    def read(node):
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.Name):
            return values[node.id]
        if isinstance(node, (ast.Tuple, ast.List)):
            return tuple(read(x) for x in node.elts)
        if isinstance(node, ast.Dict):
            return {read(k): read(v) for k, v in zip(node.keys, node.values)}
        if isinstance(node, ast.BinOp) and type(node.op) in operations:
            left, right = read(node.left), read(node.right)
            if isinstance(node.op, ast.Pow) and not 0 <= right <= 10:
                raise ValueError('Exponente no pequeño')
            return operations[type(node.op)](left, right)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'len' and len(node.args) == 1:
            return len(read(node.args[0]))
        raise ValueError('No es constante admitida')

    for node in tree.body:
        if isinstance(node, ast.Assign):
            try:
                value = read(node.value)
            except (ValueError, KeyError, TypeError):
                continue
            for target in node.targets:
                if isinstance(target, ast.Name):
                    values[target.id] = value
    return values


def inputs(root_path, search_path, weights_path, book_path, budget):
    root = checked_root(root_path)
    search, weights, book = [input_path(root, p) for p in [search_path, weights_path, book_path]]
    strategy = input_path(root, 'strategy.py')
    metadata = tomllib.loads(input_path(root, 'equipo.toml').read_text())
    name = metadata['nombre']
    setup()
    from validador.reglas import PATRON_NOMBRE
    if not isinstance(name, str) or not PATRON_NOMBRE.fullmatch(name) or name in ['random', 'montecarlo', 'humano'] or name.startswith(('tier_', '_')):
        raise ValueError('Nombre no válido')
    config = constants(ast.parse(strategy.read_text()))
    weights_name = config.get('PESOS_EVAL3')
    if not isinstance(weights_name, str) or Path(weights_name).name != weights_name or not weights_name.endswith('.npz'):
        raise ValueError('Nombre NPZ relativo no reconocido en estrategia')
    files = {'strategy.py': strategy, 'busqueda_eval3.py': search,
             'data/' + weights_name: weights, 'data/libro.json': book,
             'equipo.toml': input_path(root, 'equipo.toml'), 'INFORME.md': input_path(root, 'INFORME.md')}
    if (root/'requirements.txt').exists():
        files['requirements.txt'] = input_path(root, 'requirements.txt')
    dependencies = {'standard_library': [], 'preinstalled': [], 'tournament_api': []}
    todo, done = ['strategy.py', 'busqueda_eval3.py'], set()
    while todo:
        destination = todo.pop()
        if destination in done:
            continue
        done.add(destination)
        tree = ast.parse(files[destination].read_text(), filename=destination)
        for node in ast.walk(tree):
            imported = []
            if isinstance(node, ast.Import):
                imported = [a.name.split('.')[0] for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    raise ValueError('Paquetes relativos requieren adaptador explícito')
                imported = [node.module.split('.')[0]] if node.module else []
            for module in imported:
                if module in ['numpy', 'scipy', 'numba', 'llvmlite']:
                    dependencies['preinstalled'].append(module)
                elif module == 'motor':
                    dependencies['tournament_api'].append(module)
                elif module in sys.stdlib_module_names or module == '__future__':
                    dependencies['standard_library'].append(module)
                else:
                    target = module + '.py'
                    if target not in files:
                        files[target] = input_path(root, target)
                    todo.append(target)
        budget.wait()
    if 'eval3.py' not in files:
        raise ValueError('El buscador debe declarar eval3')
    for group in dependencies:
        dependencies[group] = sorted(set(dependencies[group]))
    sources = {name: {'sha256': sha(path, budget), 'bytes': path.stat().st_size, 'mode': '0644'} for name, path in sorted(files.items())}
    return root, name, files, sources, dependencies


def rules_hashes(budget):
    paths = [ROOT/'docs/reglas.md', ROOT/'docs/entregar.md', ROOT/'sistema/limites.toml', ROOT/'sistema/config.py',
             ROOT/'sistema/requirements.txt', ROOT/'sistema/requirements-dev.txt',
             *sorted((ROOT/'sistema/validador').glob('*.py'))]
    return {str(p.relative_to(ROOT)): sha(p, budget) for p in paths}


def recipe(args, budget):
    root, name, files, sources, dependencies = inputs(args.raiz_participante, args.buscador, args.pesos, args.libro, budget)
    portable = {'format': FORMAT, 'team': name, 'constructor_sha256': sha(Path(__file__)),
                'constructor_support_sha256': {'fase8a_soporte.py': sha(Path(__file__).with_name('fase8a_soporte.py'))}, 'files': sources,
                'dependencies': dependencies, 'official_sources': rules_hashes(budget),
                'archive': {'prefix': 'estudiantes/' + name, 'mtime': 0, 'uid': 0, 'gid': 0, 'mode': '0644'},
                'selection': 'explicit_inputs_only_no_model_decision', 'static_smoke': False}
    return root, portable, files


def freeze(args):
    budget = Budget()
    root, portable, files = recipe(args, budget)
    output = fresh_output(args.salida, root)
    output.mkdir(parents=True, exist_ok=False)
    save(output/'receta.json', portable)
    save(output/'procedencia.json', {'root': str(root), 'sources': {name: str(path) for name, path in files.items()},
                                  'constructor': str(Path(__file__).resolve())})
    budget.wait()
    return {'recipe': str(output/'receta.json'), 'files': len(files)}


def build(args):
    budget = Budget()
    root, current, files = recipe(args, budget)
    expected = json.loads(args.receta.read_text())
    if expected != current:
        raise ValueError('Receta rechazada: fuente/modelo/libro/dependencias/reglas modificados')
    output = fresh_output(args.salida, root)
    # Todos los hashes se verifican ANTES de crear la salida.
    content = {}
    for name, path in files.items():
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != expected['files'][name]['sha256']:
            raise ValueError('Fuente cambió durante lectura')
        content[name] = raw
        budget.wait()
    output.mkdir(parents=True, exist_ok=False)
    participant = output/'estudiantes'/expected['team']
    participant.mkdir(parents=True)
    for name, raw in sorted(content.items()):
        target = participant/name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        target.chmod(0o644)
    archive = output/'participante.tar'
    with tarfile.open(archive, 'x', format=tarfile.USTAR_FORMAT) as tar:
        for name, raw in sorted(content.items()):
            info = tarfile.TarInfo(expected['archive']['prefix'] + '/' + name)
            info.size, info.mode, info.mtime, info.uid, info.gid = len(raw), 0o644, 0, 0, 0
            info.uname, info.gname = '', ''
            tar.addfile(info, io.BytesIO(raw))
    save(output/'receta.json', expected)
    manifest = {'format': FORMAT, 'team': expected['team'], 'recipe_sha256': sha(args.receta), 'files': expected['files'],
                'dependencies': expected['dependencies'], 'archive_sha256': sha(archive, budget),
                'archive_bytes': archive.stat().st_size, 'game_tree': 'estudiantes/' + expected['team'],
                'cache_copied': False, 'selection': expected['selection']}
    save(output/'manifiesto.json', manifest)
    save(output/'procedencia.json', {'root': str(root), 'recipe': str(args.receta.resolve()),
                                   'sources': {name: str(path) for name, path in files.items()}})
    budget.wait()
    return {'participant': str(participant), 'archive_sha256': manifest['archive_sha256'], 'files': len(files)}


def npz_review(participant, budget):
    import numpy as np
    motor = constants(ast.parse((ROOT/'sistema/motor/nucleo.py').read_text()))
    config = constants(ast.parse((participant/'eval3.py').read_text()), motor)
    if config['N_PESOS'] != 275 or config['N_FEATURES'] != 267 or len(config['BANDERAS']) != 8:
        raise ValueError('Esquema eval3 no es275/267/8')
    strategy_config = constants(ast.parse((participant/'strategy.py').read_text()))
    with np.load(participant/'data'/strategy_config['PESOS_EVAL3'], allow_pickle=False) as data:
        weights = data['pesos']
        if weights.shape != (275,) or weights.dtype != np.float64 or not np.isfinite(weights).all():
            raise ValueError('NPZ no contiene vector275 float64 finito')
        flags = weights[267:]
        if not np.isin(flags, [0.0, 1.0]).all():
            raise ValueError('Banderas no binarias')
        inactive = []
        for flag, family in zip(flags, config['BANDERAS']):
            if flag == 0:
                lo, hi = config['FAMILIAS'][family]
                if np.any(weights[lo:hi] != 0):
                    raise ValueError('Familia apagada con pesos no nulos: ' + family)
                inactive.append(family)
        result = {'shape': list(weights.shape), 'dtype': str(weights.dtype), 'finite': True,
                  'flags': dict(zip(config['BANDERAS'], [int(x) for x in flags])), 'inactive_zero_weights': inactive,
                  'keys': list(data.files), 'no_pickle': True}
    budget.wait()
    return result


def validate_book(book):
    if not isinstance(book, dict):
        raise ValueError('Libro no es objeto')
    for key, move in book.items():
        if not isinstance(key, str) or not key.isascii() or not key.isdecimal() or str(int(key)) != key or not 0 <= int(key) < 2**64:
            raise ValueError('Clave no canónica uint64')
        if not isinstance(move, list) or len(move) != 2 or any(type(v) is not int or not 0 <= v < 81 for v in move):
            raise ValueError('Movimiento no es par entero0..80')
        a, b = move
        if abs(a//9-b//9) != 1 or abs(a%9-b%9) > 1:
            raise ValueError('Geometría del movimiento inválida')


def audit(args):
    budget = Budget()
    setup()
    output = Path(args.paquete).resolve()
    manifest = json.loads((output/'manifiesto.json').read_text())
    participant = output/manifest['game_tree']
    actual_files = sorted(str(p.relative_to(participant)) for p in participant.rglob('*') if p.is_file())
    if actual_files != sorted(manifest['files']):
        raise ValueError('Inventario de juego distinto del manifiesto')
    if any(p.is_symlink() for p in [participant, *participant.rglob('*')]):
        raise ValueError('Enlace en paquete')
    for name, info in manifest['files'].items():
        if sha(participant/name, budget) != info['sha256']:
            raise ValueError('Archivo modificado en paquete: ' + name)
    if sha(output/'participante.tar', budget) != manifest['archive_sha256']:
        raise ValueError('Tar modificado')
    with tarfile.open(output/'participante.tar') as tar:
        names = []
        for item in tar:
            if not item.isfile() or Path(item.name).is_absolute() or '..' in Path(item.name).parts or item.issym() or item.islnk():
                raise ValueError('Miembro inseguro en tar')
            relative = str(Path(item.name).relative_to(Path(manifest['game_tree'])))
            if relative not in manifest['files'] or hashlib.sha256(tar.extractfile(item).read()).hexdigest() != manifest['files'][relative]['sha256']:
                raise ValueError('Contenido de tar distinto de inventario')
            names.append(relative)
            budget.wait()
        if sorted(names) != actual_files:
            raise ValueError('Miembros duplicados/faltantes en tar')
    from config import cargar_limites
    from validador import validar as official
    limits = cargar_limites(ROOT/'sistema/limites.toml')
    original_smoke = official._jugar_humo
    calls = []

    def forbidden_smoke(*args, **kwargs):
        calls.append(True)
        raise AssertionError('Nunca ejecutar humo en 8B.1')

    try:
        official._jugar_humo = forbidden_smoke
        report = official.validar_equipo(participant, limits, jugar_humo=False, docker=False, oficial=False, entrega=True)
        assert not calls and not report.humo_jugado
    finally:
        official._jugar_humo = original_smoke
    absolute_paths, imports = [], {}
    for name in actual_files:
        p = participant/name
        if p.suffix in ['.py', '.md', '.txt', '.toml', '.json']:
            text = p.read_text()
            if '/Users/' in text or '/home/' in text or 'file://' in text:
                absolute_paths.append(name)
            if p.suffix == '.py':
                tree = ast.parse(text)
                imports[name] = sorted({a.name for x in ast.walk(tree) if isinstance(x, ast.Import) for a in x.names} |
                                       {x.module for x in ast.walk(tree) if isinstance(x, ast.ImportFrom) and x.module})
        budget.wait()
    if absolute_paths:
        raise ValueError('Rutas de host en árbol de juego: ' + str(absolute_paths))
    book = json.loads((participant/'data/libro.json').read_text())
    validate_book(book)
    npz = npz_review(participant, budget)
    review = {'static_only': True, 'official_static_api': 'validar_equipo(jugar_humo=False,entrega=True)',
              'official_static_report': asdict(report), 'smoke_guard_calls': len(calls),
              'official_validation_approval': False, 'limits_source': 'sistema/limites.toml', 'limits': asdict(limits),
              'inventory': manifest['files'], 'files': len(actual_files),
              'total_bytes': sum(info['bytes'] for info in manifest['files'].values()),
              'no_symlinks': True, 'no_host_absolute_paths': True, 'imports': imports, 'npz': npz,
              'book': {'entries': len(book), 'schema': 'canonical_uint64_pair_0..80', 'contextual_legality': 'only_existing_phase7A_evidence_not_replayed'},
              'unmeasured': ['JIT', 'Linux_ABI', 'cold_start', 'clock', 'peak_memory', 'strength'],
              'official_sources': rules_hashes(budget)}
    if args.salida.exists() or args.salida.is_symlink():
        raise FileExistsError('Resultado estático existente')
    save(args.salida, review)
    budget.wait()
    return {'static_ok': report.ok, 'humo_jugado': False, 'files': len(actual_files), 'bytes': review['total_bytes']}


def main():
    setup()
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for command in ['congelar', 'construir']:
        p = sub.add_parser(command)
        p.add_argument('--raiz-participante', type=Path, required=True)
        p.add_argument('--buscador', type=Path, required=True)
        p.add_argument('--pesos', type=Path, required=True)
        p.add_argument('--libro', type=Path, required=True)
        p.add_argument('--salida', type=Path, required=True)
        if command == 'construir':
            p.add_argument('--receta', type=Path, required=True)
    p = sub.add_parser('auditar')
    p.add_argument('--paquete', type=Path, required=True)
    p.add_argument('--salida', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps({'congelar': freeze, 'construir': build, 'auditar': audit}[args.command](args), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
