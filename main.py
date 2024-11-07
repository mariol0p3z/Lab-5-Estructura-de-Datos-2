from arbolb import Arbol_B
from rsa import RSA
import json

class main:
    def __init__(self):
        self.arbol = Arbol_B(3)
        self.key_manager = RSA()

    def leerArchivo(self, nombre_archivo):
        with open(nombre_archivo, mode ='r', encoding='utf-8') as archivo:
            try:
                for linea in archivo:
                    separacion = linea.split(";")
                    
                    accion =  separacion[0]
                    dato_json = separacion[1].strip()

                    if dato_json.startswith('"') and dato_json.endswith('"'):
                        dato_json = dato_json[1:-1]
                        dato_json = dato_json.replace('""', '"')
                    
                    try:
                        dato = json.loads(dato_json)
                    except json.JSONDecodeError as e:
                        print(f"Error al decodificar JSON: {e}")
                        continue
        
                    if accion == "INSERT":
                        self.arbol.insertar(dato)
                    elif accion == "PATCH":
                        self.arbol.actualizar(dato.get("dpi"), dato.get("name"), dato)
                    elif accion == "DELETE":
                        self.arbol.eliminar({"name": dato.get("name"), "dpi": dato.get("dpi")})
            except FileNotFoundError:
                print("Archivo no encontrado")
            finally:
                archivo.close()

    def validarIdentidad(self, empresa, reclutador, nombre, dpi):
        datos = f"{nombre}-{dpi}"
        firma = self.key_manager.sign_data(empresa, reclutador, datos)
        print(f"Firma generada para {nombre} en {empresa} por reclutador {reclutador}: {firma}")

        es_valida = self.key_manager.verify_data(empresa, reclutador, datos, firma)
        if es_valida:
            print("Identidad verificada correctamente")
        else:
            print("No se pudo realizar la verificacion")

if __name__ == '__main__':
    programa = main()
    nombre_archivo = input("Ingrese el nombre del archivo: ")
    programa.leerArchivo(nombre_archivo)

    nombre_persona = input("Ingrese el nombre de la persona que desea buscar: ")
    resultados = programa.arbol.buscarNombre(nombre_persona)

    if not resultados:
        print("No se encontró ninguna persona con ese nombre.")
    else:
        for persona in resultados:
             print(f"\nPersona encontrada: {persona['name']}")
             for company in persona["companies"]:
                reclutador = persona["recluiter"]
                programa.key_manager.generarLlaves(company, reclutador)
                programa.validarIdentidad(company, reclutador, persona["name"], persona["dpi"])