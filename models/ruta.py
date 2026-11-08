from models.estacion import Estacion

class Ruta:
    
    def __init__(self, codigo, nombre, estaciones, hora_inicio, hora_fin, frecuencia):
        self.set_codigo(codigo)
        self.set_nombre(nombre)
        self.set_estaciones(estaciones)
        
        # Composición
        self._programacion = ProgramacionHoraria(hora_inicio, hora_fin, frecuencia)
        
    # Código
    def get_codigo(self):
        return self._codigo
    
    def set_codigo(self, codigo):
        if codigo.strip() != "":
            self._codigo = codigo.strip().upper()
        else:
            raise ValueError("El código de la ruta no puede estar vacío.")
    
    # Nombre
    def get_nombre(self):
        return self._nombre
    
    def set_nombre(self, nombre):
        if nombre.strip() != "":
            self._nombre = nombre.strip()
        else:
            raise ValueError("El nombre de la ruta no puede estar vacío.")
        
    # Estaciones
    def get_estaciones(self):
        return self._estaciones.copy()
    
    def set_estaciones(self, estaciones):
        if len(estaciones) < 2:
            raise ValueError("La ruta debe tener al menos dos estaciones.")
        
        codigos_vistos = []
        for estacion in estaciones:
            if estacion.get_codigo() in codigos_vistos:
                raise ValueError(f"La estación con código {estacion.get_codigo()} ya está en la ruta.")
            codigos_vistos.append(estacion.get_codigo())
        
        self._estaciones = list(estaciones)  # Crear una copia de la lista 
    
    # Programación horaria
    def get_programacion(self):
        return self._programacion
    
    def _posicion(self, estacion):
        posicion = 0
        for e in self._estaciones:
            if e.get_codigo() == estacion.get_codigo():
                return posicion
            posicion += 1
        return -1
    
    def contiene(self, estacion):
        return self._posicion(estacion) != -1
    
    def validar_horario(self, hora):
        return self._programacion.opera_a(hora)
    
    def descripcion(self):
        nombres = [estacion.get_nombre() for estacion in self._estaciones]
        return (
            f"Ruta {self._codigo} - {self._nombre} - Estaciones: {' -> '.join(nombres)} - "
            f"{self._programacion.descripcion()}"
        )