
class Vehiculo:
    
    def __init__(self, codigo, capacidad):
        self.set_codigo(codigo)
        self.set_capacidad(capacidad)
        self._ruta = None  # Inicialmente, el vehículo no tiene ruta asignada
        
    # Código
    def get_codigo(self):
        return self._codigo
    
    def set_codigo(self, codigo):
        if codigo.strip() != "":
            self._codigo = codigo.strip().upper()
        else:
            raise ValueError("El código del vehículo no puede estar vacío.")
    
    # Capacidad
    def get_capacidad(self):
        return self._capacidad
    
    def set_capacidad(self, capacidad):
        if capacidad > 0:
            self._capacidad = capacidad
        else:
            raise ValueError("La capacidad del vehículo debe ser mayor que cero.")
    
    # Ruta
    def get_ruta(self):
        return self._ruta
    
    def asignar_ruta(self, ruta):
        if ruta is not None:
            self._ruta = ruta
        else:
            raise ValueError("Debe indicar una ruta existente.")
    
    def calcular_tarifa(self, tarifa_base):
        if self._ruta is not None:
            return tarifa_base * self._ruta.get_distancia()
        else:
            raise ValueError("El vehículo no tiene una ruta asignada.")
        
    def tiempo_estimado(self, tramos):
        if self._ruta is not None:
            return self._ruta.calcular_tiempo_estimado(tramos)
        else:
            raise ValueError("El vehículo no tiene una ruta asignada.")
    
    