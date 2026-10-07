"""04 — Merge sort (von Neumann 1945) vs insertion sort. Comparison-counted."""
def merge_count(a,b,ctr):
    i=j=0; out=[]
    while i<len(a) and j<len(b):
        ctr[0]+=1
        if a[i]<=b[j]: out.append(a[i]); i+=1
        else: out.append(b[j]); j+=1
    out.extend(a[i:]); out.extend(b[j:])
    return out

def mergesort(xs,ctr=None):
    if ctr is None: ctr=[0]
    if len(xs)<=1: return list(xs)
    m=len(xs)//2
    L=mergesort(xs[:m],ctr); R=mergesort(xs[m:],ctr)
    return merge_count(L,R,ctr)

def insertionsort(xs,ctr=None):
    if ctr is None: ctr=[0]
    a=list(xs)
    for i in range(1,len(a)):
        j=i
        while j>0:
            ctr[0]+=1
            if a[j]<a[j-1]: a[j],a[j-1]=a[j-1],a[j]; j-=1
            else: break
    return a
