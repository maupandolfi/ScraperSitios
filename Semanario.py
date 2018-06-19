import Herramientas
from bs4 import BeautifulSoup
from xml.etree import ElementTree
from xml.dom import minidom

import datetime
import json
import os

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

    info = Herramientas.get_simple("https://semanariouniversidad.com")

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
    portada  = (homePage.find('div', attrs= {'class': 'owl-wrapper'}))
    noticias_portada = portada.find_all('a')

    for x in range (0,5) :
        div_con_link = noticias_portada[x]
        links.append(div_con_link.a['href'])

    indice = 1

    #for


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