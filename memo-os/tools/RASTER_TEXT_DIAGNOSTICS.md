# Raster text diagnostic

`python memo-os/tools/compare_editorial_raster_text.py page.png page.receipt.json diagnostic.json`

Requires Pillow, local Tesseract OCR with English language data (`tesseract-ocr`, `tesseract-ocr-eng` on Ubuntu). CI installs these and runs an actual pixel extraction positive/mismatch regression; the real OCR test explicitly skips when the executable is unavailable locally. Test fixtures also require DejaVu Sans.

The PNG must match the compositor receipt hash. Each declared region is cropped from immutable decoded PNG bytes, observed using Tesseract, and compared to the receipt's rendered line commands. Only one terminal OCR linefeed is removed; whitespace, case, punctuation and Unicode remain exact. Exit0 means every declared region matched; exit1 means a comparison mismatch. Missing tools/failed extraction raise an error, never a successful observation.

The output binds PNG and render-receipt hashes, crop hashes, OCR version/configuration, observed text and comparison differences. This is a diagnostic against render commands, not an approved manuscript, complete page coverage, OCR accuracy certification, PDF render-back comparison, independent visual judgment, mobile review or publication approval. Blank/omitted regions and false upstream copy remain outside this check. No editorial normalization policy is invented and no acceptance state is promoted.
