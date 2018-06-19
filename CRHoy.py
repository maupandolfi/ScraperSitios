import bs4
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from xml.etree import ElementTree
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, Comment

import datetime
import json
import os


def get_simple(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if revisar_respuesta(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def revisar_respuesta(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and ( content_type.find('html') > -1 or content_type.find('json') > -1 ) )


def log_error(e):
    print(e)


def obtenerPortada():

    obj = datetime.datetime.now()

    anno = obj.year

    r_dia = obj.day
    if r_dia < 10 :
        dia = "0" + str(r_dia)
    else:
        dia = str(r_dia)

    r_mes = obj.month
    if r_mes < 10 :
        mes = "0" + str(r_mes)
    else:
        mes = str(r_mes)

    r_hora = obj.hour
    if r_hora < 10:
        hora = "0" + str(r_hora)
    else:
        hora = str(r_hora)

    r_min = obj.minute
    if r_min < 10:
        min = "0" + str(r_min)
    else:
        min = str(r_min)

    nombre_carpeta = str(anno) + "-" + mes + "-" +dia + "__" + hora + "-" + min

    crearCarpeta(nombre_carpeta)

    codigo_servicio = str(anno) + str(r_mes-1) + str(r_dia)

    info = get_simple("https://www.crhoy.com/site/dist/json/index2.json?v=" + codigo_servicio)

    obtenerPlanos (info, "")

def crearCarpeta (nom) :
    if not os.path.exists(nom):
        os.makedirs(nom)
        os.makedirs(nom+"/CRHOY.COM")
    elif not os.path.exists(nom+"/CRHOY.COM"):
        os.makedirs(nom + "/CRHOY.COM")
    os.chdir(nom + "/CRHOY.COM")


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def obtenerPlanos (cont, ruta) :

    j = json.loads(cont)
    archivo_txt = ""
    links = []

    for x in range (0,4) :
        links.append(j['slider'][x]['url'])
    links.append(j['visualB'][0]['url'])

    indice = 1

    for x in links :

        link = x
        info1 = get_simple(link)
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
        nombre = "top" + str(indice) + "__" + titulo.replace(":", ",").replace("?", "¿")

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
        cat = SubElement(archivo_xml, 'categoria')
        cat.text = clasificacion.getText().replace("\n", "")

        # Tags
        div_tags = sou.find('div', attrs={'class': 'etiquetas'})
        tags = div_tags.find_all('a')
        for tag in tags :
            tag_xml = SubElement(archivo_xml, 'etiqueta')
            tag_xml.text = tag.getText()

        #Codificacion
        archivo_txt = archivo_txt.encode('iso-8859-1', 'ignore').decode('iso-8859-1', 'ignore')
        archivo_xml = prettify(archivo_xml).encode('iso-8859-1', 'ignore').decode('iso-8859-1', 'ignore')

        #Creacion de archivos
        hacerArchivo(ruta, archivo_txt, nombre, '.txt')
        hacerArchivo(ruta, archivo_xml, nombre, '.xml')

        indice = indice + 1


def hacerArchivo(ruta, info, nom, tipo):
    com = ruta + nom + tipo
    file = open(com, "w")
    file.write(info)
    file.close()


#obtenerPortadaCRHOY()

