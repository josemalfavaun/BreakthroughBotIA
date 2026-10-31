"""Probe externo al participante, ejecutado solo dentro del contenedor propio8B2."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import signal
import sys
import time


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def cgroup():
    paths=['/sys/fs/cgroup/memory.peak','/sys/fs/cgroup/memory.current','/sys/fs/cgroup/memory.max',
           '/sys/fs/cgroup/cpu.max','/sys/fs/cgroup/cpu.stat','/sys/fs/cgroup/memory.events']
    return {p:Path(p).read_text().strip() for p in paths if Path(p).is_file()}


def identity():
    import numpy as np
    import numba
    from motor import nucleo
    return {'python':sys.version,'numpy':np.__version__,'numba':numba.__version__,
            'platform':sys.platform,'architecture':platform.machine(),'motor_file':nucleo.__file__,
            'motor_sha256':digest(nucleo.__file__),
            'files':{name:digest(Path('/bot')/name) for name in ['strategy.py','busqueda_eval3.py','eval3.py','data/pesos_eval3_ligero.npz','data/libro.json']}}


def cache_stats(search):
    result={}
    for name in ['_mejor_jugada_numba','_valor_numba','_evaluar_numba']:
        f=getattr(search,name)
        stats=getattr(f,'stats',None)
        result[name]={'cache_hits':sum(stats.cache_hits.values()) if stats else None,
                      'cache_misses':sum(stats.cache_misses.values()) if stats else None,
                      'signatures':[str(s) for s in getattr(f,'signatures',[])],
                      'code_filename':getattr(f,'py_func',f).__code__.co_filename}
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode',choices=['abi','cold','functional'],required=True)
    args=parser.parse_args()
    if args.mode=='abi':
        print(json.dumps({'identity':identity(),'cgroup':cgroup()},ensure_ascii=False));return
    from arbitro import runner
    runner.copiar_cache_numba()
    runner.calentar_motor()
    start=time.perf_counter()
    strategy=None

    def deadline(*args):
        raise TimeoutError('import+preparar excedió10s de reloj')

    signal.signal(signal.SIGALRM,deadline)
    signal.setitimer(signal.ITIMER_REAL,10.0)
    error=None
    try:
        strategy=runner.cargar_estrategia(Path('/bot'))
        imported=time.perf_counter()
        strategy.preparar(runner.Config('blancas',0,Path('/bot/data'),30.0))
        prepared=time.perf_counter()
    except BaseException as exc:
        error={'type':type(exc).__name__,'message':str(exc)}
        imported=locals().get('imported',time.perf_counter());prepared=time.perf_counter()
    finally:
        signal.setitimer(signal.ITIMER_REAL,0)
    result={'mode':args.mode,'ok':error is None and prepared-start<10.0,'error':error,
            'import_s':imported-start,'prepare_only_s':prepared-imported,'total_prepare_s':prepared-start,
            'identity':identity(),'cgroup':cgroup()}
    if error is None:
        result['loaded']={'strategy_file':strategy.__file__,'strategy_code_file':strategy.jugar.__code__.co_filename,
                          'search_file':strategy._busqueda.__file__,'gain':float(strategy._busqueda._pesos_y_ganancia()[1]),
                          'cache_stats':cache_stats(strategy._busqueda)}
    if args.mode=='functional' and result['ok']:
        import numpy as np
        from motor import Estado,Jugada
        from motor.nucleo import MAX_JUGADAS
        search=strategy._busqueda
        cases=[]
        # Solo globals de fixture; todos se restauran antes de terminar.
        previous={name:getattr(strategy,name) for name in ['color','libro','reserva']}
        try:
            for color in ['blancas','negras']:
                if color=='blancas':
                    d={'blancas':['a8'],'negras':['b9','i8'],'turno':color,'puntos':{'blancas':2,'negras':0}}
                    attack,safe=Jugada(63,73),Jugada(63,72)
                    f={'blancas':['a2'],'negras':['a3','i8'],'turno':color}
                else:
                    d={'blancas':['h1','a2'],'negras':['i2'],'turno':color,'puntos':{'blancas':0,'negras':2}}
                    attack,safe=Jugada(17,7),Jugada(17,8)
                    f={'blancas':['i7','a2'],'negras':['i8'],'turno':color}
                state=Estado.desde_dict(d)
                strategy.color=color;strategy.libro={str(state.clave):list(attack)}
                chosen=strategy.jugar(state,30.0)
                assert chosen==safe and all(child.ganador()==color for _,child in state.siguiente(chosen))
                branches=[{'p':p,'winner':child.ganador(),'points':child.puntos} for p,child in state.siguiente(attack)]
                assert len(branches)==2 and branches[0]['winner']==color and branches[1]['winner']!=color
                cases.append({'kind':'safe_before_book','color':color,'move':list(chosen),'attack_branches':branches})
                forced=Estado.desde_dict(f);strategy.libro={str(forced.clave):[0,80]}
                assert len(forced.jugadas())==1 and strategy.jugar(forced,0)==forced.jugadas()[0]
                cases.append({'kind':'forced','color':color,'legal':True})
                quiet=Estado.inicial().a_dict();quiet['turno']=color;quiet=Estado.desde_dict(quiet)
                strategy.libro={};strategy.reserva=1.0
                chosen=strategy.jugar(quiet,0.0)
                assert chosen in quiet.jugadas()
                cases.append({'kind':'short_clock_fallback','color':color,'move':list(chosen),'legal':True})
            strategy.libro={}
            tab,pts,color=search._tablero_desde_estado(Estado.inicial())
            count=np.zeros(2,np.int64);weights,gain=search._pesos_y_ganancia()
            move=search._mejor_jugada_numba(tab,pts,color,3,weights,gain,-1,-1,count,1)
            assert move[3]==1 and count[1]==1
            cases.append({'kind':'aborted_root_unknown','result':[int(move[0]),int(move[1]),float(move[2]),int(move[3]),int(move[4])],
                          'counter':[int(x) for x in count],'discard_partial_value':True})
            e=Estado.desde_dict({'blancas':['a3','e4'],'negras':['b7','g6'],'turno':'blancas'})
            for objective,expected in [(0,-1.3877787807814457e-17),(1,1.3877787807814457e-17)]:
                keys=np.zeros(search.TT_TAM,np.uint64);values=np.zeros(search.TT_TAM)
                observed=[]
                for alpha,beta in ([(gain-1,gain),(-gain,gain)] if objective==0 else [(-gain,1-gain),(-gain,gain)]):
                    t,p,c=search._tablero_desde_estado(e);counter=np.zeros(2,np.int64)
                    value=float(search._valor_numba(t,p,c,objective,2,alpha,beta,weights,gain,np.empty(MAX_JUGADAS,np.int64),
                           np.empty(MAX_JUGADAS,np.int64),keys,values,counter,5000))
                    assert counter[1]==0;observed.append(value)
                assert abs(observed[-1]-expected)<=1e-12
                cases.append({'kind':'Linux_compiled_TT_equivalence','objective':objective,'observed':observed,'oracle8A':expected})
        finally:
            for name,value in previous.items():setattr(strategy,name,value)
        result['functional']={'passed':len(cases),'cases':cases,'globals_restored':True,'TT_size_unmodified':search.TT_TAM}
        result['cgroup']=cgroup()
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
