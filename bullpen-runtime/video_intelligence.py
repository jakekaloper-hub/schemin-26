#!/usr/bin/env python3
"""Evidence-first video ingestion. Optional yt-dlp; never claims to have watched frames."""
import argparse
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import urlparse, parse_qs

def video_id(url):
    p = urlparse(url)
    host = (p.hostname or "").lower()
    if host in {"youtu.be", "www.youtu.be"}:
        ident = p.path.strip("/")
    elif host in {"youtube.com", "www.youtube.com", "m.youtube.com"} and p.path == "/watch":
        ident = parse_qs(p.query).get("v", [""])[0]
    else:
        raise ValueError("Only standard YouTube video URLs are accepted")
    if not re.fullmatch(r"[A-Za-z0-9_-]{11}", ident):
        raise ValueError("Invalid YouTube video ID")
    return ident

def run(url, output, allow_media=False):
    ident = video_id(url)
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    source = "https://www.youtube.com/watch?v=" + ident
    cmd = ["yt-dlp", "--no-playlist", "--skip-download", "--write-info-json",
           "--write-auto-subs", "--write-subs", "--sub-langs", "en.*",
           "--sub-format", "vtt", "-o", str(output / "%(id)s.%(ext)s"), source]
    subprocess.run(cmd, check=True, timeout=180)
    metadata_file = output / (ident + ".info.json")
    if not metadata_file.exists():
        raise RuntimeError("No metadata receipt")
    metadata = json.loads(metadata_file.read_text())
    receipt = {"video_id": ident, "source": source, "title": metadata.get("title"),
               "duration_seconds": metadata.get("duration"), "status": "METADATA_ONLY",
               "transcript_files": sorted(p.name for p in output.glob(ident + "*.vtt")),
               "visual_review": "NOT_PERFORMED", "director_review": "NOT_PERFORMED"}
    if receipt["transcript_files"]:
        receipt["status"] = "CAPTIONS_RETRIEVED"
    if allow_media:
        subprocess.run(["yt-dlp", "--no-playlist", "-f", "bv*+ba/b", "-o",
                        str(output / "%(id)s.%(ext)s"), source], check=True, timeout=900)
        receipt["media_files"] = sorted(p.name for p in output.glob(ident + ".*")
                                        if p.suffix not in {".json", ".vtt"})
        receipt["status"] = "MEDIA_RETRIEVED" if receipt["media_files"] else receipt["status"]
    (output / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    return receipt

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--output", default="video-intelligence-output")
    parser.add_argument("--allow-media", action="store_true",
                        help="Only for media you are authorized to retrieve")
    args = parser.parse_args()
    print(json.dumps(run(args.url, args.output, args.allow_media), indent=2))
