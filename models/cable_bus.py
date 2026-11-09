from models.vehiculo import Vehiculo


class CableBus(Vehiculo):
    """Cabina de cable aéreo: va directo desde la estación de origen hasta su única parada."""

    def __init__(self, codigo, capacidad, parada, minutos_trayecto):
        super().__init__(codigo, capacidad)
        self.set_parada(parada)
        self.set_minutos_trayecto(minutos_trayecto)

    # Parada: el cable bus solo tiene una parada (no hace paradas intermedias)
    def get_parada(self):
        return self._parada

    def set_parada(self, parada):
        if parada.strip() != "":
            self._parada = parada.strip()
        else:
            raise ValueError("La parada del cable bus no puede estar vacía")

    # Minutos de trayecto: tiempo fijo que tarda en llegar a su única parada
    def get_minutos_trayecto(self):
        return self._minutos_trayecto

    def set_minutos_trayecto(self, minutos_trayecto):
        if isinstance(minutos_trayecto, int) and minutos_trayecto > 0:
            self._minutos_trayecto = minutos_trayecto
        else:
            raise ValueError("Los minutos de trayecto deben ser un número entero mayor a cero")

    def llega_a(self, nombre_estacion):
        """True si la estación indicada es la única parada del cable bus."""
        return nombre_estacion.strip().lower() == self._parada.lower()

    # Reglas: el cable bus cobra lo mismo que el alimentador (no cobra tarifa)
    # y, como va directo a su única parada, su tiempo es fijo sin importar los tramos
    def calcular_tarifa(self, tarifa_base):
        return 0

    def tiempo_estimado(self, tramos):
        return self._minutos_trayecto

    def descripcion(self):
        return (
            f"{super().descripcion()} - Tipo: Cable bus - Parada única: {self._parada} - "
            f"Trayecto: {self._minutos_trayecto} minutos"
        )