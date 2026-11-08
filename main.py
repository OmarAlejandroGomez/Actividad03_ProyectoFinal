

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
        print(f"{error}. Intenta nuevamente.")

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


        