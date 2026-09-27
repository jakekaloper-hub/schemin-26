# PROLOGUE PRODUCTION RUN — ASSEMBLY RECORD

**Status:** ASSEMBLED PRODUCTION v1
**Date:** 2026-09-27
**Operational lead:** Bullpen / Closer
**Format:** 16 facing spreads representing 32 book pages

## Assembly
The Prologue has been assembled from the sixteen individual paired-spread assets in the production workspace:

- spread_01_p01-p02.png
- spread_02_p03-p04.png
- spread_03_p05-p06.png
- spread_04_p07-p08.png
- spread_05_p09-p10.png
- spread_06_p11-p12.png
- spread_07_p13-p14.png
- spread_08_p15-p16.png
- spread_09_p17-p18.png
- spread_10_p19-p20.png
- spread_11_p21-p22.png
- spread_12_p23-p24.png
- spread_13_p25-p26.png
- spread_14_p27-p28.png
- spread_15_p29-p30.png
- spread_16_p31-p32.png

Final assembled artifact:
`SCHEMIN_CHRONICLE_VOLUME_I_2026_PROLOGUE.pdf`

Archive bundle:
`SCHEMIN_CHRONICLE_VOLUME_I_2026_PROLOGUE_ARCHIVE.zip`

## Production doctrine applied
Librarian Source Packet -> Architect -> Umpire Preflight -> Clean Art -> Character QA -> Literary Typesetting -> Critic -> Final Umpire -> Render QA -> Closer -> Lock -> next spread.

## Important archival note
The GitHub connector available in this production surface supports UTF-8 repository files and Git blobs, but does not expose a practical binary-file upload path for multi-megabyte local generated images without transferring their base64 through the model context. The exact spread binaries therefore remain in the generated archive bundle for user download, while this repository stores their production record and filenames. Do not falsely mark binary GitHub archival complete until the binary sync is performed through a suitable file-capable Git/GitHub environment.

## PDF preflight
- 16 PDF pages / 16 facing spreads / 32 represented book pages.
- openable by PyMuPDF;
- not encrypted;
- image-led illustrated-book PDF by design.

## Next QA doctrine
Any later correction to a spread must:
1. preserve its spread filename;
2. update its SHA-256 manifest;
3. rerun spread QA;
4. rebuild PDF;
5. rerun whole-book preflight.
