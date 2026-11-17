#!/usr/bin/env python3
"""Run from repository root; no third-party packages or private cookies required."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent/'src'))
from playoff_context.pipeline import main

if __name__ == '__main__':
    main()
