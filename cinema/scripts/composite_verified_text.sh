#!/usr/bin/env bash
set -euo pipefail
IN="$1"; OUT="$2"
ffmpeg -y -i "$IN" -vf "drawbox=x=40:y=h-150:w=w-80:h=100:color=black@0.58:t=fill,drawtext=text='RED LEOPARDS 191.90  |  CHILI CHEESERS 100.90':x=70:y=h-115:fontsize=30:fontcolor=white" -c:v libx264 -crf 18 -pix_fmt yuv420p -an "$OUT"
