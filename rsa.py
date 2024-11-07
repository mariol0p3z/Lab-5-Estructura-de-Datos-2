from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import base64
import os

class RSA:
    def __init__(self):
        self.llaves_empresas = {}
        os.makedirs("Llaves", exist_ok=True)

    def generarLlaves(self, nombreEmpresa, nombreReclutador):
        llave_privada = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        llave_publica = llave_privada.public_key()

        if nombreEmpresa not in self.llaves_empresas:
            self.llaves_empresas[nombreEmpresa] = {}

        self.llaves_empresas[nombreEmpresa][nombreReclutador] = {
            "private_key":llave_privada,
            "public_key":llave_publica
        }

        self.save_keys_to_files(nombreEmpresa, nombreReclutador, llave_privada, llave_publica)

    def save_keys_to_files(self, company_name, recruiter_name, private_key, public_key):
        folder = "Llaves"
        private_key_file = os.path.join(folder, f"{company_name}_{recruiter_name}_private_key.pem")
        public_key_file = os.path.join(folder, f"{company_name}_{recruiter_name}_public_key.pem")

        with open(private_key_file, "wb") as private_file:
            private_file.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
            )

        with open(public_key_file, "wb") as public_file:
            public_file.write(
                public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
            )
        print(f"Claves guardadas en archivos:\n{private_key_file}\n{public_key_file}")


    def getLlavePublica(self, nombreEmpresa, nombreReclutador):
        llave_publica = self.llaves_empresas[nombreEmpresa][nombreReclutador]["public_key"]
        pem = llave_publica.public_bytes(encoding = serialization.Encoding.PEM, format = serialization.PublicFormat.SubjectPublicKeyInfo)
        return pem.decode('utf-8')

    def getLlavePrivada(self, nombreEmpresa, nombreReclutador):
        llave_privada = self.llaves_empresas[nombreEmpresa][nombreReclutador]["private_key"]
        pem = llave_privada.private_bytes(encoding = serialization.Encoding.PEM, format = serialization.PrivateFormat.PKCS8, encryption_algorithm = serialization.NoEncryption())
        return pem.decode('utf-8')

    def encriptarEmpresas(self, nombreEmpresa, nombreReclutador, datos):
        llave_publica = self.llaves_empresas[nombreEmpresa][nombreReclutador]["public_key"]
        encrypted = llave_publica.encrypt(datos.encode(), padding.OAEP(mgf = padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256, label = None))
        return base64.b64encode(encrypted).decode('utf-8')

    def desencriptarEmpresas(self, nombreEmpresa, nombreReclutador, datos_encriptados):
        llave_privada = self.llaves_empresas[nombreEmpresa][nombreReclutador]["private_key"]
        datos_encriptados = base64.b64decode(datos_encriptados)
        decrypted = llave_privada.decrypt(datos_encriptados, padding.OAEP(mgf = padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label= None))
        return decrypted.decode('utf-8')


    def sign_data(self, nombreEmpresa, nombreReclutador, datos):
        llave_privada = self.llaves_empresas[nombreEmpresa][nombreReclutador]["private_key"]
        signature = llave_privada.sign(datos.encode(), padding.PSS(mgf = padding.MGF1(hashes.SHA256()), salt_length = padding.PSS.MAX_LENGTH), hashes.SHA256())
        return base64.b64encode(signature).decode('utf-8')

    def verify_data(self, nombreEmpresa, nombreReclutador, datos, signature):
        llave_publica = self.llaves_empresas[nombreEmpresa][nombreReclutador]["public_key"]
        try:
            llave_publica.verify(base64.b64decode(signature), datos.encode(), padding.PSS(mgf = padding.MGF1(hashes.SHA256()), salt_length = padding.PSS.MAX_LENGTH), hashes.SHA256())
            return True
        except Exception:
            return False