import datetime
from xml.dom import minidom
from xml.etree import ElementTree

import os
from requests import get
from requests.exceptions import RequestException
from contextlib import closing

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



def get_especial(url):
    try:
        h = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        with closing(get(url, stream=True, headers=h)) as resp:
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


def prettify(elem):
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def obtenerCodigoTiempo ():
    obj = datetime.datetime.now()

    anno = obj.year

    r_dia = obj.day
    if r_dia < 10:
        dia = "0" + str(r_dia)
    else:
        dia = str(r_dia)

    r_mes = obj.month
    if r_mes < 10:
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

    nombre_carpeta = str(anno) + "-" + mes + "-" + dia + "__" + hora + "-" + min
    return nombre_carpeta


def crearCarpeta (directorio, nom, medio) :
    os.chdir(directorio)
    if not os.path.exists(nom):
        os.makedirs(nom)
        os.makedirs(nom + "/" + medio)
    elif not os.path.exists(nom + "/" + medio):
        os.makedirs(nom + "/" + medio)
    os.chdir(nom + "/" + medio)


def hacerArchivo( info, nom, tipo):
    com = nom + tipo
    file = open(com, "w")
    file.write(info)
    file.close()