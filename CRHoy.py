import bs4
import Herramientas

from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement, Comment

import json

def obtenerPortada(directorio):

    codigo = Herramientas.obtenerCodigoTiempo ()
    Herramientas.crearCarpeta(directorio, codigo, "CRHOY.COM")

    datos = codigo.split("-")
    datos2 = datos[2].split("__")[0]
    codigo_servicio = datos[0] + str(int(datos[1])-1) + datos2

    info = Herramientas.get_simple("https://www.crhoy.com/site/dist/json/index2.json?v=" + codigo_servicio)

    j = json.loads(info)
    archivo_txt = ""
    links = []

    for x in range (0,4) :
        links.append(j['slider'][x]['url'])

    for x in range(0,3):
        links.append(j['visualB'][x]['url'])

    for x in range(0,3):
        links.append(j['visualA'][x]['url'])

    for x in range(0,3):
        links.append(j['visualC'][x]['url'])

    indice = 1

    for x in links :

        link = x
        info1 = Herramientas.get_simple(link)
        sou = BeautifulSoup(info1, 'html.parser')

        archivo_xml = Element('nota')
        archivo_txt = ""

        # Pre-titulo
        pre_titulo = sou.find('h3', attrs={'class': 'pre-titulo'}).getText().replace("\n", "")
        if (len(pre_titulo) != 0) :
            archivo_txt = pre_titulo + "\n"
            pretit = SubElement(archivo_xml, 'pre_titulo')
            pretit.text = pre_titulo

        # Titulo
        titulo = sou.find('title').getText()
        archivo_txt = archivo_txt + titulo + "\n"
        tit = SubElement(archivo_xml, 'titulo')
        tit.text = titulo
        nombre = "top" + str(indice) + "__" + titulo.replace(":", ",").replace("?", "¿").replace("\"", "")

        # Bajada
        bajadas = sou.find_all('li', attrs={'class': 'bajadita'})
        if len(bajadas) != 0 :
            baj = SubElement(archivo_xml, 'bajada')
            for i in bajadas:
                baj2 = SubElement(baj, 'b')
                baj2.text = i.getText().replace("\n", "")
                archivo_txt = archivo_txt + i.getText() + "\n"

        # Parrafos
        contenidos = sou.find('div', attrs={'class': 'contenido'})

        texto = SubElement(archivo_xml, 'texto')

        aux = contenidos.find_all( ['p', 'h2', 'h1'] , attrs={'class':None})
        es_lead = True

        for p in aux:
            if p.name == 'p' :
                ha_habido_resaltado = False
                ul_resaltado = None

                if not ( p.parent is not None and p.parent.parent is not None and p.parent.parent.parent is not None and (p.parent.parent.parent)['class'][0] == 'leerMasOuter' ):
                    hijos_div = p.find_all('div')
                    hijos_span = p.find_all('span')
                    if len(hijos_div)+len(hijos_span) == 0 :
                        if (es_lead):
                            parr = Element('lead')
                            es_lead = False
                        else:
                            parr = Element('parrafo')
                        parr.text = ""
                        lista = list(p.contents)
                        parrafo = ""
                        for p2 in lista :
                            if type(p2) is bs4.element.NavigableString :
                                parrafo = parrafo + p2
                                if ha_habido_resaltado:
                                    ul_resaltado.tail = ul_resaltado.tail + p2
                                else :
                                    parr.text = parr.text + p2
                            else:
                                ul_resaltado = SubElement(parr, 'resaltado')
                                ul_resaltado.text = p2.getText()
                                ha_habido_resaltado = True
                                ul_resaltado.tail = ""
                                parrafo = parrafo + p2.getText()
                        texto.append(parr)
                        archivo_txt = archivo_txt + parrafo + "\n"
            else :
                if p.name == 'h2' or p.name == 'h1' :
                    archivo_txt = archivo_txt + p.getText() + "\n"
                    subtit = SubElement(texto, 'subtitulo')
                    subtit.text = p.getText()

        # Categoría
        clasificacion = sou.find('h3', attrs={'class': 'breadcrumbs'})
        if clasificacion :
            cat = SubElement(archivo_xml, 'categoria')
            cat.text = clasificacion.getText().replace("\n", "")

        # Tags
        div_tags = sou.find('div', attrs={'class': 'etiquetas'})
        if div_tags :
            tags = div_tags.find_all('a')
            for tag in tags :
                tag_xml = SubElement(archivo_xml, 'etiqueta')
                tag_xml.text = tag.getText()

        #Codificacion
        archivo_txt = archivo_txt.encode('iso-8859-1', 'ignore').decode('iso-8859-1', 'ignore').replace('&quot;', '')
        archivo_xml = Herramientas.prettify(archivo_xml).encode('iso-8859-1', 'ignore').decode('iso-8859-1', 'ignore').replace('&quot;', '\"')

        # Creacion de archivos
        Herramientas.hacerArchivo( archivo_txt, nombre, '.txt')
        Herramientas.hacerArchivo( archivo_xml, nombre, '.xml')

        indice = indice + 1


