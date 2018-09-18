import Herramientas
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement, Comment

def obtenerPortada(directorio, codigo):
    try:
        #codigo = Herramientas.obtenerCodigoTiempo()
        Herramientas.crearCarpeta(directorio, codigo, "MONUMENTAL.CO.CR")

        info = Herramientas.get_simple("http://www.monumental.co.cr")

        links = []

        homePage = BeautifulSoup(info, 'html.parser')
        noticias_portada  = (homePage.find_all('div', attrs= {'class': 'carousel-caption'}))

        for x in noticias_portada :
            a_con_link = x.find('a')
            links.append(a_con_link['href'])

        noticias_portada = homePage.find('div', attrs={'class': 'cont-noticias'})
        articulos_portada = noticias_portada.find_all('article')

        for articulo in articulos_portada:
            a_con_link = list(articulo.find_all('a'))[1]
            links.append(a_con_link['href'])

        indice = 1

        for x in links:

            try:
                link = x
                info1 = Herramientas.get_simple(link)
                sou = BeautifulSoup(info1, 'html.parser')

                archivo_xml = Element('nota')
                archivo_txt = ""

                # Titulo
                titulo = (sou.find('article').find('h2').getText())
                archivo_txt = archivo_txt + titulo + "\n"
                tit = SubElement(archivo_xml, 'titulo')
                tit.text = titulo
                nombre = "top" + str(indice) + "__" + titulo.replace(":", ",").replace("?", "¿").replace("\"", "")

                # Bajada NA

                # Parrafos
                contenidos = sou.find('div', attrs={'class': 'the-content'})

                texto = SubElement(archivo_xml, 'texto')

                aux = contenidos.find_all('p')

                es_lead = True

                for p in aux:
                    if "@" not in p.getText() and "Por:" not in p.getText() :
                        t = p.getText().replace(u'\xa0', '').replace("\n", "")
                        if not t == '':
                            if (es_lead):
                                parr = SubElement(texto, 'lead')
                                parr.text = p.getText()
                                es_lead = False
                            else:
                                parr = SubElement(texto, 'parrafo')
                                parr.text = p.getText()
                            archivo_txt = archivo_txt + p.getText() + "\n"


                # Tags NO APLICA

                # Categoría
                clasificacion = (sou.find('meta', attrs={'property': 'article:section'}))['content']
                cat = SubElement(archivo_xml, 'categoria')
                cat.text = clasificacion.replace("\n", "")

                # Codificacion
                archivo_txt = archivo_txt.encode('iso-8859-1', 'ignore').decode('iso-8859-1', 'ignore')
                archivo_xml = Herramientas.prettify(archivo_xml).encode('iso-8859-1', 'ignore').decode('iso-8859-1', 'ignore')

                # Creacion de archivos
                Herramientas.hacerArchivo( archivo_txt, nombre, '.txt')
                Herramientas.hacerArchivo( archivo_xml, nombre, '.xml')

            except Exception as e:
                err = str(e) + "-MONUMENTAL-" + str(link) + "---"
                print(err)
                Herramientas.guardarError(err)

            indice = indice + 1

    except Exception as e:
        err = str(e) + "-MONUMENTAL-"
        print(err)
        Herramientas.guardarError(err)