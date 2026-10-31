from equipos import consultar_computadoras, buscar_soft, agreg_comp
from usuarios import agre_alu_o_admi, pedir_num_control, existe_usuario, es_admin
from prestamos import solic_pres, devo_comp, crea_reserv, historial_prest, liberar_reservas_vencidas
from estadisticas import mostrar_estadisticas, software_necesidad
from datos import alumnos, admins

def sistema_de_prestamo (num_control):
  while True:
    liberar_reservas_vencidas()
    print("\n==============================")
    print("      Sistema de prestamos  ")
    print("================================")
    print("1. Consultar computadoras y estados")
    print("2. Buscar por software")
    print("3. Solicitar prestamo")
    print("4. Devolver computadora o cancelar reservacion")
    print("5. Crear reservacion")
    print("6. Agregar computadora")
    print("7. Agregar alumno o admin")
    print("8. Historial de prestamos")
    print("9. Estadisticas")
    print("10. Necesidades de software")
    print("11. Cambiar de cuenta")
    print("12. Salir")
    try:
      opcion = int(input("Seleccione una opcion: "))
    except ValueError:
      print("Error, debe ingresar un numero correspondiente al menu")
      continue

    if opcion == 1:
      consultar_computadoras()
    elif opcion == 2:
      buscar_soft(num_control)
    elif opcion == 3:
      solic_pres(num_control)
    elif opcion == 4:
      devo_comp(num_control)
    elif opcion == 5:
     crea_reserv(num_control)
    elif opcion == 6:
      agreg_comp(num_control)
    elif opcion == 7:
      agre_alu_o_admi()
    elif opcion == 8:
      historial_prest(num_control)
    elif opcion == 9:
      mostrar_estadisticas(num_control)
    elif opcion == 10:
      software_necesidad(num_control)
    elif opcion == 11:
      nuevo_control = pedir_num_control()
      if existe_usuario(nuevo_control):
        num_control = nuevo_control
      else:
        print("El alumno o admi no existe")
    elif opcion == 12:
      for i in alumnos:
        if i['nume_control'] == num_control:
          print(f"Saliendo del sistema... Hasta luego {i['nombre']}")
      for i in admins:
        if i['nume_control'] == num_control:
          print(f"Saliendo del sistema... Hasta luego {i['nombre']}")
      break
    else:
      print("Opcion no valida")