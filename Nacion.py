import Herramientas
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement, Comment

def obtenerPortada(directorio):
    codigo = Herramientas.obtenerCodigoTiempo()
    Herramientas.crearCarpeta(directorio, codigo, "NACION.COM")

    info = Herramientas.get_simple("https://www.nacion.com")

    links = []

    homePage = BeautifulSoup(info, 'html.parser')
    portada  = (homePage.find_all('div', attrs= {'class': 'pb-c-default-chain'}))
    noticias_portada = []

    for noticia in portada :
        noticias_portada = noticias_portada + noticia.find_all('div', attrs={'class': 'pb-f-homepage-story'})

    for x in noticias_portada :
        div_con_link = x.find('div', attrs={'class' : 'headline'})
        links.append("https://www.nacion.com" + div_con_link.a['href'])

    indice = 1

    for x in links:
        link = x
        info1 = Herramientas.get_simple(link)
        sou = BeautifulSoup(info1, 'html.parser')

        archivo_xml = Element('nota')
        archivo_txt = ""

        # Titulo
        aux_titulo = sou.find('div', attrs= {'class', 'headline-hed-last'})
        if aux_titulo:
            titulo = aux_titulo.getText()
            archivo_txt = archivo_txt + titulo + "\n"
            tit = SubElement(archivo_xml, 'titulo')
            tit.text = titulo
            nombre = "top" + str(indice) + "__" + titulo.replace(":", ",").replace("?", "¿").replace("\"", "")

            # Bajada
            bajada = sou.find('p', attrs={'class': 'subheadline'})
            if bajada:
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
            if div_tags :
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
            archivo_xml = Herramientas.prettify(archivo_xml).encode('iso-8859-1', 'ignore').decode('iso-8859-1', 'ignore')

            # Creacion de archivos
            Herramientas.hacerArchivo( archivo_txt, nombre, '.txt')
            Herramientas.hacerArchivo( archivo_xml, nombre, '.xml')

            indice = indice + 1


