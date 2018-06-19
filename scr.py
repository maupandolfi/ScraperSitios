from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

import datetime

def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if esta_bienj(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def esta_bienj(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('json') > -1)


def simple_get3(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if esta_bien(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def esta_bien(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    print(e)


def masLeidasCRHOY():

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
    codigo_servicio = str(anno) + str(r_mes-1) + str(r_dia)

    ru = nombre_carpeta
    import os
    try:
        os.makedirs(ru)
    except OSError:
        pass
    os.chdir(ru)

    info = simple_get("https://www.crhoy.com/site/dist/json/index2.json?v=" + codigo_servicio)
    import json
    j = json.loads(info)

    for x in range(0, 5):
        link = j['masleidas'][x]['url']
        info1 = simple_get3(link)
        sou = BeautifulSoup(info1, 'html.parser')
        nombre = sou.find('title').getText().replace(":", ",").replace("?","¿")
        contenidos = sou.find_all('div', attrs={'class' : 'contenido'})
        for i in contenidos:
            aux = i.find_all('p', attrs={'class':None})
            num = len(aux)
            st = ""
            for p in aux:
                hijos_div = p.find_all('div')
                hijos_span = p.find_all('span')
                if len(hijos_div)+len(hijos_span) == 0 :
                    lista = list(p.strings)
                    largo = len(lista)
                    for p2 in range (0, largo) :
                        st = st + lista[p2]
                    st = st + "\n"
            st = st.encode('iso-8859-1', 'ignore').decode('iso-8859-1', 'ignore')
            hacerArchivo(ru, st , nombre)


def hacerArchivo(ruta, info, nom):
    import os
    com = ruta + nom + ".txt"
    file = open(com, "w")
    file.write(info)
    file.close()





masLeidasCRHOY()