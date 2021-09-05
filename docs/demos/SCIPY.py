from pylightnix import (StorageSettings, Matcher, Build, Context, Path, RefPath,
                        Config, Registry, RRef, DRef, Path, build_path,
                        build_outpath, build_cattrs, mkdrv, rref2path, mkconfig,
                        tryread, fetchurl, instantiate, realize1, match_only,
                        build_wrapper, selfref, mklens, instantiate_inplace,
                        realize_inplace, rmref, fsinit, pack, unpack, allrrefs,
                        gc, redefine, match_some, match_latest, dirrm,
                        mksettings, readstr, writestr)

from typing import List, Optional
from numpy import vstack, array, save, load
from numpy.random import rand
from scipy.cluster.vq import kmeans,vq,whiten

import matplotlib.pyplot as plt

from contextlib import contextmanager

# https://www.tutorialkart.com/python/scipy/scipy-kmeans/
# https://numpy.org/doc/stable/reference/generated/numpy.save.html


# 1.

def stage_dataset(r:Registry)->DRef:
  def _config():
    name = 'dataset'
    centers = [1,3,4.5]
    rnd_shape = [20,2]
    out = [selfref, "dataset.npy"]
    return locals()
  def _make(b:Build):
    data = vstack([rand(*mklens(b).rnd_shape.val)+center
                   for center in mklens(b).centers.val])
    save(mklens(b).out.syspath, data)
  return mkdrv(r, mkconfig(_config()), match_only(), build_wrapper(_make))


def stage_cluster(r:Registry, ref_dataset:DRef)->DRef:
  def _config():
    name = 'cluster'
    nonlocal ref_dataset
    out = [selfref, 'clusters.npy']
    distortion = [selfref, 'distortion.txt']
    return locals()
  def _make(b:Build):
    data = load(mklens(b).ref_dataset.out.syspath)
    clusters,distortion=kmeans(data, len(mklens(b).ref_dataset.centers.val))
    save(mklens(b).out.syspath,clusters)
    writestr(mklens(b).distortion.syspath, str(distortion))
  return mkdrv(r, mkconfig(_config()), match_only(), build_wrapper(_make))


def stage_plot(r:Registry, ref_cluster:DRef)->DRef:
  def _config():
    name = 'plot'
    nonlocal ref_cluster
    out = [selfref, 'plot.png']
    return locals()
  def _make(b:Build):
    data=load(mklens(b).ref_cluster.ref_dataset.out.syspath)
    clusters=load(mklens(b).ref_cluster.out.syspath)
    plt.plot(data[:,0],data[:,1],'go',
             clusters[:,0],clusters[:,1],'bs')
    plt.savefig(mklens(b).out.syspath)
  return mkdrv(r, mkconfig(_config()), match_only(), build_wrapper(_make))


def run1():
  ds=instantiate_inplace(stage_dataset)
  cl=instantiate_inplace(stage_cluster,ds)
  vis=instantiate_inplace(stage_plot,cl)
  return realize_inplace(vis)

# 2. Functional API

def stage_all(r:Registry):
  ds=stage_dataset(r)
  cl=stage_cluster(r,ds)
  vis=stage_plot(r,cl)
  return vis

def run2(S=None):
  return realize1(instantiate(stage_all,S=S))

# 3. Different storages

Sa=mksettings('_storageA')
Sb=mksettings('_storageB')
fsinit(Sa,remove_existing=True)
fsinit(Sb,remove_existing=True)

def run_copystorage():
  rrefA=realize1(instantiate(stage_all, S=Sa))
  rrefB=realize1(instantiate(stage_all, S=Sb))
  print(rrefA)
  print(rrefB)
  print('Before', list(allrrefs(S=Sb)))
  arch=Path('archive.zip')
  pack([rrefA], arch, S=Sa)
  unpack(arch, S=Sb)
  print('After', list(allrrefs(S=Sb)))

# 4. Overwriting matchers

def match_min_distortion(S:Optional[StorageSettings],
                         rrefs:List[RRef])->List[RRef]:
  distortions=[float(readstr(mklens(rref,S=S).distortion.syspath)) \
               for rref in rrefs]
  best:RRef=sorted(zip(distortions,rrefs))[0][1]
  return [best]


def stage_all2(r:Registry):
  ds=redefine(stage_dataset, new_matcher=match_latest())(r)
  cl=redefine(stage_cluster, new_matcher=match_min_distortion)(r,ds)
  vis=redefine(stage_plot, new_matcher=match_latest())(r,cl)
  return vis

def run_matchers():
  # Call after run_copystorage
  return realize1(instantiate(stage_all2,S=Sb))


#############################################################

IMGDIR='img'
from os.path import join
from os import makedirs
from tempfile import NamedTemporaryFile
from subprocess import call

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

