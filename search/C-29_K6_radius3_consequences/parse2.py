import re,sys,json
T='../A-3-eager-fermat/tables/2_tables.txt'
txt=open(T,encoding='utf-8',errors='replace').read().split('\n')
tok=re.compile(r'(?:(?<=\s)[a-z] )?(\d+)(?:�(\d+))?(?: [a-z])?(?=\s|$)')
cur=None;rows={}
for ln in txt:
    m=re.match(r'^\s*Bounds on K\(n, R\), R = ([\d, ]+)',ln.strip() and ln) if 'Bounds on' in ln else None
    if 'Bounds on K(n, R)' in ln:
        cur=[int(x) for x in re.findall(r'\d+',ln.split('R =')[1])]; continue
    m=re.match(r'^(\d+)\s+(.*)$',ln)
    if m and cur:
        n=int(m.group(1)); rest=m.group(2)
        cells=[]
        for t in tok.finditer(' '+rest):
            lo=int(t.group(1)); hi=int(t.group(2)) if t.group(2) else None
            cells.append((lo,hi))
        rows[(tuple(cur),n)]=cells
if __name__=='__main__':
    for k,v in rows.items():
        if k[1]>=10: print(k,len(v),v)
