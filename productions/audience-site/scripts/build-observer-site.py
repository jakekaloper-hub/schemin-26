#!/usr/bin/env python3
"""Build the existing audience site plus a PRIVATE observer entry; never deploy.

The public catalog retains its own authority. The observer is a separate derived
candidate in the same output directory, with private edition assets excluded.
"""
from pathlib import Path
import argparse
import importlib.util
import json
import re
import subprocess
import sys

SITE=Path(__file__).resolve().parents[1]
ROOT=SITE.parents[1]


def link_observer(html):
    link='<a href="observer.html" data-observer-preview="true">World preview</a>'
    if 'data-observer-preview="true"' in html:return html
    pattern=r'(<nav\b[^>]*\bid="navigation"[^>]*>)(.*?)(</nav>)'
    result,count=re.subn(pattern,lambda m:m[1]+m[2]+link+m[3],html,count=1,flags=re.S)
    if count!=1:raise ValueError('AUDIENCE_NAVIGATION_NOT_FOUND')
    return result


def build(output):
    output=Path(output).resolve()
    subprocess.run([sys.executable,str(SITE/'build_public_catalog.py'),'--output',str(output),'--no-render'],cwd=ROOT,check=True)
    source=output/'observer-candidate.json'
    subprocess.run(['node',str(SITE/'scripts/build-observer-catalog.mjs'),str(source)],cwd=ROOT,check=True)
    spec=importlib.util.spec_from_file_location('observer_build',SITE/'preview/build_preview.py')
    compiler=importlib.util.module_from_spec(spec);spec.loader.exec_module(compiler)
    receipt=compiler.build(source,output/'observer.html',no_editions=True)
    index=output/'index.html';index.write_text(link_observer(index.read_text()))
    (output/'observer-build-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    return receipt

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True,help='Private preview output; not a deployment destination')
    args=parser.parse_args();print(json.dumps(build(args.output),indent=2))
