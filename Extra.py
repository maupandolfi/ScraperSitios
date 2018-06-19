import Herramientas
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement, Comment

def obtenerPortada(directorio):

    codigo = Herramientas.obtenerCodigoTiempo()
    Herramientas.crearCarpeta(directorio, codigo, "DIARIOEXTRA.COM")
    info = Herramientas.get_simple("https://www.diarioextra.com")

    links = []

    homePage = BeautifulSoup(info, 'html.parser')
    portada  = (homePage.find('div', attrs= {'id': 'mainBanner'}))
    noticias_portada = portada.find_all('li')

    for n in range (0,5) :
        links.append("https://www.diarioextra.com" + noticias_portada[n].a['href'])

    indice = 1

    for x in links:
        link = x
        info1 = Herramientas.get_simple(link)
        sou = BeautifulSoup(info1, 'html.parser')

        archivo_xml = Element('nota')
        archivo_txt = ""

        contenido_noticia = sou.find('div', attrs= {'class', 'mainNew'})

        # Titulo
        encabezado = contenido_noticia.find('figcaption')
        titulo = encabezado.h1.getText()
        archivo_txt = archivo_txt + titulo + "\n"
        tit = SubElement(archivo_xml, 'titulo')
        tit.text = titulo
        nombre = "top" + str(indice) + "__" + titulo.replace(":", ",").replace("?", "¿").replace("\"", "")

        # Bajada
        bajada = encabezado.h3.getText()
        baj = SubElement(archivo_xml, 'bajada')
        baj.text = bajada.replace("\n", "")
        archivo_txt = archivo_txt + bajada + "\n"

        # Parrafos
        contenidos = contenido_noticia.find('article')

        texto = SubElement(archivo_xml, 'texto')

        aux = contenidos.find_all('p')

        es_lead = True

        for p in aux:
            padres = p.parents
            if not (p.parent.name == "section" or p.parent.parent.name == "section") :
                t = p.getText().replace(u'\xa0', '').replace("\n","")
                if not t == '' :
                    if (es_lead):
                        parr = SubElement(texto, 'lead')
                        parr.text = p.getText()
                        es_lead = False
                    else:
                        if (p.find('strong') is None) :
                            parr = SubElement(texto, 'parrafo')
                            parr.text = p.getText()
                        else :
                            subt = SubElement(texto, 'subtitulo')
                            subt.text = p.getText()

                    archivo_txt = archivo_txt + p.getText() + "\n"


        # Tags NO HAY

        # Categoría
        clasificacion = contenido_noticia.find('span')
        cat = SubElement(archivo_xml, 'categoria')
        cat.text = clasificacion.getText().replace("\n", "")

        # Codificacion
        archivo_txt = archivo_txt.encode('iso-8859-1', 'ignore').decode('iso-8859-1', 'ignore')
        archivo_xml = Herramientas.prettify(archivo_xml).encode('iso-8859-1', 'ignore').decode('iso-8859-1', 'ignore')

        # Creacion de archivos
        Herramientas.hacerArchivo( archivo_txt, nombre, '.txt')
        Herramientas.hacerArchivo( archivo_xml, nombre, '.xml')

        indice = indice + 1

