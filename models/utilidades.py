from datetime import datetime

def convertir_hora(texto):
    try:
        return datetime.strptime(texto, "%H:%M").time()
    except ValueError:
        raise ValueError("La hora debe tener el formato HH:MM (ejemplo: 17:30).")
