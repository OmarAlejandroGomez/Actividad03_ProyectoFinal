from models.vehiculo import Vehiculo
#bus

class BusTroncal(Vehiculo):

    def __init__(self, codigo, capacidad, cuerpos, puertas_izquierdas):
        super().__init__(codigo, capacidad)
        self.set_cuerpos(cuerpos)
        self.set_puertas_izquierdas(puertas_izquierdas)

    # Cuerpos (1 = bus sencillo, 2 = articulado, 3 = biarticulado)
    def get_cuerpos(self):
        return self._cuerpos

    def set_cuerpos(self, cuerpos):
        if isinstance(cuerpos, int) and cuerpos > 0:
            self._cuerpos = cuerpos
        else:
            raise ValueError("La cantidad de cuerpos debe ser un número entero mayor a cero")

    # Puertas izquierdas (True o False)
    def get_puertas_izquierdas(self):
        return self._puertas_izquierdas

    def set_puertas_izquierdas(self, puertas_izquierdas):
        if isinstance(puertas_izquierdas, bool):
            self._puertas_izquierdas = puertas_izquierdas
        else:
            raise ValueError("Puertas izquierdas debe ser True o False")

    def lado_de_abordaje(self):
        if self._puertas_izquierdas:
            return "izquierda"
        return "derecha"

    # Reglas supuestas (el diagrama no las define): el bus troncal cobra la tarifa base y tarda 3 minutos por tramo
    def calcular_tarifa(self, tarifa_base):
        return tarifa_base

    def tiempo_estimado(self, tramos):
        return tramos * 3

    def descripcion(self):
        return (
            f"{super().descripcion()} - Tipo: Troncal - Cuerpos: {self._cuerpos} - "
            f"Abordaje por la {self.lado_de_abordaje()}"
        )
