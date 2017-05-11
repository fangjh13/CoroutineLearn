import xml.sax

def coroutine(func):
    def wrapper(*args, **kwargs):
        rs = func(*args, **kwargs)
        next(rs)
        return rs
    return wrapper


class EventHandler(xml.sax.ContentHandler):
    def __init__(self,target):
        self.target = target
    def startElement(self,name,attrs):
        self.target.send(('start', name))
    def characters(self,text):
        self.target.send(('text',text))
    def endElement(self,name):
        self.target.send(('end',name))


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


xml.sax.parse('allroutes.xml', EventHandler(
        buses_to_dicts(
            filter_on_field('route', '22',
                filter_on_field('direction', 'North Bound',
                    bus_locations())))))