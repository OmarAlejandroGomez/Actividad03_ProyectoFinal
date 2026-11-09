from controllers.pasajero_controller import PasajeroController
from controllers.tarjeta_controller import TarjetaController
from models.sistema_transporte import SistemaTransporte
from models.estacion import Estacion
from models.ruta import Ruta
from models.bus_troncal import BusTroncal
from models.bus_alimentador import BusAlimentador
from models.cable_bus import CableBus
from models.utilidades import convertir_hora
from models.excepciones import (TarjetaBloqueadaError,SaldoInsuficienteError,EstacionNoPerteneceARutaError,FueraDeHorarioError)


def elegir_con_descripcion(elementos, descripciones, mensaje_vacio):
    
    if len(elementos) == 0:
        print(mensaje_vacio)
        return None
    
    posicion = 1
    for descripcion in descripciones:
        print(f"{posicion}. {descripcion}")
        posicion += 1
    
    while True:
        opcion = int(input("Elige el número de la lista: "))
        if opcion >= 1 and opcion <= len(elementos):
            return elementos[opcion - 1]
        print("Opción fuera de la lista")
    
def elegir_estacion(sistema, mensaje="Primero debe registrar estaciones."):
    estaciones = sistema.get_estaciones()
    descripciones = [f"{estacion.get_codigo()} - {estacion.get_nombre()}" for estacion in estaciones]
    return elegir_con_descripcion(estaciones, descripciones, mensaje)

def elegir_ruta(sistema):
    rutas = sistema.get_rutas()
    descripciones = [f"{ruta.get_codigo()} - {ruta.get_nombre()}" for ruta in rutas]
    return elegir_con_descripcion(rutas, descripciones, "Primero debe registrar una ruta.")

def elegir_vehiculo(vehiculos, mensaje_vacio):
    descripciones = [f"{vehiculo.get_codigo()} (Capacidad: {vehiculo.get_capacidad()}" for vehiculo in vehiculos]
    return elegir_con_descripcion(vehiculos, descripciones, mensaje_vacio)

def pedir_si_no(mensaje):
   return input(mensaje + " (s/n): ").strip().lower() == 's'

def buscar_tarjeta_perdida(tarjeta_controller):
    numero = input("Ingrese el número de la tarjeta perdida: ")
    tarjeta = tarjeta_controller.buscar_tarjeta(numero)
    if tarjeta is None:
        print("No existe una tarjeta con ese número.")
    return tarjeta

def agregar_estacion(sistema):
    codigo = input("Ingrese el código de la estación: ")
    nombre = input("Ingrese el nombre de la estación: ")
    zona = input("Ingrese la zona: ")
    accesible = pedir_si_no("¿La estación es accesible?")
    
    try:
        sistema.agregar_estacion(codigo, nombre, zona, accesible)
        print("Estación agregada exitosamente.")
        return
    except ValueError as error:
        print(f"{error}. Intenta nuevamente.\n")

def agregar_ruta(sistema):
    if len(sistema.get_estaciones()) < 2:
        print("Debe haber al menos dos estaciones registradas para crear una ruta.")
        return
    
    while True:
        codigo = input("Ingrese el código de la ruta: ")
        nombre = input("Ingrese el nombre de la ruta: ")
        cantidad = int(input("¿Cuantas estaciones tendrá la ruta?: "))
        
        estaciones = []
        for numero in range(1, cantidad + 1):
            print(f"Estación {numero}:")
            estacion = elegir_estacion(sistema)
            estaciones.append(estacion)

        hora_inicio = input("Ingrese la hora de inicio de operación (HH:MM): ")
        hora_fin = input("Ingrese la hora de fin de operación (HH:MM): ")
        frecuencia = int(input("Ingrese cada cuantos minutos sale un vehículo: "))
        
        try:
            ruta = Ruta(codigo, nombre, estaciones, hora_inicio, hora_fin, frecuencia   )        
            sistema.agregar_ruta(ruta)
            print("Ruta agregada exitosamente.")
            return
        except ValueError as error:
            print(f"{error}. Intenta nuevamente. \n")

def agregar_vehiculo(sistema):
    ruta = elegir_ruta(sistema)
    if ruta is None:
        return

    print("Tipo de vehículo: 1. Bus troncal   2. Bus alimentador   3. Cable Bus")
    tipo = input("Elige el tipo: ")
    if tipo != "1" and tipo != "2" and tipo != "3":
        print("Tipo de vehículo inválido")
        return

    while True:
        codigo = input("Ingresa el código del vehículo: ")
        capacidad = int(input("Ingresa la capacidad de pasajeros: "))

        try:
            if tipo == "1":
                cuerpos = int(input("Ingresa la cantidad de cuerpos: "))
                puertas_izquierdas = pedir_si_no("¿Tiene puertas del lado izquierdo?")
                vehiculo = BusTroncal(codigo, capacidad, cuerpos, puertas_izquierdas)
            if tipo == "2":
                barrio = input("Ingresa el barrio que atiende: ")
                paradas_fijas = int(input("Ingresa la cantidad de paradas fijas: "))
                vehiculo = BusAlimentador(codigo, capacidad, barrio, paradas_fijas)
              
            else:
                parada = input("Ingresa la parada única: ")
                minutos_trayecto = int(input("Ingresa los minutos de trayecto: "))
                vehiculo = CableBus(codigo, capacidad, parada, minutos_trayecto)

            sistema.agregar_vehiculo(vehiculo, ruta)
            print("Vehículo agregado con éxito")
            return
        except ValueError as error:
            print(f"{error}. Intenta nuevamente.\n")


def agregar_pasajero(pasajero_controller):
    while True:
        documento = input("Ingresa el documento: ")
        nombre = input("Ingresa el nombre: ")
        perfil = input("Ingresa el perfil (General, Estudiante, Adulto mayor...): ")

        try:
            pasajero_controller.add_pasajero(documento, nombre, perfil)
            print("Pasajero agregado con éxito")
            return
        except ValueError as error:
            print(f"{error}. Intenta nuevamente.\n")


def asignar_tarjeta(pasajero_controller, tarjeta_controller):
    documento = input("Ingresa el documento del pasajero: ")
    pasajero = pasajero_controller.buscar_pasajero(documento)
    if pasajero is None:
        print("No existe un pasajero con ese documento")
        return

    numero = input("Ingresa el número de la nueva tarjeta: ")
    try:
        tarjeta_controller.add_tarjeta(pasajero, numero)
        print("Tarjeta asignada con éxito")
    except ValueError as error:
        print(f"No se pudo asignar la tarjeta: {error}")



def recargar_tarjeta(tarjeta_controller):
    tarjeta = buscar_tarjeta_perdida(tarjeta_controller)
    if tarjeta is None:
        return

    monto = int(input("Ingresa el monto a recargar: "))
    try:
        nuevo_saldo = tarjeta.recargar(monto)
        print(f"Recarga exitosa. Nuevo saldo: ${nuevo_saldo}")
    except ValueError as error:
        print(f"No se pudo recargar: {error}")


def realizar_viaje(sistema, tarjeta_controller):
    tarjeta = buscar_tarjeta_perdida(tarjeta_controller)
    if tarjeta is None:
        return

    vehiculo = elegir_vehiculo(sistema.get_flota(), "Primero debe registrar un vehículo")
    if vehiculo is None:
        return

    print("Estación de origen:")
    origen = elegir_estacion(sistema)
    print("Estación de destino:")
    destino = elegir_estacion(sistema)

    try:
        hora = convertir_hora(input("Ingresa la hora del viaje (HH:MM): "))
        viaje = sistema.realizar_viaje(tarjeta, vehiculo, origen, destino, hora)
        print("Viaje realizado con éxito")
        print(viaje.resumen())
        if viaje.get_valor() == 0:
            print("Este vehículo no cobra tarifa: solo se registró el ingreso con la tarjeta")
    except TarjetaBloqueadaError as error:
        print(f"No se pudo realizar el viaje: {error}")
    except SaldoInsuficienteError as error:
        print(f"No se pudo realizar el viaje: {error}. Recarga la tarjeta e intenta de nuevo.")
    except EstacionNoPerteneceARutaError as error:
        print(f"No se pudo realizar el viaje: {error}")
    except FueraDeHorarioError as error:
        print(f"No se pudo realizar el viaje: {error}")
    except ValueError as error:
        print(f"No se pudo realizar el viaje: {error}")


def elegir_alimentador(sistema):
    alimentadores = [v for v in sistema.get_flota() if isinstance(v, BusAlimentador)]
    return elegir_vehiculo(alimentadores, "No existen buses alimentadores registrados")


def cambiar_barrio(sistema):
    vehiculo = elegir_alimentador(sistema)
    if vehiculo is None:
        return

    nuevo_barrio = input("Ingresa el nuevo barrio: ")
    try:
        vehiculo.cambiar_barrio(nuevo_barrio)
        print("Barrio actualizado con éxito")
    except ValueError as error:
        print(f"No se pudo modificar: {error}")



def mostrar_estaciones(sistema):
    estaciones = sistema.get_estaciones()
    if not estaciones:
        print("No existen estaciones registradas")
        return
    for estacion in estaciones:
        print(estacion.descripcion())



def mostrar_rutas(sistema):
    rutas = sistema.get_rutas()
    if not rutas:
        print("No existen rutas registradas")
        return

    for ruta in rutas:
        print(ruta.descripcion())


def mostrar_flota(sistema):
    """Un solo ciclo recorre todos los vehículos; cada objeto ejecuta SU versión de descripcion()."""
    flota = sistema.get_flota()
    if not flota:
        print("No existen vehículos registrados")
        return

    for vehiculo in flota:
        print(vehiculo.descripcion())


def mostrar_pasajeros(pasajero_controller):
    pasajeros = pasajero_controller.get_pasajeros()
    if not pasajeros:
        print("No existen pasajeros registrados")
        return

    for pasajero in pasajeros:
        print(pasajero.descripcion())


def mostrar_tarjetas(tarjeta_controller):
    tarjetas = tarjeta_controller.get_tarjetas()
    if not tarjetas:
        print("No existen tarjetas registradas")
        return

    for tarjeta in tarjetas:
        print(tarjeta.descripcion())



def mostrar_viajes(sistema):
    viajes = sistema.get_viajes()
    if not viajes:
        print("No se han realizado viajes")
        return

    for viaje in viajes:
        print(viaje.resumen())


def mostrar_recaudo(sistema):
    print(f"Recaudo total del sistema {sistema.get_nombre()}: ${sistema.recaudo_total()}")


def mostrar_reporte_estaciones(sistema):
    reporte = sistema.reporte_estaciones()
    if not reporte:
        print("No existen estaciones registradas")
        return

    print("Estaciones ordenadas por ingresos (de mayor a menor):")
    for linea in reporte:
        print(linea)


def mostrar_proximas_salidas(sistema):
    ruta = elegir_ruta(sistema)
    if ruta is None:
        return

    try:
        desde = convertir_hora(input("Ingresa la hora desde la cual buscar (HH:MM): "))
        cantidad = int(input("¿Cuántas salidas quieres ver?: "))
    except ValueError as error:
        print(f"Dato inválido: {error}")
        return

    salidas = ruta.get_programacion().proximas_salidas(desde, cantidad)
    if not salidas:
        print("No hay más salidas programadas a partir de esa hora")
        return

    print("Próximas salidas: " + ", ".join(salida.strftime("%H:%M") for salida in salidas))


def intentar_viaje(sistema, tarjeta, vehiculo, origen, destino, hora_texto):
    """Ayuda de la demostración: intenta un viaje y muestra el resultado o el error."""
    try:
        viaje = sistema.realizar_viaje(tarjeta, vehiculo, origen, destino, convertir_hora(hora_texto))
        print(f"Viaje realizado -> {viaje.resumen()}")
    except TarjetaBloqueadaError as error:
        print(f"Rechazado (tarjeta bloqueada): {error}")
    except SaldoInsuficienteError as error:
        print(f"Rechazado (saldo insuficiente): {error}")
    except EstacionNoPerteneceARutaError as error:
        print(f"Rechazado (estación fuera de la ruta): {error}")
    except FueraDeHorarioError as error:
        print(f"Rechazado (fuera de horario): {error}")



def ejecutar_demostracion(sistema, pasajero_controller, tarjeta_controller):
    if len(sistema.get_estaciones()) > 0:
        print("La demostración solo se ejecuta cuando el sistema está vacío")
        return

    print("\n1) Estaciones y rutas")
    portal = Estacion("E01", "Portal Norte", "Norte", True)
    calle100 = Estacion("E02", "Calle 100", "Norte", True)
    calle72 = Estacion("E03", "Calle 72", "Centro", False)
    centro = Estacion("E04", "Centro", "Centro", True)
    for estacion in (portal, calle100, calle72, centro):
        sistema.agregar_estacion(estacion)

    troncal = Ruta("T01", "Troncal Norte-Centro", [portal, calle100, calle72, centro], "05:00", "22:00", 10)
    alimentadora = Ruta("A01", "Alimentadora Suba", [portal, calle100], "06:00", "20:00", 15)
    sistema.agregar_ruta(troncal)
    sistema.agregar_ruta(alimentadora)
    mostrar_rutas(sistema)

    print("\n2) Flota (cada vehículo calcula su tarifa y tiempo de forma distinta)")
    bus_troncal = BusTroncal("BT-01", 80, 2, True)
    bus_alimentador = BusAlimentador("BA-01", 30, "Suba", 6)
    sistema.agregar_vehiculo(bus_troncal, troncal)
    sistema.agregar_vehiculo(bus_alimentador, alimentadora)
    mostrar_flota(sistema)

    print("\n3) Pasajeros y tarjetas (todas las tarjetas son iguales: pagan la tarifa completa)")
    datos = [("1001", "Ana Ruiz", "Estudiante", "TJ-1001", 10000),
             ("1002", "Luis Gómez", "General", "TJ-1002", 1000),
             ("1003", "Marta Díaz", "Adulto mayor", "TJ-1003", 20000),
             ("1004", "Pedro Pardo", "General", "TJ-1004", 20000)]
    tarjetas = {}
    for documento, nombre, perfil, numero, saldo in datos:
        pasajero = pasajero_controller.add_pasajero(documento, nombre, perfil)
        tarjeta = tarjeta_controller.add_tarjeta(pasajero, numero)
        tarjeta.recargar(saldo)
        tarjetas[documento] = tarjeta
    mostrar_pasajeros(pasajero_controller)

    print("\n4) Viajes válidos")
    intentar_viaje(sistema, tarjetas["1001"], bus_troncal, portal, centro, "08:30")
    intentar_viaje(sistema, tarjetas["1003"], bus_troncal, portal, calle72, "08:40")
    print("El alimentador no cobra: registra el ingreso con la tarjeta, pero el saldo no cambia")
    intentar_viaje(sistema, tarjetas["1004"], bus_alimentador, portal, calle100, "09:00")
    print(tarjetas["1004"].descripcion())

    print("\n5) Situaciones excepcionales (el programa continúa después de cada una)")
    intentar_viaje(sistema, tarjetas["1002"], bus_troncal, portal, centro, "09:00")         # saldo insuficiente
    tarjetas["1004"].bloquear("Reportada como perdida")
    intentar_viaje(sistema, tarjetas["1004"], bus_alimentador, portal, calle100, "09:10")   # bloqueada (aunque no cobre)
    intentar_viaje(sistema, tarjetas["1003"], bus_alimentador, portal, centro, "09:00")     # estación fuera de la ruta
    intentar_viaje(sistema, tarjetas["1003"], bus_alimentador, portal, calle100, "23:30")   # fuera de horario

    print("\n6) Se resuelven los problemas y se repiten los viajes")
    tarjetas["1004"].desbloquear()
    intentar_viaje(sistema, tarjetas["1004"], bus_alimentador, portal, calle100, "09:10")
    tarjetas["1002"].recargar(5000)
    intentar_viaje(sistema, tarjetas["1002"], bus_troncal, portal, centro, "09:00")

    print("\n7) Informes")
    mostrar_tarjetas(tarjeta_controller)
    mostrar_recaudo(sistema)
    mostrar_reporte_estaciones(sistema)
    salidas = troncal.get_programacion().proximas_salidas(convertir_hora("08:25"), 3)
    print("Próximas salidas de T01 desde las 08:25: " + ", ".join(s.strftime("%H:%M") for s in salidas))

    print("\nLa demostración terminó sin interrupciones")



def main():
    sistema = SistemaTransporte("TransMetro", 3000)
    pasajero_controller = PasajeroController()
    tarjeta_controller = TarjetaController()

    while True:
        print(f"\n {sistema.get_nombre()} - Opciones")
        print("1. Agregar estación")
        print("2. Agregar ruta")
        print("3. Agregar vehículo")
        print("4. Registrar pasajero")
        print("5. Asignar tarjeta a un pasajero")
        print("6. Recargar tarjeta")
        print("7. Realizar viaje")
        print("8. Cambiar barrio (bus alimentador)")
        print("9. Mostrar estaciones")
        print("10. Mostrar rutas")
        print("11. Mostrar flota")
        print("12. Mostrar pasajeros")
        print("13. Mostrar tarjetas")
        print("14. Mostrar viajes")
        print("15. Mostrar recaudo total")
        print("16. Reporte de estaciones")
        print("17. Próximas salidas de una ruta")
        print("18. Ejecutar demostración")
        print("19. Salir\n")

        option = input("Selecciona una opción: ")

        match option:
            case "1":
                agregar_estacion(sistema)

            case "2":
                agregar_ruta(sistema)

            case "3":
                agregar_vehiculo(sistema)

            case "4":
                agregar_pasajero(pasajero_controller)

            case "5":
                asignar_tarjeta(pasajero_controller, tarjeta_controller)

            case "6":
                recargar_tarjeta(tarjeta_controller)

            case "7":
                realizar_viaje(sistema, tarjeta_controller)

            case "8":
                cambiar_barrio(sistema)

            case "9":
                mostrar_estaciones(sistema)

            case "10":
                mostrar_rutas(sistema)

            case "11":
                mostrar_flota(sistema)

            case "12":
                mostrar_pasajeros(pasajero_controller)

            case "13":
                mostrar_tarjetas(tarjeta_controller)

            case "14":
                mostrar_viajes(sistema)

            case "15":
                mostrar_recaudo(sistema)

            case "16":
                mostrar_reporte_estaciones(sistema)

            case "17":
                mostrar_proximas_salidas(sistema)

            case "18":
                ejecutar_demostracion(sistema, pasajero_controller, tarjeta_controller)

            case "19":
                print("Vuelve pronto")
                break

            case _:
                print("Opción inválida")


if __name__ == "__main__":
    main()
