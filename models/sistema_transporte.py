from models import ruta
from models.estacion import Estacion
from models.ruta import Ruta
from models.vehiculo import Vehiculo
from models.viaje import Viaje
from models.excepciones import FueraDeHorarioError

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
    
    def agregar_estacion(self, estacion):
        if not isinstance(estacion, Estacion):
            raise ValueError("Debe indicar una estación existente.")
        if any(e.get_codigo() == estacion.get_codigo() for e in self.estaciones):
            raise ValueError(f"Ya existe una estación con el código {estacion.get_codigo()}.")
        self.estaciones.append(estacion)
    
    def agregar_ruta(self, ruta):
        if not isinstance(ruta, Ruta):
            raise ValueError("Debe indicar una ruta existente.")
        if any(r.get_codigo() == ruta.get_codigo() for r in self.rutas):
            raise ValueError(f"Ya existe una ruta con el código {ruta.get_codigo()}.")
        for estacion in ruta.get_estaciones():
            if estacion not in self.estaciones:
                raise ValueError(f"La estación {estacion.get_codigo()} no está registrada en el sistema.")  
        self.rutas.append(ruta)
    
    def agregar_vehiculo(self, vehiculo, ruta):
        if not isinstance(vehiculo, Vehiculo):
            raise ValueError("Debe indicar un vehículo existente.")
        if any(v.get_codigo() == vehiculo.get_codigo() for v in self.flota):
            raise ValueError(f"Ya existe un vehículo con el código {vehiculo.get_codigo()}.")
        if ruta not in self.rutas:
            raise ValueError(f"La ruta {ruta.get_codigo()} no está registrada en el sistema.")
        vehiculo.asignar_ruta (ruta)
        self.flota.append(vehiculo)
    
    def realizar_viaje(self, tarjeta, vehiculo, origen, destino, hora):
        if vehiculo not in self.flota:
            raise ValueError(f"El vehículo {vehiculo.get_codigo()} no está registrado en el sistema.")
        
        ruta = vehiculo.get_ruta()
        
        if not ruta.validar_horario(hora):
            raise FueraDeHorarioError(ruta.get_codigo(), hora)
        
        tramos = ruta.contar_tramos(origen, destino)
        tarifa = vehiculo.calcular_tarifa(self._tarifa_base)

        valor = tarjeta.cobrar(tarifa)
        origen.registrar_ingreso()
        
        minutos = vehiculo.tiempo_estimado(tramos)
        viaje = Viaje(tarjeta, vehiculo, origen, destino, hora, valor, minutos)
        self.viajes.append(viaje)
        return viaje
    
    def recaudo_total(self):
        total = 0
        for viaje in self.viajes:
            total += viaje.get_valor()
        return total
    
    def reporte_estaciones(self):
        ordenadas = sorted(self.estaciones, key=lambda estacion: estacion.get_ingresos(), reverse=True)
        return [estacion.descripcion() for estacion in ordenadas]
    

    