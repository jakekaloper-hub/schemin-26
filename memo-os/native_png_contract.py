"""Forward-only native weekly memo PNG dimension gate. Structural, not semantic QA."""
from pathlib import Path
import struct
import zlib

WIDTH, HEIGHT = 1080, 1920
SIGNATURE = b"\x89PNG\r\n\x1a\n"

class NativePNGError(ValueError):
    pass

def validate_png(path):
    data = Path(path).read_bytes()
    if not data.startswith(SIGNATURE):
        raise NativePNGError("NOT_PNG")
    offset = 8
    seen_ihdr = seen_idat = seen_iend = False
    dimensions = None
    while offset + 12 <= len(data):
        length = struct.unpack_from(">I", data, offset)[0]
        kind = data[offset + 4:offset + 8]
        end = offset + 12 + length
        if end > len(data):
            raise NativePNGError("TRUNCATED_PNG")
        chunk = data[offset + 8:offset + 8 + length]
        crc = struct.unpack_from(">I", data, offset + 8 + length)[0]
        if zlib.crc32(kind + chunk) & 0xffffffff != crc:
            raise NativePNGError("PNG_CRC_MISMATCH")
        if kind == b"IHDR":
            if seen_ihdr or offset != 8 or length != 13:
                raise NativePNGError("INVALID_IHDR")
            seen_ihdr = True
            dimensions = struct.unpack_from(">II", chunk)
            if dimensions != (WIDTH, HEIGHT):
                raise NativePNGError(f"WRONG_NATIVE_DIMENSIONS:{dimensions[0]}x{dimensions[1]}")
        elif kind == b"IDAT":
            seen_idat = True
        elif kind == b"IEND":
            if length != 0 or end != len(data):
                raise NativePNGError("INVALID_IEND_OR_TRAILING_DATA")
            seen_iend = True
            break
        offset = end
    if not (seen_ihdr and seen_idat and seen_iend):
        raise NativePNGError("INCOMPLETE_PNG")
    return {"format": "PNG", "width": WIDTH, "height": HEIGHT, "aspect_ratio": "9:16",
            "status": "STRUCTURAL_PASS_VISUAL_QA_REQUIRED"}

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("png")
    args = parser.parse_args()
    try:
        print(validate_png(args.png))
    except (NativePNGError, OSError) as error:
        parser.exit(2, f"BLOCKED: {error}\n")
