from datetime import datetime, date, timedelta
from models.utilidades import convertir_hora

class ProgramacionHoraria:
    
    def __init__(self, hora_inicio, hora_fin, frecuencia):
        self.set_horas(hora_inicio, hora_fin)
        self.set_frecuencia(frecuencia)
    
    def get_hora_inicio(self):
        return self._hora_inicio
    
    def get_hora_fin(self):
        return self._hora_fin
    
    def set_horas(self, hora_inicio, hora_fin):
        inicio = convertir_hora(hora_inicio)
        fin = convertir_hora(hora_fin)
        if fin > inicio:
            self._hora_inicio = inicio
            self._hora_fin = fin
        else:
            raise ValueError("La hora de fin debe ser posterior a la hora de inicio.")
    
    # Frecuencia
    def get_frecuencia(self):
        return self._frecuencia 
    
    def set_frecuencia(self, frecuencia):
        if isinstance(frecuencia, int) and frecuencia > 0:
            self._frecuencia = frecuencia
        else:
            raise ValueError("La frecuencia debe ser un número entero positivo.")
    
    def opera_a(self, hora):
        return self._hora_inicio <= hora <= self._hora_fin
    
    def proximas_salidas(self, desde, cantidad):
        salida = datetime.combine(date.today(), self._hora_inicio)
        fin = datetime.combine(date.today(), self._hora_fin)
        limite = datetime.combine(date.today(), desde)
        
        salidas = []
        while salida <= fin and len(salidas) < cantidad:
            if salida >= limite:
                salidas.append(salida.time())
            salida = salida + timedelta(minutes=self._frecuencia)
        return salidas
    
    def descripcion(self):
        return (
            f"Opera de {self._hora_inicio.strftime('%H:%M')} a {self._hora_fin.strftime('%H:%M')} "
            f"con salidas cada {self._frecuencia} minutos."
        )
        
    