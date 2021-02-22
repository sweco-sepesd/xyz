import os.path
import csv
import json
script_dir = os.path.dirname(__file__)

def avstand(fp = os.path.join(script_dir,'avstand.csv')):
    with open(fp) as cin:
        reader = csv.reader(cin, delimiter = ' ')
        return [(t1, t2, float(dist)) for (i, (t1,t2,dist)) in enumerate(reader) if i]

def objekt(fp = os.path.join(script_dir,'objekt.csv')):
    with open(fp) as cin:
        reader = csv.reader(cin, delimiter = ' ')
        return {id:(float(dia), beskr) for (i, (id,dia,beskr)) in enumerate(reader) if i}

def normalized():
    d = avstand()
    o = objekt()
    for t1,t2,dist in sorted(d, key=lambda x:x[0]+'.'+x[1]):
        d1 = o[t1][0]
        d2 = o[t2][0]
        normalized = round(dist + (d1 + d2) / 2, 1)
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

if __name__ == '__main__':
    import sys
    command = sys.argv[1]
    if '-o' == command:
        outgoing(sys.argv[2])
    elif '-json' == command:
        outgoing = [t1 for t1,t2,d in normalized()]
        incoming = [t2 for t1,t2,d in normalized()]
        #ids = set(*outgoing, *incoming)
        ids = set(outgoing) | set(incoming)
        counts = {id: outgoing.count(id) + incoming.count(id) for id in ids}
        filtered = [
            (k,(dia,desc)) 
            for k,(dia,desc) 
            in objekt().items()
            if k in counts and counts[k] > 2
            ]
        nodes = {
            k : {'id': k, 'index': i, 'radius': dia/2, 'label': desc}
            for i,(k,(dia,desc))
            in enumerate(filtered)
        }
        links = [
            {'source': nodes[t1]['index'], 'target': nodes[t2]['index'], 'distance': normalized, 'label': '{}-{}'.format(t1,t2)}
            for t1,t2,normalized
            in normalized()
            if t1 in nodes and t2 in nodes
        ]


        data = {
            'nodes': nodes.values()
            , 'links': links
        }
        #dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, encoding='utf-8', default=None, sort_keys=False, **kw)
        #print(json.dumps(data, indent=4,  ensure_ascii=False))
        print(json.dumps(data, separators=(',',':'),  ensure_ascii=False))