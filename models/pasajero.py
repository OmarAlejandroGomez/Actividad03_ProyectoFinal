from models.tarjeta import Tarjeta


class Pasajero:

    def __init__(self, documento, nombre, perfil):
        self.set_documento(documento)
        self.set_nombre(nombre)
        self.set_perfil(perfil)
        self._tarjeta = None            # un pasajero puede no tener tarjeta (0..1)

    # Documento
    def get_documento(self):
        return self._documento

    def set_documento(self, documento):
        if documento.strip() != "":
            self._documento = documento.strip()
        else:
            raise ValueError("El documento no puede estar vacío")

    # Nombre
    def get_nombre(self):
        return self._nombre

    def set_nombre(self, nombre):
        if nombre.strip() != "":
            self._nombre = nombre.strip()
        else:
            raise ValueError("El nombre no puede estar vacío")

    # Perfil (por ejemplo: General, Estudiante, Adulto mayor)
    def get_perfil(self):
        return self._perfil

    def set_perfil(self, perfil):
        if perfil.strip() != "":
            self._perfil = perfil.strip()
        else:
            raise ValueError("El perfil no puede estar vacío")

    # Tarjeta (el pasajero es el titular)
    def get_tarjeta(self):
        return self._tarjeta

    def vincular_tarjeta(self, tarjeta):
        if not isinstance(tarjeta, Tarjeta):
            raise ValueError("Debe indicar una tarjeta existente")
        if self._tarjeta is not None:
            raise ValueError("El pasajero ya tiene una tarjeta vinculada")
        self._tarjeta = tarjeta

    def descripcion(self):
        if self._tarjeta is None:
            tarjeta = "Sin tarjeta"
        else:
            tarjeta = self._tarjeta.descripcion()
        return f"Documento: {self._documento} - Nombre: {self._nombre} - Perfil: {self._perfil} - {tarjeta}"
