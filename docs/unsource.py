#!/usr/bin/env python3

import collections
import pathlib
import sys
from typing import Dict, List

sources:Dict[str,List[str]] = collections.defaultdict(list)

pytxcode = sys.argv[1]
dstsource = sys.argv[2] if len(sys.argv)==3 else "pythontex_sources"
with open(pytxcode, encoding='utf8') as f:
  in_source = False
  spaces_to_trim = None
  source_name = 'source'
  for line in f:
    if line.startswith('=>PYTHONTEX#'):
      in_source = True
      spaces_to_trim = None
      source_name = f'source_{line.split("#")[1]}_{line.split("#")[2]}.py'
    elif line.startswith('=>PYTHONTEX') or line.startswith('=>DEPYTHONTEX'):
      in_source = False
    elif in_source:
      if spaces_to_trim is None:
        # Detect the number of leading spaces to trim using the first line
        spaces_to_trim = 0
        for c in line:
          if c!=' ':
            break
          spaces_to_trim+=1
      if len(line[:spaces_to_trim].strip()) != 0:
        print(f"Can't find {spaces_to_trim} spaces at the beginning of line '{line}'")
      else:
        line=line[spaces_to_trim:]
      sources[source_name].append(line)

if len(sources.keys())==1:
  with open(dstsource, 'w', encoding='utf8') as f:
    f.write(''.join(sources[list(sources.keys())[0]]))
else:
  source_path = pathlib.Path(dstsource)
  if not source_path.is_dir():
    source_path.mkdir()
  for source, lines in sources.items():
    with open(source_path / source, 'w', encoding='utf8') as f:
      f.write(''.join(lines))

