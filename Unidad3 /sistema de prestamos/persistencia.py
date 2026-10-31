import json
import os
from datos import alumnos, admins, computadoras, historial, necesidades_software, reservas

RUTA = os.path.join(os.path.dirname(__file__), "prestamos_datos.json")

def cargar_datos():
    if not os.path.exists(RUTA):
        return  # primera vez: se queda con los datos iniciales
    with open(RUTA, "r", encoding="utf-8") as f:
        datos = json.load(f)
    alumnos[:] = datos["alumnos"]
    admins[:] = datos["admins"]
    computadoras[:] = datos["computadoras"]
    historial[:] = datos.get("historial", [])
    necesidades_software[:] = datos.get("necesidades_software", [])
    reservas[:] = datos.get("reservas", [])

    #borrar despues de pruebas
    for pc in computadoras:
        if pc.get("estado") == "Reservada":
            reservas.append({"id_pc": pc["id"],
                             "usuario": pc["usuario"],
                             "fecha": pc["fecha_reserva"]})
            pc["estado"] = "Disponible"
            pc["usuario"] = ""
        pc.pop("fecha_reserva", None)
        #ESte bloque for es para que borremos los datos viejos que estan en el json
def guardar_datos():
    datos = {"alumnos": alumnos, "admins": admins, "computadoras": computadoras,
             "historial": historial,  "necesidades_software": necesidades_software,
             "reservas": reservas}
    with open(RUTA, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
