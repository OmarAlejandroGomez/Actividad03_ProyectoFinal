from models.tarjeta import Tarjeta

class TarjetaController:
    def __init__(self):
        self.tarjetas = []

    def add_tarjeta(self, pasajero, numero):
        
        if self.buscar_tarjeta(numero) is not None:
            raise ValueError(f"Ya existe una tarjeta con el número {numero}.")

             
        tarjeta = Tarjeta(numero)
        pasajero.vincular_tarjeta(tarjeta)
        self.tarjetas.append(tarjeta)
        return tarjeta

    def buscar_tarjeta(self, numero):
        for tarjeta in self.tarjetas:
            if tarjeta.get_numero() == numero.strip().upper():
                return tarjeta
        return None

    def get_tarjetas(self):
        return self.tarjetas.copy()