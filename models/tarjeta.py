


class Tarjeta:

    def __init__(self, numero):
        self.set_numero(numero)
        self._saldo = 0
        self._bloqueado = False         # atributo protegido (#) en el diagrama
        self._motivo_bloqueo = ""       # atributo protegido (#) en el diagrama

    # Número
    def get_numero(self):
        return self._numero

    def set_numero(self, numero):
        if numero.strip() != "":
            self._numero = numero.strip().upper()
        else:
            raise ValueError("El número de la tarjeta no puede estar vacío")

    # Saldo (solo cambia con recargar y cobrar)
    def get_saldo(self):
        return self._saldo

    def get_bloqueado(self):
        return self._bloqueado

    def get_motivo_bloqueo(self):
        return self._motivo_bloqueo

    # Bloquear y desbloquear: el diagrama define los atributos, pero estos métodos permiten modificarlos
    def bloquear(self, motivo):
        if motivo.strip() == "":
            raise ValueError("Debe indicar el motivo del bloqueo")
        self._bloqueado = True
        self._motivo_bloqueo = motivo.strip()

    def desbloquear(self):
        self._bloqueado = False
        self._motivo_bloqueo = ""

    def recargar(self, monto):
        """Suma el monto al saldo y devuelve el nuevo saldo."""
        if not isinstance(monto, int) or monto <= 0:
            raise ValueError("El monto de la recarga debe ser un número entero mayor a cero")
        self._saldo += monto
        return self._saldo

    def validar_pago(self, tarifa):
        """True si la tarjeta no está bloqueada y su saldo alcanza para pagar la tarifa."""
        return not self._bloqueado and self._saldo >= tarifa

    def cobrar(self, tarifa):
        """Descuenta la tarifa completa del saldo y la devuelve. Si no se puede pagar, lanza una excepción.
        Con tarifa 0 (bus alimentador) no se descuenta nada, pero la tarjeta no debe estar bloqueada."""
        if self._bloqueado:
            raise TarjetaBloqueadaError(self._numero, self._motivo_bloqueo)

        if not self.validar_pago(tarifa):
            raise SaldoInsuficienteError(self._numero, self._saldo, tarifa)

        self._saldo -= tarifa
        return tarifa

    def descripcion(self):
        estado = f"Bloqueada ({self._motivo_bloqueo})" if self._bloqueado else "Activa"
        return f"Tarjeta {self._numero} - Saldo: ${self._saldo} - Estado: {estado}"
