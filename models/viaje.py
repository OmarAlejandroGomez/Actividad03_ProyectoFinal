
class Viaje:
    
    def __init__(self, tarjeta, vehiculo, origen, destino, hora, valor, minutos):
        self.set_tarjeta(tarjeta)
        self.set_vehiculo(vehiculo)
        self.set_origen(origen)
        self.set_destino(destino)
        self.set_hora(hora)
        self.set_valor(valor)
        self.set_minutos(minutos)
    
    def get_tarjeta(self):
        return self._tarjeta
    
    def get_vehiculo(self):
        return self._vehiculo

    def get_origen(self):
        return self._origen

    def get_destino(self):
        return self._destino

    def get_hora(self):
        return self._hora

    def get_valor(self):
        return self._valor

    def get_minutos(self):
        return self._minutos
    
    def resumen(self):
        return (
            f"Tarjeta {self._tarjeta.get_numero()} - Vehiculo {self._vehiculo.get_codigo()} - "
            f"{self._origen.get_nombre()} -> {self._destino.get_nombre()} - "
            f"Hora: {self._hora.strftime('%H:%M')} - Valor: ${self._valor} - Tiempo estimado: {self._minutos} minutos"
        )