def pout(a, limit=5):
    if len(a) > limit:
        print(f'Rodoma {limit} eilutės iš {len(a)}')
    for k,i in enumerate(a):
        if k > limit:
            break
        l = []
        for k in i:
            f = f'{str(k):^18.18}'
            l.append(f)
        t = '|'+'|'.join(l)+'|'
    print(t)