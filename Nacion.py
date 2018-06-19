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

    info = get_simple("https://www.nacion.com")

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
    portada  = (homePage.find_all('div', attrs= {'class': 'pb-c-default-chain'}))
    noticias_portada = []

    for n in portada :
        noticias_portada = noticias_portada + n.find_all('div', attrs={'class': 'pb-f-homepage-story'})

    for x in range (0,5) :
        div_con_la_noticia = noticias_portada[x]
        div_con_link = div_con_la_noticia.find('div', attrs={'class' : 'headline'})
        links.append("https://www.nacion.com" + div_con_link.a['href'])

    indice = 1

    for x in links:
        link = x
        info1 = get_simple(link)
        sou = BeautifulSoup(info1, 'html.parser')

        archivo_xml = Element('nota')
        archivo_txt = ""

        # Titulo
        titulo = (sou.find('div', attrs= {'class', 'headline-hed-last'})).getText()
        archivo_txt = archivo_txt + titulo + "\n"
        tit = SubElement(archivo_xml, 'titulo')
        tit.text = titulo
        nombre = "top" + str(indice) + "__" + titulo.replace(":", ",").replace("?", "¿")

        # Bajada
        bajada = sou.find('p', attrs={'class': 'subheadline'})
        baj = SubElement(archivo_xml, 'bajada')
        baj.text = bajada.getText().replace("\n", "")
        archivo_txt = archivo_txt + bajada.getText() + "\n"

        # Parrafos
        contenidos = sou.find('div', attrs={'id': 'article-content'})

        texto = SubElement(archivo_xml, 'texto')

        aux = contenidos.find_all(['p', 'span'], attrs={'class': 'element'})

        es_lead = True

        for p in aux:
            if p.name == 'p':
                if (es_lead):
                    parr = SubElement(texto, 'lead')
                    parr.text = p.getText()
                    es_lead = False
                else:
                    parr = SubElement(texto, 'parrafo')
                    if (p.find('b') is None) :
                        parr.text = p.getText()
                    else :
                        resal = SubElement(parr, 'resaltado')
                        resal.text = p.getText()
            else:
                if p.name == 'span':
                    subtit = SubElement(texto, 'subtitulo')
                    subtit.text = p.getText()
            archivo_txt = archivo_txt + p.getText() + "\n"


        # Tags
        div_tags = sou.find('div', attrs={'class': 'etiqueta'})
        tags = div_tags.find_all('a')
        for tag in tags :
            tag_xml = SubElement(archivo_xml, 'etiqueta')
            tag_xml.text = tag.getText()

        # Categoría
        clasificacion = (sou.find('div', attrs={'class': 'headline-seccion'})).a
        cat = SubElement(archivo_xml, 'categoria')
        cat.text = clasificacion.getText().replace("\n", "")

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
        os.makedirs(nom+"/NACION.COM")
    elif not os.path.exists(nom+"/NACION.COM"):
        os.makedirs(nom + "/NACION.COM")
    os.chdir(nom + "/NACION.COM")


def hacerArchivo(ruta, info, nom, tipo):
    com = ruta + nom + tipo
    file = open(com, "w")
    file.write(info)
    file.close()

#obtenerPortadaNacion()

