import pandas as pd
import rdflib
from rdflib import URIRef, Graph, Namespace
from rdflib.plugins.parsers.notation3 import N3Parser
import xml.etree.ElementTree as et
from xml.dom import minidom

g = Graph()
result = g.parse(file=open("twitter_example.txt", "r"), format="n3")
xml_result = g.serialize(format='xml')
print(xml_result)
print('\n')

print("graph has %s statements." % len(g))
print('\n')

root = et.fromstring(xml_result)
print(root)
print(root.tag)
print(root.attrib)
print('\n')
for child in root:
    print(child.tag, child.attrib)
print('\n')

for child in root:
    for element in child:
        print('TAG: ', element.tag, '||', 'ATTR: ', element.attrib)

'''
output = minidom.parseString(xml_result)
print(output)
#print('\n')

rdf = output.getElementsByTagName('rdf:RDF')   #nodelist object
print(rdf)
print(len(rdf))
print('\n')

descriptions = output.getElementsByTagName('rdf:Description')  #nodelist object
print(descriptions)
print(len(descriptions))
print('\n')

for Description in descriptions:   #Descriptions is a element object
    nodeID = Description.getAttribute('rdf:nodeID')   
    print('NODE-ID: '+nodeID)
print(len(nodeID))
print('\n')

types = output.getElementsByTagName('rdf:type')  #nodelist object
print(types)
print(len(types))
print('\n')

for type in types:   #type is a element object
    resource = type.getAttribute('rdf:resource')
    print('RESOURCE: '+resource)
print(len(resource))
'''