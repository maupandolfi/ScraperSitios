import Herramientas
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement, Comment

def obtenerPortada(directorio):
    codigo = Herramientas.obtenerCodigoTiempo()
    Herramientas.crearCarpeta(directorio, codigo, "TELETICA.COM")

    info = Herramientas.get_simple("https://www.teletica.com")

    links = []

    homePage = BeautifulSoup(info, 'html.parser')
    portada  = (homePage.find('div', attrs= {'class', 'sector-heading-news'}).find_all('div', attrs= {'class': 'text'}))

    for x in portada :
        as_con_link = x.find_all('a')
        for a in as_con_link :
            links.append("https://www.teletica.com" + a.attrs['href'])

    portada_otros = (homePage.find('div', attrs={'class', 'main-content'}).find_all('div', attrs={'class': 'text'}))

    for x in portada_otros:
        as_con_link = x.find_all('a')
        for a in as_con_link:
            links.append("https://www.teletica.com" + a.attrs['href'])

    indice = 1

    for x in links:
        link = x
        info1 = Herramientas.get_simple(link)
        sou = BeautifulSoup(info1, 'html.parser')

        archivo_xml = Element('nota')
        archivo_txt = ""

        encabezado = sou.find('div', attrs= {'class': 'title'})

        # Titulo
        titulo = encabezado.find('h1').getText()
        archivo_txt = archivo_txt + titulo + "\n"
        tit = SubElement(archivo_xml, 'titulo')
        tit.text = titulo
        nombre = "top" + str(indice) + "__" + titulo.replace(":", ",").replace("?", "¿").replace("\"", "")

        # Bajada
        bajada = encabezado.find('h3')
        baj = SubElement(archivo_xml, 'bajada')
        baj.text = bajada.getText().replace("\n", "")
        archivo_txt = archivo_txt + bajada.getText() + "\n"

        # Parrafos

        contenidos = sou.find('div', attrs={'class': 'main-content'})

        texto = SubElement(archivo_xml, 'texto')

        aux = contenidos.find('div', attrs={'class': 'body'})
        textos = aux.find_all('p')

        es_lead = True

        for p in textos:
            if (es_lead):
                parr = SubElement(texto, 'lead')
                parr.text = p.getText()
                es_lead = False
            else:
                parr = SubElement(texto, 'parrafo')
                parr.text = p.getText()

            archivo_txt = archivo_txt + p.getText() + "\n"


        # Tags
        div_tags = contenidos.find('div', attrs={'class': 'tags'})
        tags = div_tags.find_all('a')
        for tag in tags :
            tag_xml = SubElement(archivo_xml, 'etiqueta')
            tag_xml.text = tag.getText()

        # Categoría
        clasificacion = (sou.find('div', attrs={'id':'main'})).find('h3').getText()
        cat = SubElement(archivo_xml, 'categoria')
        cat.text = clasificacion.replace("\n", "")

        # Codificacion
        archivo_txt = archivo_txt.encode('iso-8859-1', 'ignore').decode('iso-8859-1', 'ignore').replace('&quot;', '')
        archivo_xml = Herramientas.prettify(archivo_xml).encode('iso-8859-1', 'ignore').decode('iso-8859-1', 'ignore').replace('&quot;', '')

        # Creacion de archivos
        Herramientas.hacerArchivo( archivo_txt, nombre, '.txt')
        Herramientas.hacerArchivo( archivo_xml, nombre, '.xml')

        indice = indice + 1


