from collections import Counter
from datos import historial, necesidades_software, alumnos
from usuarios import es_admin

# Estadisticas por programa, y por carrera

def estats(conteo):
  popular = conteo.most_common()
  posicion = 1
  for p in popular:
    soft = p[0]
    veces = p[1]
    print(f"  {posicion}. {soft} — {veces} solicitud(es)")
    posicion += 1


def mostrar_estadisticas(num_control):
    if not es_admin(num_control):
        print("Solo un admin puede ver las estadísticas.")
        return

    print("\n--- ESTADÍSTICAS DEL HISTORIAL ---")
    if not historial:
        print("Aún no hay registros en el historial.")
        return
    else:
      print(f"Total de trámites: {len(historial)}")

    print("\n------ Estadisticas por programa ------")
    software = Counter()
    for t in historial:
      for s in t["software"].split(","):
        software[s.strip().lower()] += 1
    estats(software)

    print("\n------ Estadisticas por carrera ------")
    carrera_alum = {}
    for a in alumnos:
      numero = a["nume_control"]
      carrera = a["carrera"]
      carrera_alum[numero] = carrera
    can_car = Counter()
    for t in historial:
      carrera = carrera_alum.get(t["usuario"])
      if carrera:
        can_car[carrera] += 1
    if can_car:
      estats(can_car)
    else:
      print("Sin tramites de alumnos aun")

def software_necesidad(num_control):
  if not es_admin(num_control):
    print("Debes ser admin para tener acceso")
    return
  print("\n ------ NECESIDADES DE SOFTWARE NO EXISTENTE -----")
  if not necesidades_software:
    print("No hay registros aun")
    return
  conteo = Counter()
  for n in necesidades_software:
    nombre = n["software"].strip().lower()
    conteo[nombre] += 1
  popular = conteo.most_common()
  posicion = 1
  for p in popular:
    soft = p[0]
    veces = p[1]
    print(f"  {posicion}. {soft} — {veces} solicitud(es)")
    posicion += 1