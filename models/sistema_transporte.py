
class SistemaTransporte:
    
    def __init__(self, nombre, tarifa_base):
        self.set_nombre(nombre)
        self.set_tarifa_base(tarifa_base)
        self.estaciones = []
        self.rutas = []
        self.flota = []
        self.viajes = []
    
    #Nombre
    def get_nombre(self):
        return self._nombre
    
    def set_nombre(self, nombre):
        if nombre.strip() != "":
            self._nombre = nombre.strip()
        else:
            raise ValueError("El nombre del sistema no puede estar vacío.")
    
    #Tarifa Base
    def get_tarifa_base(self):
        return self._tarifa_base
    
    def set_tarifa_base(self, tarifa_base):
        if tarifa_base >= 0:
            self._tarifa_base = tarifa_base
        else:
            raise ValueError("La tarifa base no puede ser negativa.")
    
    # Las listas se entregan como copias para evitar modificaciones
    def get_estaciones(self):
        return self.estaciones.copy()
    
    def get_rutas(self):
        return self.rutas.copy()
    
    def get_flota(self):
        return self.flota.copy()
    
    def get_viajes(self):
        return self.viajes.copy()