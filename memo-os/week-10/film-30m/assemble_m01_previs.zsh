#!/bin/zsh
# Assemble W10 M01's five independent audio buses + monitoring MP4.
# Candidate dialogue is Mac system TTS only; NOT approved casting, performed VO or lip-sync.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="$HERE/proofs/M01_RODEO_STUNT_PREVIS"
mkdir -p "$OUT"
FF=$(/tmp/schemin-week10-film-qa-venv/bin/python -c 'import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())')
if [[ ! -s "$OUT/W10_M01_stunt_previs_silent.mp4" ]]; then
  echo "No source moving previs; run make_m01_previs.py" >&2; exit 2
fi

say -v Daniel -r 165 -o "$OUT/VO_01_TEMP.aiff" "In the Highland galleries, the joke was funny once. Then the outlaw decided twice would be better."
say -v Fred -r 170 -o "$OUT/DX_CHILI_01_TEMP.aiff" "Four hooves, and not one knows how to dance."
say -v Ralph -r 150 -o "$OUT/DX_DK_01_TEMP.aiff" "That was your second chance."
say -v Daniel -r 160 -o "$OUT/VO_02_TEMP.aiff" "The loop closed around his torso. The skid was his own doing. The knot came later."
say -v Fred -r 164 -o "$OUT/DX_CHILI_02_TEMP.aiff" "They're still watching?"
say -v Ralph -r 150 -o "$OUT/DX_DK_02_TEMP.aiff" "You asked for an audience."

for stem in AMB FX MX; do
  "$FF" -y -hide_banner -loglevel error -i "$OUT/W10_M01_${stem}_original_24k.wav" \
     -af "apad,atrim=0:42" -ar 48000 -c:a pcm_s24le "$OUT/W10_M01_${stem}_48k24.wav"
done

"$FF" -y -hide_banner -loglevel error -i "$OUT/VO_01_TEMP.aiff" -i "$OUT/VO_02_TEMP.aiff" \
  -filter_complex "[0:a]aresample=48000,adelay=1200:all=1[a];[1:a]aresample=48000,adelay=22800:all=1[b];[a][b]amix=inputs=2:duration=longest:normalize=0,apad,atrim=0:42[m]" \
  -map "[m]" -ar 48000 -c:a pcm_s24le "$OUT/W10_M01_VO_TEMP_48k24.wav"
"$FF" -y -hide_banner -loglevel error \
 -i "$OUT/DX_CHILI_01_TEMP.aiff" -i "$OUT/DX_DK_01_TEMP.aiff" -i "$OUT/DX_CHILI_02_TEMP.aiff" -i "$OUT/DX_DK_02_TEMP.aiff" \
 -filter_complex "[0:a]aresample=48000,adelay=10500:all=1[c1];[1:a]aresample=48000,adelay=15300:all=1[d1];[2:a]aresample=48000,adelay=36500:all=1[c2];[3:a]aresample=48000,adelay=39400:all=1[d2];[c1][d1][c2][d2]amix=inputs=4:duration=longest:normalize=0,apad,atrim=0:42[m]" \
 -map "[m]" -ar 48000 -c:a pcm_s24le "$OUT/W10_M01_DX_TEMP_48k24.wav"

"$FF" -y -hide_banner -loglevel error -i "$OUT/W10_M01_stunt_previs_silent.mp4" \
  -i "$OUT/W10_M01_DX_TEMP_48k24.wav" \
  -i "$OUT/W10_M01_VO_TEMP_48k24.wav" \
  -i "$OUT/W10_M01_FX_48k24.wav" \
  -i "$OUT/W10_M01_AMB_48k24.wav" \
  -i "$OUT/W10_M01_MX_48k24.wav" \
  -filter_complex "[1:a]volume=0.88[dx];[2:a]volume=0.9[vo];[3:a]volume=0.8[fx];[4:a]volume=0.74[amb];[5:a]volume=0.65[mx];[dx][vo][fx][amb][mx]amix=inputs=5:duration=first:normalize=0,alimiter=limit=0.90[a]" \
  -map 0:v:0 -map "[a]" -t 42 -c:v copy -c:a aac -ar 48000 -b:a 192k -movflags +faststart \
  "$OUT/W10_M01_Rodeo_Blocking_Proof_with_TEMP_DX.mp4"

"$FF" -y -hide_banner -loglevel error -ss 22 -i "$OUT/W10_M01_Rodeo_Blocking_Proof_with_TEMP_DX.mp4" -frames:v 1 "$OUT/FRAME_22S_QA.png"
echo "SUCCESS: 42s MP4 + 5 separate 48kHz/24-bit WAV mix buses (DX/VO/FX/AMB/MX)."
ls -lh "$OUT"/*_48k24.wav "$OUT/W10_M01_Rodeo_Blocking_Proof_with_TEMP_DX.mp4" | tail -7
