import Herramientas
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement, Comment

def obtenerPortada(directorio):
    codigo = Herramientas.obtenerCodigoTiempo()
    Herramientas.crearCarpeta(directorio, codigo, "AMELIARUEDA.COM")

    info = Herramientas.get_simple("https://www.ameliarueda.com")

    links = []

    homePage = BeautifulSoup(info, 'html.parser')

    #Noticia_principal
    portada_1  = homePage.find('div', attrs= {'class': 'main-hero__content'}).find('a')
    links.append("https://www.ameliarueda.com" + portada_1.attrs['href'])

    #Slider de titulares
    portada_2 = homePage.find('ul', attrs={'class': 'de-primero__listing'}).find_all('a')

    for noticia in portada_2 :
        links.append(noticia.attrs['href'])

    #Slider vertical
    portada_3 = homePage.find('div', attrs={'class': 'owl-carousel'}).find_all('a')

    for noticia in portada_3 :
        if noticia.attrs['href'].startswith('/') :
            links.append("https://www.ameliarueda.com" + noticia.attrs['href'])

    # Resto de noticias
    portada_4 = homePage.find('div', attrs={'class': 'container'}).find_all('div', attrs={'class': 'main-news-article'})

    for div_con_a in portada_4:
        noticia = div_con_a.find('a')
        links.append("https://www.ameliarueda.com" + noticia.attrs['href'])

    indice = 1

    for x in links:
        link = x
        info1 = Herramientas.get_simple(link)
        sou = BeautifulSoup(info1, 'html.parser')

        archivo_xml = Element('nota')
        archivo_txt = ""

        contenidos = sou.find('div', attrs= {'class': 'note__hero'})

        # Titulo
        titulo = contenidos.find('h1').getText()
        archivo_txt = archivo_txt + titulo + "\n"
        tit = SubElement(archivo_xml, 'titulo')
        tit.text = titulo
        nombre = "top" + str(indice) + "__" + titulo.replace(":", ",").replace("?", "¿").replace("\"", "")

        # Bajada
        bajada = contenidos.find('div', attrs= {'class': 'note__article__summary'})
        baj = SubElement(archivo_xml, 'bajada')
        baj.text = bajada.getText().replace("\n", "")
        archivo_txt = archivo_txt + bajada.getText() + "\n"

        # Parrafos
        texto = SubElement(archivo_xml, 'texto')

        aux = contenidos.find('div', attrs={'class': 'note__article__main-content'})
        textos = aux.find_all(['p','h4'])

        es_lead = True

        for p in textos:
            if p.getText().replace('\n', '') != '':
                if p.name == 'p':
                    if (es_lead):
                        parr = SubElement(texto, 'lead')
                        parr.text = p.getText()
                        es_lead = False
                    else:
                        parr = SubElement(texto, 'parrafo')
                        parr.text = p.getText()
                else :
                    subt = SubElement(texto, 'subtitulo')
                    subt.text = p.getText()

                archivo_txt = archivo_txt + p.getText() + "\n"

        # Tags NO APLICA

        # Categoría NO APLICA

        # Codificacion
        archivo_txt = archivo_txt.encode('iso-8859-1', 'ignore').decode('iso-8859-1', 'ignore').replace('&quot;', '')
        archivo_xml = Herramientas.prettify(archivo_xml).encode('iso-8859-1', 'ignore').decode('iso-8859-1', 'ignore').replace('&quot;', '')

        # Creacion de archivos
        Herramientas.hacerArchivo( archivo_txt, nombre, '.txt')
        Herramientas.hacerArchivo( archivo_xml, nombre, '.xml')

        indice = indice + 1
