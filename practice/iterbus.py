from xml.etree.cElementTree import iterparse

for event,elem in iterparse("allroutes.xml",('start','end')):
    if event == 'start' and elem.tag == 'buses':
        buses = elem
    elif event == 'end' and elem.tag == 'bus':
        busdict = dict((child.tag,child.text) 
                        for child in elem)
        if (busdict['route'] == '22' and 
            busdict['direction'] == 'North Bound'):
            print("{id},{route},\"{direction}\","\
                  "{latitude},{longitude}".format(**busdict))
        buses.remove(elem) 
