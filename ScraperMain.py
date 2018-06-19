import CRHoy
import Nacion
import Extra
import Financiero
import Monumental
import Semanario
import PrensaLibre

import os

def obtenerInfo():

    directorio = 'C:\\Users\\Isiles\\PycharmProjects\\ScraperSitios\\RESULTADOS'

    os.chdir(directorio)
    CRHoy.obtenerPortada()

    os.chdir(directorio)
    Nacion.obtenerPortada()

    os.chdir(directorio)
    Extra.obtenerPortada()

    os.chdir(directorio)
    Financiero.obtenerPortada()

    os.chdir(directorio)
    Monumental.obtenerPortada()

#    os.chdir(directorio)
#    PrensaLibre.obtenerPortada()





obtenerInfo()