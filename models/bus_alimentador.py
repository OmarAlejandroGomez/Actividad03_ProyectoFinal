from models.vehiculo import Vehiculo


class BusAlimentador(Vehiculo):

    def __init__(self, codigo, capacidad, barrio, paradas_fijas):
        super().__init__(codigo, capacidad)
        self.set_barrio(barrio)
        self.set_paradas_fijas(paradas_fijas)

    # Barrio
    def get_barrio(self):
        return self._barrio

    def set_barrio(self, barrio):
        if barrio.strip() != "":
            self._barrio = barrio.strip()
        else:
            raise ValueError("El barrio no puede estar vacío")

    # Paradas fijas: el alimentador se detiene siempre en las mismas paradas (no se solicitan)
    def get_paradas_fijas(self):
        return self._paradas_fijas

    def set_paradas_fijas(self, paradas_fijas):
        if isinstance(paradas_fijas, int) and paradas_fijas > 0:
            self._paradas_fijas = paradas_fijas
        else:
            raise ValueError("Las paradas fijas deben ser un número entero mayor a cero")

    def cambiar_barrio(self, nuevo_barrio):
        self.set_barrio(nuevo_barrio)

    # Reglas supuestas (el diagrama no las define): el alimentador NO cobra tarifa (la tarjeta solo registra el ingreso)
    # y tarda 5 minutos por tramo más 1 minuto por cada parada fija
    def calcular_tarifa(self, tarifa_base):
        return 0

    def tiempo_estimado(self, tramos):
        return tramos * 5 + self._paradas_fijas

    def descripcion(self):
        return (
            f"{super().descripcion()} - Tipo: Alimentador - Barrio: {self._barrio} - "
            f"Paradas fijas: {self._paradas_fijas}"
        )
