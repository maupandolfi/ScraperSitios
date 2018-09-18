import Herramientas
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement, Comment

def obtenerPortada(directorio, codigo):

    try:

        #codigo = Herramientas.obtenerCodigoTiempo()
        Herramientas.crearCarpeta(directorio, codigo, "REPRETEL.COM")

        info = Herramientas.get_simple("http://www.repretel.com")

        links = []

        homePage = BeautifulSoup(info, 'html.parser')
        portada_1  = homePage.find('section', attrs= {'class', 'noticias-container'})
        portada_2 = portada_1.find_all('a', attrs= {'class': 'contenido'})

        for x in portada_2:
            links.append( x.attrs['href'])

        portada = homePage.find_all('div', attrs={'class', 'mas-leido-nota'})

        for x in portada:
            links.append(x.find('a').attrs['href'])

        portada = homePage.find_all('div', attrs={'class', 'noticia-tipo2'})

        for x in range (0, 4):
            links.append(portada[x].find('a').attrs['href'])

        portada_2 = portada_1.find_next_sibling('section', attrs={'class', 'noticias-container'})
        portada_3 = portada_2.find_all('a', attrs={'class': 'contenido'})

        for x in portada_3:
            links.append( x.attrs['href'])

        for x in range (4, 7):
            links.append(portada[x].find('a').attrs['href'])

        portada_1 = portada_2.find_next_sibling('section', attrs={'class', 'noticias-container'})
        portada_3 = portada_1.find_all('a', attrs={'class': 'contenido'})

        for x in portada_3:
            links.append(x.attrs['href'])


        indice = 1

        for link in links:
            try:

                info1 = Herramientas.get_simple(link)
                sou = BeautifulSoup(info1, 'html.parser')

                archivo_xml = Element('nota')
                archivo_txt = ""

                contenidos = sou.find('section', attrs={'class': 'noticia-container'})

                # Titulo
                titulo = (contenidos.find('h1')).getText()
                archivo_txt = archivo_txt + titulo + "\n"
                tit = SubElement(archivo_xml, 'titulo')
                tit.text = titulo
                nombre = "top" + str(indice) + "__" + titulo.replace(":", ",").replace("?", "¿").replace("\"", "")

                # Bajada
                bajada = sou.find('div', attrs={'class': 'sub-header'})
                baj = SubElement(archivo_xml, 'bajada')
                baj.text = bajada.getText().replace("\n", "")
                archivo_txt = archivo_txt + bajada.getText() + "\n"

                # Parrafos

                texto = SubElement(archivo_xml, 'texto')

                aux = contenidos.find_all('div', attrs={'class':None})
                for au in aux:
                    if au.getText() != 'Cargando el player...' and au.getText() != '':
                        aud = au
                #aux2 = aux.find_all('div', attrs={'class':None})
                textos = aud.find_all('p')

                es_lead = True

                for p in textos:
                    if p.getText().replace('\n', '') != '':
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
                if div_tags :
                    tags = div_tags.find_all('a')
                    for tag in tags :
                        tag_xml = SubElement(archivo_xml, 'etiqueta')
                        tag_xml.text = tag.getText()

                # Categoría
                clasificacion = (sou.find('meta', attrs={'property': 'article:section'})).attrs["content"]
                cat = SubElement(archivo_xml, 'categoria')
                cat.text = clasificacion.replace("\n", "")

                # Codificacion
                archivo_txt = archivo_txt.encode('iso-8859-1', 'ignore').decode('iso-8859-1', 'ignore').replace('&quot;', '')
                archivo_xml = Herramientas.prettify(archivo_xml).encode('iso-8859-1', 'ignore').decode('iso-8859-1', 'ignore').replace('&quot;', '')

                # Creacion de archivos
                Herramientas.hacerArchivo( archivo_txt, nombre, '.txt')
                Herramientas.hacerArchivo( archivo_xml, nombre, '.xml')

            except Exception as e:
                err = str(e) + "-REPRETEL-" + str(link) + "---"
                Herramientas.guardarError(err)

            indice = indice + 1

    except Exception as e:
        err = str(e) + "-REPRETEL-"
        print(err)
        Herramientas.guardarError(err)

