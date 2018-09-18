import Herramientas
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement, Comment

def obtenerPortada(directorio, codigo):

    try:

        #codigo = Herramientas.obtenerCodigoTiempo()
        Herramientas.crearCarpeta(directorio, codigo, "LAPRENSALIBRE.CR")

        info = Herramientas.get_simple("https://www.laprensalibre.cr")

        links = []

        homePage = BeautifulSoup(info, 'html.parser')

        portadas = homePage.find_all('section')

        categorias = []

        for port in portadas:
            portada  = port.find_all('a')

            for noticia in portada :
                links.append("https://www.laprensalibre.cr" + noticia['href'])
                cat = noticia.find('p', attrs={'class', 'sectionName'})
                if cat :
                    categorias.append(cat.getText())
                else :
                    categorias.append("")

        indice = 1

        for link in links:

            try:

                info1 = Herramientas.get_simple(link)
                sou = BeautifulSoup(info1, 'html.parser')

                archivo_xml = Element('nota')
                archivo_txt = ""

                contenidos = sou.find('section')

                # Titulo
                titulo = contenidos.h1.getText()
                archivo_txt = archivo_txt + titulo + "\n"
                tit = SubElement(archivo_xml, 'titulo')
                tit.text = titulo
                nombre = "top" + str(indice) + "__" + titulo.replace(":", ",").replace("?", "¿").replace("\"", "")

                # Bajada
                bajada = sou.find_all('div', attrs={'class': 'preTitle'})
                for b in bajada:
                    baj = SubElement(archivo_xml, 'bajada')
                    baj.text = b.getText().replace("\n", "")
                    archivo_txt = archivo_txt + b.getText() + "\n"

                # Parrafos

                texto = SubElement(archivo_xml, 'texto')

                aux = contenidos.find_all('p')

                es_lead = True

                for p in aux:
                    if p.contents and p.contents[0].name is None and p.parent.name != 'a' and p.parent.name != 'article':
                        for parrafo in p.contents :
                            if parrafo.name is None and parrafo != ' ':
                                if (es_lead):
                                    parr = SubElement(texto, 'lead')
                                    parr.text = parrafo
                                    es_lead = False
                                else:
                                    parr = SubElement(texto, 'parrafo')
                                    parr.text = parrafo
                                archivo_txt = archivo_txt + parrafo + "\n"


                # Tags NA
                div_tags = sou.find('div', attrs={'id': 'tags'})
                tags = div_tags.find_all('a')
                for tag in tags :
                    tag_xml = SubElement(archivo_xml, 'etiqueta')
                    tag_xml.text = tag.getText()

                # Categoría
                clasificacion = categorias[indice-1]
                cat = SubElement(archivo_xml, 'categoria')
                cat.text = categorias[indice-1].replace("\n", "")

                # Codificacion
                archivo_txt = archivo_txt.encode('iso-8859-1', 'ignore').decode('iso-8859-1', 'ignore')
                archivo_xml = Herramientas.prettify(archivo_xml).encode('iso-8859-1', 'ignore').decode('iso-8859-1', 'ignore')

                # Creacion de archivos
                Herramientas.hacerArchivo( archivo_txt, nombre, '.txt')
                Herramientas.hacerArchivo( archivo_xml, nombre, '.xml')


            except Exception as e:
                err = str(e) + "-PRENSALIBRE-" + str(link) + "---"
                print(err)
                Herramientas.guardarError(err)

            indice = indice + 1

    except Exception as e:
        err = str(e) + "-PRENSALIBRE-"
        print(err)
        Herramientas.guardarError(err)
