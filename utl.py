import os.path
import csv
import json
script_dir = os.path.dirname(__file__)

def avstand(fp = os.path.join(script_dir,'avstand.csv')):
    with open(fp, encoding='utf8') as cin:
        reader = csv.reader(cin, delimiter = ' ')
        return [(t1, t2, float(dist)) for (i, (t1,t2,dist)) in enumerate(reader) if i]

def objekt(fp = os.path.join(script_dir,'objekt.csv')):
    with open(fp, encoding='utf8') as cin:
        reader = csv.reader(cin, delimiter = ' ')
        return {id:{'r':float(dia)/2, 'd': beskr, **xy_or_empty(fx, fy)} for (i, (id,dia,beskr,fx,fy)) in enumerate(reader) if i}
def xy_or_empty(x,y):
    if x and len(x) and y and len(y):
        return {'fx': float(x), 'fy': float(y), 'x': float(x), 'y': float(y)}
    return {}
def normalized():
    d = avstand()
    o = objekt()
    for t1,t2,dist in sorted(d, key=lambda x:x[0]+'.'+x[1]):
        r1 = o[t1]['r']
        r2 = o[t2]['r']
        normalized = dist + r1 + r2
        yield t1,t2,normalized

def outgoing(id='B'):
    o = objekt()[id]
    print('{} ({})'.format(o[1],id))
    d = normalized()
    for t1,t2,dist in d:
        if not id in (t1,t2): continue
        if t1 == id:
            print(t1, t2, dist)
        else:
            print(t2, t1, dist)
def to_d3_json():
    has_xy = set([k for k,o in objekt().items() if o.get('x')])
    #print(has_xy)
    outgoing = [t1 for t1,t2,d in normalized() if t1 in has_xy or t2 in has_xy]
    incoming = [t2 for t1,t2,d in normalized() if t1 in has_xy or t2 in has_xy]
    #ids = set(*outgoing, *incoming)
    ids = set(outgoing) | set(incoming)
    counts = {id: outgoing.count(id) + incoming.count(id) for id in ids}
    filtered = [
        (k,v) 
        for k,v 
        in objekt().items()
        if k in counts and counts[k] > 1
        ]
    nodes = {
        k : {'id': k, 'index': i, **v}
        for i,(k,v)
        in enumerate(filtered)
    }
    links = [
        {'source': nodes[t1]['index'], 'target': nodes[t2]['index'], 'distance': normalized, 'label': '{}-{}'.format(t1,t2)}
        for t1,t2,normalized
        in normalized()
        if t1 in nodes and t2 in nodes
    ]


    return {
        'nodes': list(nodes.values())
        , 'links': links
    }
if __name__ == '__main__':
    import sys
    command = sys.argv[1]
    if '-o' == command:
        outgoing(sys.argv[2])
    elif '-json' == command:
        #dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, encoding='utf-8', default=None, sort_keys=False, **kw)
        #print(json.dumps(data, indent=4,  ensure_ascii=False))
        data = to_d3_json()
        print(json.dumps(data, separators=(',',':'),  ensure_ascii=False))