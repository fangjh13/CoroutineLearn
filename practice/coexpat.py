import xml.parsers.expat

def coroutine(func):
    def wrapper(*args, **kwargs):
        rs = func(*args, **kwargs)
        next(rs)
        return rs
    return wrapper


@coroutine
def buses_to_dicts(target):
    while True:
        event, value = yield
        if event == 'start' and value == 'bus':
            busdict = {}
            fragments = []
            while True:
                event, value = yield
                if event == 'start':
                    fragments = []
                elif event == 'text':
                    fragments.append(value)
                elif event == 'end':
                    if value != 'bus':
                        busdict[value] = ''.join(fragments)
                    else:
                        target.send(busdict)
                        break

@coroutine
def filter_on_field(filedname, value, target):
    while True:
        d = yield
        if d.get(filedname) == value:
            target.send(d)

@coroutine
def bus_locations():
    while True:
        d = yield
        print(repr(d))
        print("{route},{id},\"{direction}\",\
{latitude},{longitude}".format(**d))
        print()


def expat_parse(f, target):
    parser = xml.parsers.expat.ParserCreate()
    parser.buffer_size = 65536
    parser.buffer_text = True
    parser.StartElementHandler = \
        lambda name, attrs: target.send(('start', (name)))
    parser.EndElementHandler = \
        lambda name: target.send(('end', name))
    parser.CharacterDataHandler = \
        lambda data: target.send(('text', data))
    parser.ParseFile(f)

expat_parse(open('allroutes.xml', 'rb'), buses_to_dicts(
            filter_on_field('route', '22',
                filter_on_field('direction', 'North Bound',
                    bus_locations()))))