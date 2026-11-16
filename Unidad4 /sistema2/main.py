from persistencia import cargar_datos
from prestamos import liberar_reservas_vencidas
from menu import sistema_de_prestamo
from usuarios import pedir_num_control, existe_usuario


def main():

  cargar_datos()
  liberar_reservas_vencidas()


  num_control =  pedir_num_control()
  if existe_usuario(num_control):
    sistema_de_prestamo(num_control)
  else:
      print("El alumno o admi no existe")

if __name__ == "__main__":
    main()