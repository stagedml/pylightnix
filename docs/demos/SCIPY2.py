from pylightnix import (StorageSettings, Matcher, Build, Context, Path, RefPath,
                        Config, Registry, RRef, DRef, Path, build_path,
                        build_outpath, build_cattrs, mkdrv, rref2path, mkconfig,
                        tryread, fetchurl, instantiate, realize1, match_only,
                        build_wrapper, selfref, mklens, instantiate_inplace,
                        realize_inplace, rmref, fsinit, pack, unpack, allrrefs,
                        gc, redefine, match_some, match_latest, dirrm,
                        mksettings, readstr, writestr)

from typing import List, Optional
from numpy import vstack, array, save, load, exp
from numpy.random import rand
from scipy.cluster.vq import kmeans,vq,whiten
from scipy.optimize import dual_annealing

import matplotlib.pyplot as plt

from contextlib import contextmanager

# https://www.tutorialkart.com/python/scipy/scipy-kmeans/
# https://numpy.org/doc/stable/reference/generated/numpy.save.html
# https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.optimize.anneal.html

# 0.

def f(z, *params):
    x, y = z
    a, b, c, d, e, f, g, h, i, j, k, l, scale = params
    return (a * x**2 + b * x * y + c * y**2 + d*x + e*y + f) + \
           (-g*exp(-((x-h)**2 + (y-i)**2) / scale)) + \
           (-j*exp(-((x-k)**2 + (y-l)**2) / scale))

# 1.

def stage_params(r:Registry)->DRef:
  def _config():
    name = 'params'
    out = [selfref, "params.npy"]
    return locals()
  def _make(b:Build):
    save(mklens(b).out.syspath, (2, 3, 7, 8, 9, 10, 44, -1, 2, 26, 1, -2, 0.5))
  return mkdrv(r, mkconfig(_config()), match_only(), build_wrapper(_make))

def stage_anneal(r:Registry, ref_params:DRef)->DRef:
  def _config():
    name = 'anneal2'
    nonlocal ref_params
    trace_xs = [selfref, 'tracex.npy']
    trace_fs = [selfref, 'tracef.npy']
    out = [selfref, 'result.npy']
    return locals()
  def _make(b:Build):
    params = load(mklens(b).ref_params.out.syspath)
    xs = []; fs = []
    def _trace(x,f,ctx):
      nonlocal xs,fs
      xs.append(x.tolist())
      fs.append(f)
    res = dual_annealing(f, [[-10,10],[-10,10]],
                         x0=[2.,2.],args=params,
                         maxiter=500, callback=_trace)
    save(mklens(b).trace_xs.syspath, array(xs))
    save(mklens(b).trace_fs.syspath, array(fs))
    save(mklens(b).out.syspath, res['x'])
  return mkdrv(r, mkconfig(_config()), match_only(), build_wrapper(_make))


def stage_plot(r:Registry, ref_anneal:DRef)->DRef:
  def _config():
    name = 'plot'
    nonlocal ref_anneal
    out = [selfref, 'plot.png']
    return locals()
  def _make(b:Build):
    xs=load(mklens(b).ref_anneal.trace_xs.syspath)
    fs=load(mklens(b).ref_anneal.trace_fs.syspath)
    res=load(mklens(b).ref_anneal.out.syspath)
    plt.figure()
    plt.title(f"Min {fs[-1]}, found at {res}")
    plt.plot(range(len(fs)),fs)
    plt.grid(True)
    plt.savefig(mklens(b).out.syspath)
  return mkdrv(r, mkconfig(_config()), match_latest(), build_wrapper(_make))

def run1():
  ds=instantiate_inplace(stage_params)
  cl=instantiate_inplace(stage_anneal,ds)
  vis=instantiate_inplace(stage_plot,cl)
  return realize_inplace(vis)

# 2.

def stage_all(r:Registry):
  ds=stage_params(r)
  cl=stage_anneal(r,ds)
  vis=stage_plot(r,cl)
  return vis


def run2(S=None):
  return realize1(instantiate(stage_all,S=S))

# 3. Different storages

Sa=mksettings('_storageA')
Sb=mksettings('_storageB')

def run3():
  fsinit(Sa,remove_existing=True)
  fsinit(Sb,remove_existing=True)
  rrefA=realize1(instantiate(stage_all, S=Sa))
  kittyshow(mklens(rrefA,S=Sa).out.syspath)
  rrefB=realize1(instantiate(stage_all, S=Sb))
  kittyshow(mklens(rrefB,S=Sb).out.syspath)
  print(rrefA)
  print(rrefB)
  print('Before', list(allrrefs(S=Sb)))
  arch=Path('archive.zip')
  pack([rrefA], arch, S=Sa)
  unpack(arch, S=Sb)
  print('After', list(allrrefs(S=Sb)))

# 4. Overwriting matchers

def match_min(S, rrefs:List[RRef])->List[RRef]:
  avail=[load(mklens(rref,S=S).trace_fs.syspath)[-1] for rref in rrefs]
  best=sorted(zip(avail,rrefs))[0]
  if best[1] in allrrefs(Sa):
    print(f"Picking Alice ({best[0]}) out of {avail}")
  else:
    print(f"Picking Bob ({best[0]}) out of {avail}")
  return [best[1]]

def stage_all2(r:Registry):
  ds=stage_params(r)
  cl=redefine(stage_anneal, new_matcher=match_min)(r,ds)
  vis=stage_plot(r,cl)
  return vis

def run4():
  run3()
  return realize1(instantiate(stage_all2,S=Sb))


#############################################################

IMGDIR='img'
from os.path import join
from os import makedirs, get_terminal_size
from tempfile import NamedTemporaryFile
from subprocess import call

def kittyshow(path):
  ret=call(['upload-terminal-image.sh',
            '-c','70',
            '-r','30',path])
  assert ret==0, f"upload-terminal-image.sh returned {ret}"

@contextmanager
def kittyupload():
  with NamedTemporaryFile(suffix='.png') as f:
    yield f
    ret=call(['upload-terminal-image.sh', f.name])
    assert ret==0, f"upload-terminal-image.sh returned {ret}"

from shutil import copyfileobj
def kittyplot(path:str)->None:
  with kittyupload() as d:
    with open(path,'rb') as s:
      copyfileobj(s,d)

