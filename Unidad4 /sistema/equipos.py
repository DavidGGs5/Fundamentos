from usuarios import es_admin
from datos import computadoras, necesidades_software, reservas
from persistencia import guardar_datos
from datetime import datetime, timedelta, timezone

ZONA = timezone(timedelta(hours=-6))

def consultar_computadoras():
  print("\n--- COMPUTADORAS ---")
  for i in (computadoras):
    print(f"| Aula: {i["aula"]} | ID: {i["id"]} | Software: {i["software"]} | Estado: {i["estado"]} | Usuario: {i["usuario"]}")
    propias = []
    for r in reservas:
        if r["id_pc"] == i["id"]:
            propias.append(r)
    propias.sort(key=lambda r: datetime.strptime(r["fecha"], "%d/%m/%Y"))
    partes = []
    for r in propias:
        partes.append(f"{r['fecha']} ({r['usuario']})")
    texto = "\n".join(partes)
    if propias:
        print(f"| Reservas: {texto}")
    print("---------------------")


def buscar_soft(num_control):
    programa = input("\nIngrese el software que desea buscar: ")
    print("\n--- RESULTADOS ---")
    encontrado = False
    for i in computadoras:
        if programa.lower() in i["software"].lower():
            print(f"ID: {i['id']} | Aula: {i['aula']} | Software: {i['software']} | Estado: {i['estado']}")
            encontrado = True
    if encontrado == False:
        print("No se encontraron computadoras con ese software.")
        propuesta = input(f"¿Quieres registrar {programa} como un software a futuro?"
                          f" Presiona S para aceptar: ")
        if propuesta.lower() == "s":
          necesidades_software.append({"usuario": num_control,
                                      "software": programa,
                                      "fecha": datetime.now(ZONA).strftime("%d/%m/%Y %H:%M")})
          guardar_datos()
          print("El software se puso en lista de solcitado a espera de verificar")
          return
        else:
          print("No se registro nada")


def buscar_computadora_por_id(id_comp):
    for i in computadoras:
        if i["id"] == id_comp:
            return i
    return None


def buscar_pc_de_usuario(num_control):
    for pc in computadoras:
        if pc["usuario"]  == num_control:
            return pc
    return None

def tiene_software(pc, programa):
    lista = []
    for s in pc["software"].split(","):
        lista.append(s.strip().lower())
    return programa in lista

def reserva_en_fecha(id_pc, fecha):
    """Devuelve la reserva de esa PC en esa fecha (DD/MM/YYYY), o None."""
    for r in reservas:
        if r["id_pc"] == id_pc and r["fecha"] == fecha:
            return r
    return None

def reserva_de_usuario(num_control, fecha=None):
    """Primera reserva del usuario (solo de esa fecha si se indica), o None."""
    for r in reservas:
        if r["usuario"] == num_control and (fecha is None or r["fecha"] == fecha): 
                                            #Si la fecha se asigna deja de ser None, y se verifica 
                                            # que esta no sea igual, proposito: no bloquear una compu
                                            # para un alumno por ese tiempo prolongado
            return r
    return None

def agreg_comp(num_control):
  if not es_admin(num_control):
        print("Solo un admin puede agregar computadoras.")
        return
  print("\n--- AGREGAR COMPUTADORA ---")
  id_computadora = input("ID de la computadora: ")
  if buscar_computadora_por_id(id_computadora) is not None:
      print("Error: Ya existe una computadora con ese ID.")
      return
  aula = input("Aula: ")
  aulas = {pc["aula"] for pc in computadoras}
  if aula not in aulas:
      print("Esta aula no existe")
      return
  soow = input("Software instalado: ")
  nueva_pc = {
      "id": id_computadora,
      "aula": aula,
      "software": soow,
      "estado": "Disponible",
      "usuario": ""
  }
  computadoras.append(nueva_pc)
  computadoras.sort(key=lambda i: (i.get("aula", ""), i.get("id", "")))
  guardar_datos()
  print("\nComputadora agregada correctamente.")