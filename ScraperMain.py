import CRHoy
import Nacion
import Extra
import Financiero
import Monumental
import PrensaLibre
import Repretel
import Teletica
import AmeliaRueda
import Semanario
import Herramientas

def obtenerInfo():

    directorio = 'C:\\Users\\Isiles\\PycharmProjects\\ScraperSitios\\MUESTRAS_5PM'
    codigo = Herramientas.obtenerCodigoTiempo()

    CRHoy.obtenerPortada(directorio, codigo)
    Nacion.obtenerPortada(directorio, codigo)
    Extra.obtenerPortada(directorio, codigo)
    Financiero.obtenerPortada(directorio, codigo)
    Monumental.obtenerPortada(directorio, codigo)
    PrensaLibre.obtenerPortada(directorio, codigo)
    Repretel.obtenerPortada(directorio, codigo)
    Teletica.obtenerPortada(directorio, codigo)
    AmeliaRueda.obtenerPortada(directorio, codigo)
    Semanario.obtenerPortada(directorio, codigo)

obtenerInfo()