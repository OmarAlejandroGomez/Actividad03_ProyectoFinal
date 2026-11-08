from models.pasajero import Pasajero

class PasajeroController:
    def __init__(self):
        self.pasajeros = []

    def add_pasajero(self, documento, nombre, perfil):
        if any(p.get_documento() == documento.strip() for p in self.pasajeros):
            raise ValueError(f"Ya existe un pasajero con el documento {documento}.")
        
        pasajero = Pasajero(documento, nombre, perfil)
        self.pasajeros.append(pasajero)
        return pasajero

    def buscar_pasajero(self, documento):
        for pasajero in self.pasajeros:
            if pasajero.get_documento() == documento.strip():
                return pasajero
        return None

    def get_pasajeros(self):
        return self.pasajeros.copy()
    