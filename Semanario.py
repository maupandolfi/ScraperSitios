import os

import Herramientas
from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree
from selenium import webdriver
from bs4 import BeautifulSoup

def obtenerPortada(directorio, codigo):

    try:

        #codigo = Herramientas.obtenerCodigoTiempo()
        Herramientas.crearCarpeta(directorio, codigo, "SEMANARIOUNIVERSIDAD.COM")

        info = Herramientas.get_browser("https://www.semanariouniversidad.com")
        homePage = BeautifulSoup(info, 'html.parser')

        links = []

        noticias_portada = (homePage.find('div', attrs={'class': 'main-slider-wrap'})).find_all('a', attrs={'title': None})

        for x in noticias_portada :
            links.append(x['href'])

        noticias = (homePage.find('div', attrs={'id': 'block-ajax-query-contenttwelve1'})).find_all('div', attrs= {'class' : 'entry-header'})

        for x in noticias:
            y = x.find('a')
            links.append(y['href'])

        noticias_portada = (homePage.find('div', attrs={'id': 'blockslider2'})).find_all('div', attrs= {'class' : 'item'})

        for x in noticias_portada:
            y = x.find('a')
            links.append(y['href'])

        noticias_portada = (homePage.find('div', attrs={'id': 'block-ajax-query-contentseven3'})).find_all('div', attrs={'class': 'entry-image'})

        for x in noticias_portada:
            y = x.find('a')
            links.append(y['href'])

        indice = 1

        for link in links:

            try:

                info1 = Herramientas.get_browser(link)
                sou = BeautifulSoup(info1, 'html.parser')

                archivo_xml = Element('nota')
                archivo_txt = ""

                # Titulo
                aux_titulo = sou.find('h1')
                if aux_titulo:
                    titulo = aux_titulo.getText()
                    archivo_txt = archivo_txt + titulo + "\n"
                    tit = SubElement(archivo_xml, 'titulo')
                    tit.text = titulo
                    nombre = "top" + str(indice) + "__" + titulo.replace(":", ",").replace("?", "¿").replace("\"", "")

                 # Bajada
                bajada = sou.find('div', attrs={'class': 'entry-excerpt'})
                if bajada:
                    baj = SubElement(archivo_xml, 'bajada')
                    baj.text = bajada.getText().replace("\n", "")
                    archivo_txt = archivo_txt + bajada.getText() + "\n"

                # Parrafos
                contenidos = sou.find('div', attrs={'class': 'entry-content-text'})

                texto = SubElement(archivo_xml, 'texto')

                aux = contenidos.find_all(['p','h3'])

                es_lead = True

                for p in aux:
                    if (p.contents and ( p.contents[0].name == 'strong' or p.contents[0].name == 'b') ) or (p.name == 'h3') :
                        subtit = SubElement(texto, 'subtitulo')
                        subtit.text = p.getText()
                    else :
                        if (es_lead):
                            parr = SubElement(texto, 'lead')
                            parr.text = p.getText()
                            es_lead = False
                        else:
                             parr = SubElement(texto, 'parrafo')
                             parr.text = p.getText()
                    archivo_txt = archivo_txt + p.getText() + "\n"
                    aux_tags = sou.find('div', attrs={'class':'entry-tag-cat'}).contents

                # Tags
                div_tags = aux_tags[0]
                if div_tags:
                     tags = div_tags.find_all('a')
                     for tag in tags:
                         tag_xml = SubElement(archivo_xml, 'etiqueta')
                         tag_xml.text = tag.getText()

                # Cats
                div_cats = aux_tags[1]
                if div_cats:
                    cats = div_cats.find_all('a')
                    for cat in cats:
                        cat_xml = SubElement(archivo_xml, 'categoria')
                        cat_xml.text = cat.getText().replace("\n", "")

                # Codificacion
                archivo_txt = archivo_txt.encode('iso-8859-1', 'ignore').decode('iso-8859-1', 'ignore')
                archivo_xml = Herramientas.prettify(archivo_xml).encode('iso-8859-1', 'ignore').decode('iso-8859-1','ignore')

                # Creacion de archivos
                Herramientas.hacerArchivo(archivo_txt, nombre, '.txt')
                Herramientas.hacerArchivo(archivo_xml, nombre, '.xml')

            except Exception as e:
                err = str(e) + "-SEMANARIO-" + str(link) + "---"
                print(err)
                Herramientas.guardarError(err)

            indice = indice + 1

    except Exception as e:
        err = str(e) + "-SEMANARIO-"
        print(err)
        Herramientas.guardarError(err)
