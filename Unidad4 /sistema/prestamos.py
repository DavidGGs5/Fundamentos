from datetime import datetime, timedelta, timezone
from datos import computadoras, historial, necesidades_software, reservas
from persistencia import guardar_datos
from equipos import (buscar_computadora_por_id, buscar_pc_de_usuario, reserva_de_usuario, reserva_en_fecha, tiene_software)
from usuarios import es_alumno, es_admin

ZONA = timezone(timedelta(hours=-6))

def solic_pres(num_control):
  hoy_txt = datetime.now(ZONA).strftime("%d/%m/%Y")

  if es_alumno(num_control):
        pc_actual = buscar_pc_de_usuario(num_control)
        if pc_actual is not None:
            print(f"Ya tienes asignada la {pc_actual['id']}")
            return
        r = reserva_de_usuario(num_control, hoy_txt)
        if r is not None:
            print(f"Tienes una reservación para hoy: {r['id_pc']}.")
            resp = input("¿Retirarla ahora? Presiona S para aceptar: ")
            if resp.strip().lower() == "s":
                pc = buscar_computadora_por_id(r["id_pc"])
                if pc["estado"] == "Disponible":
                    reservas.remove(r)
                    pc["estado"] = "Prestada"
                    pc["usuario"] = num_control
                    historial.append({"usuario": num_control,
                                      "computadora": pc["id"],
                                      "software": r.get("software", ""),
                                      "tipo": "Prestada",
                                      "fecha_tramite": datetime.now(ZONA).strftime("%d/%m/%Y %H:%M")})
                    guardar_datos()
                    print(f"Reservación retirada. Computadora: {pc['id']} | Aula: {pc['aula']}")
                else:
                    print("Esa computadora no está disponible ahora.")
            return

  programa = input("\nIngrese el software que desea: ").strip().lower()
  if not programa:                        # evita que Enter vacio coincida con todo
    print("Debe escribir un programa.")
    return
  encontrado = False
  for i in computadoras:
    programas = []
    for s in i["software"].split(","):  #split transofrma los datos en forma de lista
      programas.append(s.strip().lower())

    if programa.lower() in programas:
      encontrado = True
      if i["estado"] == "Disponible" and reserva_en_fecha(i["id"], hoy_txt) is None:
        i["estado"] = "Prestada"
        i["usuario"] = num_control
        historial.append({"usuario": num_control,
                          "computadora": i["id"],
                          "software": programa,
                          "tipo": "Prestada",
                          "fecha_tramite": datetime.now(ZONA).strftime("%d/%m/%Y %H:%M")})
        print("Préstamo registrado correctamente a favor del alumno.", num_control)
        print(f"Computadora: {i['id']} | Aula: {i['aula']}")
        guardar_datos()
        return
  if encontrado:
    print("Hay computadoras con ese software, pero ninguna esta disponible ahora.")
  else:
    print("No existe ninguna computadora con ese software.")
    propuesta = input(f"¿Quieres registrar {programa} como un software a futuro?"
                      f" Presiona S para aceptar o N para rechazar: ")
    if propuesta.lower() == "s":
      necesidades_software.append({"usuario": num_control,
                                  "software": programa,
                                  "fecha": datetime.now(ZONA).strftime("%d/%m/%Y %H:%M")})
      guardar_datos()
      print("El software se puso en lista de solcitado a espera de verificar")
      return
    else:
      print("No se registro nada")


def devo_comp(num_control):
    print("\n--- DEVOLVER COMPUTADORA ---")
    id_computadora = input("Ingrese el ID de la computadora: ")
    i = buscar_computadora_por_id(id_computadora)
    if i is None:
        print("La computadora no existe.")
        return

    if i["estado"] == "Prestada":
      if i["usuario"] == num_control or es_admin(num_control):
        i["estado"] = "Disponible"
        i["usuario"]= ""
        print("Computadora devuelta correctamente.")
        print(f"Computadora: {i['id']} | Aula: {i['aula']}")
        guardar_datos()
        return

    mias = [r for r in reservas if r["usuario"] == num_control]
    propias = [r for r in mias if r["id_pc"] == i["id"]]
    if not propias:
        print("Esta computadora no está prestada ni reservada a este usuario.")
        return

    a_borrar = propias
    if es_admin(num_control) and len(mias) > len(propias):
        op = input("Tienes más reservaciones. 1 = solo las de esta PC, 2 = todas las tuyas: ").strip()
        if op == "2":
            a_borrar = mias

    for r in a_borrar:
        reservas.remove(r)
    guardar_datos()
    print(f"Reservación(es) cancelada(s) correctamente: {len(a_borrar)}")
        

def crea_reserv(num_control):
  if es_alumno(num_control):
    r = reserva_de_usuario(num_control)
    if r is not None:
        print(f"Ya tienes una reservación: {r['id_pc']} para el {r['fecha']}")
        return

  print("\n--- CREAR RESERVACIÓN ---")
  hoy = datetime.now(ZONA).date()
  limite_maximo = hoy + timedelta(days=3)
  print("Hoy es:", hoy.strftime("%d/%m/%Y"))
  print("")
  print("Puedes reservar hasta:", limite_maximo.strftime("%d/%m/%Y"))
  print("")

  programa = input("\nIngrese el software que desea: ").strip().lower()
  if not programa:                        # evita que Enter vacio coincida con todo
    print("Debe escribir un programa.")
    return

  fecha_solicitada = input("Fecha que quieres reservar (DD/MM/YYYY): ")
  try:
      fecha_reservacion = datetime.strptime(fecha_solicitada, "%d/%m/%Y").date()
  except ValueError:
      print("Error: El formato de fecha no es válido. Debe ser DD/MM/YYYY.")
      return
  if fecha_reservacion < hoy:
      print("No puedes solicitar la computadora para fechas pasadas.")
      return
  if fecha_reservacion > limite_maximo:
      print("La fecha excede el límite permitido:", limite_maximo.strftime("%d/%m/%Y"))
      return
  fecha_txt = fecha_reservacion.strftime("%d/%m/%Y")

  if (es_alumno(num_control) and fecha_reservacion == hoy
          and buscar_pc_de_usuario(num_control) is not None):
      print("Ya tienes una computadora prestada hoy, no puedes reservar para hoy.")
      return

  encontrado = False
  for i in computadoras:
      if not tiene_software(i, programa):
          continue
      encontrado = True
      if i["estado"] == "Mantenimiento":
          continue
      if fecha_reservacion == hoy and i["estado"] == "Prestada":
          continue
      if reserva_en_fecha(i["id"], fecha_txt) is not None:
          continue

      reservas.append({"id_pc": i["id"], "usuario": num_control,
                        "fecha": fecha_txt, "software": programa})
      historial.append({"usuario": num_control,
                        "computadora": i["id"],
                        "software": programa,
                        "tipo": "Reservada",
                        "fecha_tramite": datetime.now(ZONA).strftime("%d/%m/%Y %H:%M"),
                        "fecha_programada": fecha_txt})
      guardar_datos()
      print("\n==============================================")
      print(" ¡Reservación registrada con éxito!")
      print(f" Computadora: {i['id']} (Aula: {i['aula']})")
      print(f" Reservada para: {num_control}")
      print(f" Fecha programada: {fecha_txt}")
      print("==============================================")
      return

  if encontrado:
      print("No hay computadoras con ese software libres para esa fecha.")
  else:
      print("No existe ninguna computadora con ese software.")


def liberar_reservas_vencidas():
    hoy = datetime.now(ZONA).date()
    vigentes = []

    for r in reservas:
        fecha_reserva = datetime.strptime(r["fecha"], "%d/%m/%Y").date()
        if fecha_reserva >= hoy:
            vigentes.append(r)

    if len(vigentes) != len(reservas):
        reservas[:] = vigentes
        guardar_datos()

def historial_prest(num_control):
  print("\n--- HISTORIAL DE PRÉSTAMOS ---")
  control_admin = es_admin(num_control)
  varcontrol = False
  for t in reversed(historial):
    if control_admin or t["usuario"] == num_control:
      registro = (f"{t["fecha_tramite"]} | Usuario: {t["usuario"]} | Computadora: {t["computadora"]} | "
                  f" {t["software"]} | Tipo: {t["tipo"]}")
      if "fecha_programada" in t:
        registro += f" | Para el: {t['fecha_programada']}"
      print(registro)
      varcontrol = True
  if not varcontrol:
      print("No hay registros en el historial.")

def devolver_pc(id_pc, num_control):
    pc = buscar_computadora_por_id(id_pc)
    if pc is None:
        return False, "La computadora no existe."
    if pc["estado"] != "Prestada":
        return False, "Esa computadora no está prestada."
    if pc["usuario"] != num_control and not es_admin(num_control):
        return False, "Solo puedes devolver tu propia computadora."
    pc["estado"] = "Disponible"
    pc["usuario"] = ""
    guardar_datos()
    return True, f"Computadora {pc['id']} devuelta correctamente."


def cancelar_reserva(id_pc, fecha, num_control):
    r = reserva_en_fecha(id_pc, fecha)
    if r is None:
        return False, "Esa reservación no existe."
    if r["usuario"] != num_control and not es_admin(num_control):
        return False, "Solo puedes cancelar tus propias reservaciones."
    reservas.remove(r)
    guardar_datos()
    return True, f"Reservación de {id_pc} para el {fecha} cancelada."



def solicitar_prestamo(num_control, programa):
    hoy_txt = datetime.now(ZONA).strftime("%d/%m/%Y")
    programa = programa.strip().lower()
    if not programa:
        return False, "Debe escribir un programa."

    if es_alumno(num_control):
        pc_actual = buscar_pc_de_usuario(num_control)
        if pc_actual is not None:
            return False, f"Ya tienes asignada la {pc_actual['id']}."
        r = reserva_de_usuario(num_control, hoy_txt)
        if r is not None:
            return False, f"Tienes una reservación para hoy ({r['id_pc']}); primero hay que retirarla."

    encontrado = False
    for pc in computadoras:
        if not tiene_software(pc, programa):
            continue
        encontrado = True
        if pc["estado"] == "Disponible" and reserva_en_fecha(pc["id"], hoy_txt) is None:
            pc["estado"] = "Prestada"
            pc["usuario"] = num_control
            historial.append({"usuario": num_control,
                              "computadora": pc["id"],
                              "software": programa,
                              "tipo": "Prestada",
                              "fecha_tramite": datetime.now(ZONA).strftime("%d/%m/%Y %H:%M")})
            guardar_datos()
            return True, f"Préstamo registrado: {pc['id']} | Aula: {pc['aula']}"

    if encontrado:
        return False, "Hay computadoras con ese software, pero ninguna está disponible ahora."
    return False, "No existe ninguna computadora con ese software."