#!/bin/sh
SRC="$1"
TGT="$2"
codebraid pandoc \
  -f markdown -t markdown --no-cache --overwrite --standalone --self-contained \
  -o _tmp.md "$SRC"
pandoc -f markdown \
  --to=markdown-smart-simple_tables-multiline_tables-grid_tables-fenced_code_attributes-inline_code_attributes-raw_attribute-pandoc_title_block-yaml_metadata_block \
  --toc -s _tmp.md -o "$TGT"

