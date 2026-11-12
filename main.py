from registro import (registrar_paciente, registrar_medico, programar_cita,
                      registrar_atencion, mostrar_menu, validar_codigo,
                      validar_nombre, validar_edad, validar_especialidad,
                      validar_fecha, validar_nota, buscar_por_codigo)
from consultas import (buscar_medicos_por_especialidad, historial_de_paciente,
                       citas_de_paciente, total_atenciones)


ANCHO = 44


def mostrar_caja(titulo, lineas):
    print("\n" + f" {titulo.upper()} ".center(ANCHO, "-"))
    for linea in lineas:
        print(linea)
    print("-" * ANCHO)


def mostrar_seccion(titulo, bloques, vacio):
    print("\n" + f" {titulo.upper()} ".center(ANCHO, "="))
    if not bloques:
        print(vacio)
    for i, lineas in enumerate(bloques):
        if i > 0:
            print()
        for linea in lineas:
            print(linea)
    print("=" * ANCHO)


def mostrar_resultado(mensaje, titulo, coleccion):
    # Si hubo error imprime el mensaje; si no, muestra el último registro
    if mensaje.startswith("Error"):
        print(mensaje)
    else:
        mostrar_caja(titulo, coleccion[-1].detalle())


def pedir(mensaje, validador, *extra):
    # Repite la pregunta hasta que el dato sea válido
    while True:
        try:
            return validador(input(mensaje), *extra)
        except ValueError as error:
            print("Error:", error)


def main():
    pacientes, medicos, citas, historial = [], [], [], {}

    while True:
        print(mostrar_menu())
        opcion = input("Elija una opción: ").strip()

        if opcion == "1":
            mensaje = registrar_paciente(
                pacientes,
                pedir("Código del paciente: ", validar_codigo, "P"),
                pedir("Nombre: ", validar_nombre),
                pedir("Edad: ", validar_edad))
            mostrar_resultado(mensaje, "Paciente registrado", pacientes)
        elif opcion == "2":
            mensaje = registrar_medico(
                medicos,
                pedir("Código del médico: ", validar_codigo, "M"),
                pedir("Nombre: ", validar_nombre),
                pedir("Especialidad: ", validar_especialidad))
            mostrar_resultado(mensaje, "Médico registrado", medicos)
        elif opcion == "3":
            mensaje = programar_cita(
                citas, pacientes, medicos,
                pedir("Código de la cita: ", validar_codigo, "C"),
                pedir("Código del paciente: ", validar_codigo, "P"),
                pedir("Código del médico: ", validar_codigo, "M"),
                pedir("Fecha: ", validar_fecha))
            mostrar_resultado(mensaje, "Cita registrada", citas)
        elif opcion == "4":
            codigo = pedir("Código del paciente: ", validar_codigo, "P")
            nota = pedir("Nota de la atención: ", validar_nota)
            mensaje = registrar_atencion(historial, pacientes, codigo, nota)
            if mensaje.startswith("Error"):
                print(mensaje)
            else:
                paciente = buscar_por_codigo(pacientes, codigo)
                mostrar_caja("Atención registrada",
                             [f"Paciente : {paciente.nombre_oculto} - {codigo}",
                              f"Nota : {nota}"])
        elif opcion == "5":
            encontrados = buscar_medicos_por_especialidad(
                medicos, input("Especialidad a buscar: ").strip())
            mostrar_seccion("Médicos encontrados",
                            [m.detalle() for m in encontrados],
                            "No se encontraron médicos con esa especialidad.")
        elif opcion == "6":
            codigo = pedir("Código del paciente: ", validar_codigo, "P")
            mostrar_seccion("Citas programadas",
                            [c.detalle() for c in citas_de_paciente(citas, codigo)],
                            "No tiene citas programadas.")
            paciente = buscar_por_codigo(pacientes, codigo)
            nombre = f"Paciente : {paciente.nombre_oculto} - {codigo}" if paciente else f"Paciente : {codigo} (no registrado)"
            notas = historial_de_paciente(historial, codigo)
            mostrar_seccion("Atenciones registradas",
                            [[nombre, f"Nota : {n}"] for n in notas],
                            "El paciente no tiene atenciones registradas.")
        elif opcion == "7":
            print(f"Atenciones registradas: {total_atenciones(historial)}")
            break
        else:
            print("Error: opción no válida. Elija un número del 1 al 7.")


if __name__ == "__main__":
    main()