from xml.etree import ElementTree
from xml.dom import minidom

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")




from xml.etree.ElementTree import Element, SubElement, Comment
#from ElementTree_pretty import prettify
nota = Element('nota')
comment = Comment('CRHOY.COM - 25-5-18')
nota.append(comment)

tit = SubElement(nota, 'titulo')
tit.text = 'EJEMPLO DE TITULO'

tex1 = SubElement(nota, 'texto')
tex1.text = 'EJEMPLO DE TEXTO 1'

hijo2 = Element('parrafo')

tex2 = SubElement(hijo2, 'negrita')
tex2.text = 'NEGROOO'
tex2.text = tex2.text + 'NEGROOO'

tex2 = SubElement(hijo2, 'negrita22222222222')
tex2.text = 'NEGROOO'
tex2.text = tex2.text + 'NEGROOO'

tex2.tail = 'cola 1'
tex2.tail = tex2.tail + 'cola 2'

tex3 = SubElement(hijo2, 'negrita')
tex3.text = 'NEGROOO'


nota.append(hijo2)
#nota.append('aaaaaaaaa')



tex3.tail = 'EJEMPLO DE TEXTO 1'


## tex1.text = 'EJEMPLO DE BAJADA 3'


#nota = Element('notalhlh')


#child_with_tail = SubElement(top, 'child_with_tail')
#child_with_tail.text = 'This child has regular text.'
#child_with_tail.tail = 'And "tail" text.'

#child_with_entity_ref = SubElement(top, 'child_with_entity_ref')
#child_with_entity_ref.text = 'This & that'

print ( prettify(nota) )
