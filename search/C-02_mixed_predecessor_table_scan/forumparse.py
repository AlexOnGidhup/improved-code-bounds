import re,html,sys
def blocks(path):
    s=open(path,encoding='utf-8',errors='replace').read()
    t=html.unescape(re.sub(r'<br\s*/?>','\n',s))
    t=re.sub(r'<[^>]+>',' ',t)
    out=[];cur=[];title=None;last=''
    for line in t.split('\n'):
        l=line.strip()
        if re.fullmatch(r'[12Xx]{6,16}',l) or re.fullmatch(r'[012]{6,16}',l):
            if not cur: title=last
            cur.append(l.upper())
        else:
            if cur and l=='' : continue
            if cur:
                out.append((title,cur));cur=[]
            if l: last=l
    if cur: out.append((title,cur))
    return out
if __name__=='__main__':
    for title,b in blocks(sys.argv[1]):
        print(repr(title[:80]),len(b),len(b[0]),b[0])
