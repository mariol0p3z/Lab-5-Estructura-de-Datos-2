from cifrado import Transposicion
from arbolb import Arbol_B
import json
import os

class main:
    def __init__(self):
        self.arbol = Arbol_B(3)
        self.carpeta = "Input"

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

    def leerTexto(self):
        nombre = input("Ingrese el nombre de la persona: ")
        dpi = input("Ingrese el dpi de la persona: ")
        llave  = input("Ingrese la contraseña para el cifrado y descifrado: ")
        transposicion = Transposicion(llave)
        
        archivo_conversaciones = {archivo for archivo in os.listdir(self.carpeta) if archivo.startswith(f"CONV-{dpi}")}

        if not archivo_conversaciones:
            print(f"No se encontraron conversaciones con los datos ingresados")
            return

        persona = self.arbol.buscar_por_nombre_y_dpi(dpi, nombre)

        if not persona:
            print(f"No se encontro a la persona dentro de nuestros registros")
            return

        for archivo_conversacion in archivo_conversaciones:
            ruta_archivo = os.path.join(self.carpeta, archivo_conversacion) 
            try:
                with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                    contenido = archivo.read()

                datos_encriptados = transposicion.cifrado(contenido)
                numero_conversacion = archivo_conversacion.split('-')[-1].replace('.txt','')
                archivo_encriptado = os.path.join('Encriptados', archivo_conversacion.replace('.txt','_encriptado.txt'))

                with open(archivo_encriptado, 'w', encoding='utf-8') as salida:
                    salida.write(datos_encriptados)
                print(f"Archivo {numero_conversacion} encriptada exitosamente")

                datos_desencriptados = transposicion.descifrar(datos_encriptados)
                archivo_desencriptado = os.path.join('Desencriptados', archivo_conversacion.replace('.txt', '_desencriptado.txt'))

                with open(archivo_desencriptado, 'w', encoding='utf-8') as salida:
                    salida.write(datos_desencriptados)
                
                print(f"Conversacion {numero_conversacion} desencriptada y guardada como {archivo_desencriptado}")
            except FileNotFoundError:
                print(f"El archivo {ruta_archivo} no fue encontrado")

if __name__ == '__main__':
    programa = main()
    nombre_archivo = input("Ingrese el nombre del archivo: ")
    programa.leerArchivo(nombre_archivo)
    programa.leerTexto()

#therese - 1044665857995
#coty - 1016156267944