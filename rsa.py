from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import base64

class RSA:
    def __init__(self):
        self.llaves_empresas = {}

    def generarLlavesEmpresas(self, nombreEmpresa):
        llave_privada = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        llave_publica = llave_privada.public_key()

        self.llaves_empresas[nombreEmpresa] = {
            "private_key":llave_privada,
            "public_key":llave_publica
        }

    def getLlavePublica(self, nombreEmpresa):
        llave_publica = self.llaves_empresas[nombreEmpresa]["public_key"]
        pem = llave_publica.public_bytes(encodig = serialization.Encoding.PEM, format = serialization.PublicFormat.SubjectPublicKeyInfo)
        return pem.decode('utf-8')

    def getLlavePrivada(self, nombreEmpresa):
        llave_privada = self.llaves_empresas[nombreEmpresa]["private_key"]
        pem = llave_privada.private_bytes(encoding = serialization.Encoding.PEM, format = serialization.PrivateFormat.PKCS8, encryption_algorithm = serialization.NoEncryption())
        return pem.decode('utf-8')

    def encriptarEmpresas(self, nombreEmpresa, datos):
        llave_publica = self.llaves_empresas[nombreEmpresa]["public_key"]
        encrypted = llave_publica.encrypt(datos.encode(), padding.OAEP(mgf = padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256, label = None))
        return base64.b64encode(encrypted).decode('utf-8')

    def desencriptarEmpresas(self, nombreEmpresa, datos_encriptados):
        llave_privada = self.llaves_empresas[nombreEmpresa]["private_key"]
        datos_encriptados = base64.b64decode(datos_encriptados)
        decrypted = llave_privada.decrypt(datos_encriptados, padding.OAEP(mgf = padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label= None))
        return decrypted.decode('utf-8')