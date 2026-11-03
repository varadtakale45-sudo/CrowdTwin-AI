def linear_search(items, target):
    return next((i for i, v in enumerate(items) if v == target), -1)


def binary_search(items, target):
    lo, hi = 0, len(items)-1
    while lo <= hi:
        mid = (lo+hi)//2
        if items[mid] == target: return mid
        if items[mid] < target: lo = mid+1
        else: hi = mid-1
    return -1


def fibonacci_search(items, target):
    a, b = 0, 1
    while b < len(items): a, b = b, a+b
    offset = -1
    while b > 1:
        i = min(offset+a, len(items)-1)
        if items[i] < target: b, a, offset = a, b-a, i
        elif items[i] > target: b, a = b-a, a-(b-a)
        else: return i
    return offset+1 if a and offset+1 < len(items) and items[offset+1] == target else -1


def merge_sort(a):
    if len(a) < 2: return a[:]
    m = len(a)//2; left, right = merge_sort(a[:m]), merge_sort(a[m:]); out=[]
    while left and right: out.append(left.pop(0) if left[0] <= right[0] else right.pop(0))
    return out+left+right


def quick_sort(a):
    if len(a) < 2: return a[:]
    p=a[len(a)//2]; return quick_sort([x for x in a if x<p])+[x for x in a if x==p]+quick_sort([x for x in a if x>p])


def heap_sort(a):
    import heapq
    h=a[:]; heapq.heapify(h); return [heapq.heappop(h) for _ in range(len(h))]


def bucket_sort(a):
    if not a: return []
    lo, hi=min(a), max(a); buckets=[[] for _ in range(10)]; span=max(1,hi-lo+1)
    for x in a: buckets[min(9,(x-lo)*10//span)].append(x)
    return [x for b in buckets for x in sorted(b)]


def radix_sort(a):
    out=a[:]; exp=1
    while out and max(out)//exp:
        buckets=[[] for _ in range(10)]
        for x in out: buckets[(x//exp)%10].append(x)
        out=[x for b in buckets for x in b]; exp*=10
    return out


def benchmark(values):
    import time
    results={}
    for fn in (merge_sort, quick_sort, heap_sort, bucket_sort, radix_sort):
        started=time.perf_counter(); valid=fn(values)==sorted(values); results[fn.__name__]={"ms":round((time.perf_counter()-started)*1000,4),"valid":valid}
    return results

