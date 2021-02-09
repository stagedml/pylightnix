from pylightnix import ( RConfig, datahash, PYLIGHTNIX_NAMEPAT, mkdref, mkrref,
    trimhash, encode )

from tests.imports import (
    given, assume, example, note, settings, text, decimals, integers, rmtree,
    characters, gettempdir, isdir, join, makedirs, from_regex, islink, listdir,
    get_executable, run, dictionaries, one_of, lists, recursive, printable,
    none, booleans, floats, re_compile, composite, event, binary, just )

#   ____                           _
#  / ___| ___ _ __   ___ _ __ __ _| |_ ___  _ __ ___
# | |  _ / _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__/ __|
# | |_| |  __/ | | |  __/ | | (_| | || (_) | |  \__ \
#  \____|\___|_| |_|\___|_|  \__,_|\__\___/|_|  |___/

@composite
def drefs(draw):
  return mkdref(trimhash(draw(hashes())), draw(names()))

@composite
def rrefs(draw):
  return mkrref(trimhash(draw(hashes())), trimhash(draw(hashes())), draw(names()))

@composite
def dicts(draw, prims=none()):
  d=draw(
    dictionaries(
      keys=text(printable),
      values=recursive(none() | booleans() | floats() | text(printable) | integers() | prims,
                lambda children:
                  lists(children) |
                  dictionaries(text(printable), children),
                  max_leaves=10)
      ))
  event(str(d))
  return d

def dicts_with_refs():
  return dicts(prims=rrefs() | drefs())

@composite
def configs(draw):
  d=draw(dicts())
  name=draw(one_of(none(), names()))
  if name is not None:
    d.update({'name':name})
  return RConfig(d)

def names():
  return from_regex(re_compile(f'^{PYLIGHTNIX_NAMEPAT}+$'))

def hashes():
  return text().map(lambda x: datahash([('testhash',encode(x))]))

def prims():
  return one_of(none(), booleans(), floats(), text(printable), integers(), binary())

def bindata():
  return one_of(one_of(booleans(), floats(), integers()).map(lambda x: str(x)).map(lambda x: bytes(x,'utf-8')),
                text(printable).map(lambda x: bytes(x,'utf-8')),
                binary())

@composite
def artifacts(draw):
  ns=draw(lists(names(),min_size=1))
  vals=draw(lists(bindata(),min_size=len(ns),max_size=len(ns)))
  return {n:v for n,v in zip(ns,vals)}

