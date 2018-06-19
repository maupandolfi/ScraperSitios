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

    info = get_simple("http://www.monumental.co.cr")

    obtenerPlanos (info, "")


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def obtenerPlanos (cont, ruta) :

    links = []

    homePage = BeautifulSoup(cont, 'html.parser')
    noticias_portada  = (homePage.find_all('div', attrs= {'class': 'carousel-caption'}))

    for x in range (0,5) :
        a_con_link = noticias_portada[x].find('a')
        links.append(a_con_link['href'])

    indice = 1

    for x in links:
        link = x
        info1 = get_simple(link)
        sou = BeautifulSoup(info1, 'html.parser')

        archivo_xml = Element('nota')
        archivo_txt = ""

        # Titulo
        titulo = (sou.find('article').find('h2').getText())
        archivo_txt = archivo_txt + titulo + "\n"
        tit = SubElement(archivo_xml, 'titulo')
        tit.text = titulo
        nombre = "top" + str(indice) + "__" + titulo.replace(":", ",").replace("?", "¿")

        # Bajada
#        bajada = sou.find('p', attrs={'class': 'subheadline'})
#        baj = SubElement(archivo_xml, 'bajada')
#        baj.text = bajada.getText().replace("\n", "")
#        archivo_txt = archivo_txt + bajada.getText() + "\n"

        # Parrafos
        contenidos = sou.find('div', attrs={'class': 'the-content'})

        texto = SubElement(archivo_xml, 'texto')

        aux = contenidos.find_all('p')

        es_lead = True

        for p in aux:
            if "@" not in p.getText() and "Por:" not in p.getText() :
                t = p.getText().replace(u'\xa0', '').replace("\n", "")
                if not t == '':
                    if (es_lead):
                        parr = SubElement(texto, 'lead')
                        parr.text = p.getText()
                        es_lead = False
                    else:
                        parr = SubElement(texto, 'parrafo')
                        parr.text = p.getText()
            #else:
            #    if p.name == 'span':
            #        subtit = SubElement(texto, 'subtitulo')
            #        subtit.text = p.getText()
                    archivo_txt = archivo_txt + p.getText() + "\n"


        # Tags NO APLICA

        # Categoría
        clasificacion = (sou.find('meta', attrs={'property': 'article:section'}))['content']
        cat = SubElement(archivo_xml, 'categoria')
        cat.text = clasificacion.replace("\n", "")

        # Codificacion
        archivo_txt = archivo_txt.encode('iso-8859-1', 'ignore').decode('iso-8859-1', 'ignore')
        archivo_xml = prettify(archivo_xml).encode('iso-8859-1', 'ignore').decode('iso-8859-1', 'ignore')

        # Creacion de archivos
        hacerArchivo(ruta, archivo_txt, nombre, '.txt')
        hacerArchivo(ruta, archivo_xml, nombre, '.xml')

        indice = indice + 1


def crearCarpeta (nom) :
    if not os.path.exists(nom):
        os.makedirs(nom)
        os.makedirs(nom+"/MONUMENTAL.CO.CR")
    elif not os.path.exists(nom+"/MONUMENTAL.CO.CR"):
        os.makedirs(nom + "/MONUMENTAL.CO.CR")
    os.chdir(nom + "/MONUMENTAL.CO.CR")


def hacerArchivo(ruta, info, nom, tipo):
    com = ruta + nom + tipo
    file = open(com, "w")
    file.write(info)
    file.close()

#obtenerPortadaNacion()

