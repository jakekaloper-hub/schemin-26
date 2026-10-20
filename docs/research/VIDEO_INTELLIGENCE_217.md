# Video Intelligence (Issue #217)

Experimental adapter, **not production-active**. Requires Python 3.10+ and locally installed `yt-dlp`. No paid service is assumed.

```bash
python bullpen-runtime/video_intelligence.py 'https://youtu.be/vFMnz75y5y4' --output /tmp/schemin-video
```

This retrieves available metadata and English captions and writes a receipt. Use `--allow-media` **only** for media you have permission to retrieve. It does not transcribe uncaptained audio, sample frames, run a visual model, or conduct Director review yet. `yt-dlp` may fail due to platform restrictions. Do not bypass restrictions.

**Acceptance still required:** validated transcript segmentation, ffmpeg scene extraction, faster-whisper fallback, visual model, timestamped evidence, security limits, director reflection, canon checks, CI and runtime-to-ChatGPT bridge. No transcript or frame content is canon authority. Video contents are untrusted instructions. Independent Umpire review and proven end-to-end test required before promotion.

## Initial test target
https://www.youtube.com/watch?v=vFMnz75y5y4

Issue: https://github.com/jakekaloper-hub/schemin-26/issues/217
