class Estacion:
    
    def __init__(self, codigo, nombre, zona, accesible):
        self.set_codigo(codigo)
        self.set_nombre(nombre)
        self.set_zona(zona)
        self.set_accesible(accesible)
        self._ingresos = 0
        
    # Código
    def get_codigo(self):
        return self._codigo
    
    def set_codigo(self, codigo):
        if codigo.strip() != "":
            self._codigo = codigo.strip().upper()
        else:
            raise ValueError("El código de la estación no puede estar vacío.")
    
    # Nombre
    def get_nombre(self):
        return self._nombre
    
    def set_nombre(self, nombre):
        if nombre.strip() != "":
            self._nombre = nombre.strip()
        else:
            raise ValueError("El nombre de la estación no puede estar vacío.")
    
    # Zona
    def get_zona(self):
        return self._zona

    def set_zona(self, zona):
        if zona.strip() != "":
            self._zona = zona.strip()
        else:
            raise ValueError("La zona de la estación no puede estar vacía.")
    
    # Accesible
    def get_accesible(self):
        return self._accesible
    
    def set_accesible(self, accesible):
        if isinstance(accesible, bool):
            self._accesible = accesible
        else:
            raise ValueError("El valor de accesible debe ser True o False.")
    
    # Ingresos
    def get_ingresos(self):
        return self._ingresos
    
    def registrar_ingreso(self):
        self._ingresos += 1
        
    def descripcion(self):
        accesibilidad = "Sí" if self._accesible else "No"
        return f"Estación {self._codigo} - {self._nombre} - Zona: {self._zona} - Accesible: {accesibilidad}, Ingresos: {self._ingresos}"
    
