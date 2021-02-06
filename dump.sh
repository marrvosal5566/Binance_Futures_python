#!/bin/sh

at -m 0900 tomorrow <<ENDMARKER
python3 liquid/get_liquid_pool_asset.py
sleep 100
git add *
git ci -m "update"
git push tchou
bash dump.sh
ENDMARKER
