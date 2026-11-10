"""Bounded correction discovered while reviewing the first generated draft.
Only adjusts the approval compiler's reader-text spacing and Markdown ending.
It never changes sports observations, canonical references, approval or scores.
"""
from pathlib import Path

HERE=Path(__file__).resolve().parent
p=HERE/'build_approval_folios.py'
s=p.read_text()
old="""    def readable(s):
        s=re.sub(r'(?<=[A-Za-z])(?=\\d)', ' ',s)
        s=re.sub(r'(?<=\\d)(?=[A-Za-z])', ' ',s)
        return s.replace('Week 9','Week 9').replace('Week 10','Week 10')
"""
new="""    def readable(s):
        # Canonical team names with digits are not typography mistakes.
        protected='CANONICALDONKEYALIAS'
        s=s.replace('D0nkey K0ng',protected)
        s=re.sub(r'(?<=[A-Za-z])(?=\\d)', ' ',s)
        s=re.sub(r'(?<=\\d)(?=[A-Za-z])', ' ',s)
        s=re.sub(r'%(?=[A-Za-z])', '% ',s)
        return s.replace(protected,'D0nkey K0ng')
"""
if old in s:
    s=s.replace(old,new,1)
elif new not in s:
    raise ValueError('Unexpected text-normalization implementation; no blind replacement')
s=s.replace("write_text('\\n'.join(md)+'\\n')", "write_text('\\n'.join(md).rstrip()+'\\n')")
p.write_text(s)
print('Preserved D0nkey K0ng alias and removed extra Markdown EOF blank line.')
