from datos import alumnos, admins
from persistencia import guardar_datos



def pedir_num_control(mensaje="Ingresa tu numero de control: "):
    try:
        return int(input(mensaje))
    except ValueError:
        return None

def es_alumno(num_control):
    return any(a["nume_control"] == num_control for a in alumnos)

def es_admin(num_control):
    return any(a["nume_control"] == num_control for a in admins)

def existe_usuario(num_control):
    return es_alumno(num_control) or es_admin(num_control)


def agre_alu_o_admi():
    print("\n--- A quien vas a agregar ----")
    try:
        opcic = int(input("1 para agregar alumno, 2 para agregar admin, 3 para cancelar: "))
    except ValueError:
        print("Ingrese una opcion valida")
        return

    if opcic == 3:
        return
    if opcic not in (1, 2):
        print("Opcion no valida")
        return

    num = pedir_num_control("Numero de control: ")
    if num is None:
        print("El numero de control debe ser numerico.")
        return
    if existe_usuario(num):
        print("Ese numero de control ya existe.")
        return
    nombre = input("Nombre: ").strip()   # strip quita espacios sobrantes

    if opcic == 1:
        carrera = input("Carrera: ").strip()
        alumnos.append({"nombre": nombre, "nume_control": num, "carrera": carrera})
        print(f"El alumno {nombre} fue agregado con exito")
    elif opcic == 2:
        ocupacion = input("Ocupacion: ").strip()
        admins.append({"nombre": nombre, "nume_control": num, "ocupacion": ocupacion})
        print(f"El admin {nombre} fue agregado con exito")
    guardar_datos()