class TransporteError(Exception):
    """Clase base para errores relacionados con el transporte."""
    pass


class TarjetaBloqueadaError(TransporteError):
    """Excepción para indicar que una tarjeta está bloqueada."""


    def __init__(self, numero, motivo):
        self.numero = numero
        self.motivo = motivo
        super().__init__(f"La tarjeta {numero} está bloqueada. Motivo: {motivo}")

class SaldoInsuficienteError(TransporteError):
    """Excepción para indicar que el saldo de la tarjeta es insuficiente."""

    def __init__(self, numero, saldo, valor):
        self.numero = numero
        self.saldo = saldo
        self.valor = valor
        super().__init__(f"Saldo insuficiente en la tarjeta {numero}. Saldo actual: {saldo}, Tarifa requerida: {valor}")


class EstacionNoPerteneceARutaError(TransporteError):
    """Excepción para indicar que una estación no pertenece a la ruta."""

    def __init__(self, nombre_estacion, codigo_ruta):
        self.nombre_estacion = nombre_estacion
        self.codigo_ruta = codigo_ruta
        super().__init__(f"La estación {nombre_estacion} no pertenece a la ruta {codigo_ruta}.")

class FueraDeHorarioError(TransporteError):
    """Excepción para indicar que se intenta abordar fuera del horario permitido."""

    def __init__(self, codigo_ruta, hora):
        self.codigo_ruta = codigo_ruta
        self.hora = hora
        super().__init__(f"La Ruta: {codigo_ruta}, no opera a la Hora: {hora.strftime('%H:%M')}.")