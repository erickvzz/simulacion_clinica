from registro import (crear_persona, registrar_paciente, registrar_medico,
                      programar_cita, registrar_atencion)
from registro import validar_fecha
from consultas import buscar_medicos_por_especialidad, historial_de_paciente


def datos_iniciales():
    pacientes, medicos, citas = [], [], []
    registrar_paciente(pacientes, "P001", "Ana Torres", "34")
    registrar_medico(medicos, "M001", "Luis Rojas", "Pediatría")
    return pacientes, medicos, citas


def test_caso_normal_cita_creada():
    pacientes, medicos, citas = datos_iniciales()
    mensaje = programar_cita(citas, pacientes, medicos,
                             "C001", "P001", "M001", "2026-11-10")
    assert "Cita creada correctamente" in mensaje
    assert len(citas) == 1


def test_extremos_de_edad():
    pacientes = []
    assert "correctamente" in registrar_paciente(pacientes, "P002", "Bebe Uno", "0")
    assert "correctamente" in registrar_paciente(pacientes, "P003", "Abuela Dos", "120")
    assert "entre 0 y 120" in registrar_paciente(pacientes, "P004", "Fuera Uno", "-1")
    assert "entre 0 y 120" in registrar_paciente(pacientes, "P005", "Fuera Dos", "121")
    assert len(pacientes) == 2


def test_edad_no_numerica():
    pacientes = []
    assert "Error" in registrar_paciente(pacientes, "P006", "Texto Edad", "abc")
    assert pacientes == []


def test_codigo_duplicado():
    pacientes, medicos, citas = datos_iniciales()
    assert "ya está registrado" in registrar_paciente(pacientes, "P001", "Otra Persona", "20")
    assert len(pacientes) == 1


def test_referencia_invalida():
    pacientes, medicos, citas = datos_iniciales()
    assert "no existe un paciente" in programar_cita(
        citas, pacientes, medicos, "C002", "P999", "M001", "2026-11-10")
    assert citas == []


def test_varias_citas_y_fecha_invalida():
    pacientes, medicos, citas = datos_iniciales()
    programar_cita(citas, pacientes, medicos, "C001", "P001", "M001", "2026-11-10")
    programar_cita(citas, pacientes, medicos, "C002", "P001", "M001", "2026-11-11")
    assert len(citas) == 2
    assert "no es válida" in programar_cita(
        citas, pacientes, medicos, "C003", "P001", "M001", "30/02/2026")


def test_historial_uno_y_cero():
    pacientes, medicos, citas = datos_iniciales()
    historial = {}
    registrar_atencion(historial, pacientes, "P001", "Control general")
    assert historial_de_paciente(historial, "P001") == ["Control general"]
    assert historial_de_paciente(historial, "P002") == []


def test_busqueda_por_especialidad():
    pacientes, medicos, citas = datos_iniciales()
    assert len(buscar_medicos_por_especialidad(medicos, "pediatría")) == 1
    assert buscar_medicos_por_especialidad(medicos, "Cardiología") == []


def test_privacidad_y_tipo_invalido():
    pacientes, medicos, citas = datos_iniciales()
    assert "Torres" not in pacientes[0].resumen()
    assert "A** T*****" in pacientes[0].resumen()
    try:
        crear_persona("enfermero", "E001", "Nombre Ficticio", "x")
        assert False
    except ValueError:
        pass


def test_codigos_y_nombres_se_corrigen_o_rechazan():
    pacientes, medicos, citas = datos_iniciales()

    # Prefijo en minúscula: se rechaza; el nombre sí se corrige
    assert "en mayúscula" in registrar_paciente(
        pacientes, "p003", "María Gómez", "30")

    assert "P003: M**** G****" in registrar_paciente(
        pacientes, "P003", "maría gómez", "30")

    # Formato malo: se rechaza
    assert "formato C001" in programar_cita(
        citas, pacientes, medicos, "C001,P001,M001", "P001", "M001", "2026-11-10")

    assert "solo debe tener letras" in registrar_paciente(
        pacientes, "P004", "Ana123", "20")

    assert "no es válida" in programar_cita(
        citas, pacientes, medicos, "C002", "P001", "M001", "hola")

    assert citas == []


def test_fechas_en_varios_formatos():
    for escrita in ("11/11/26", "11/11/2026", "2026/11/11",
                    "2026-11-11", "11-11-26"):
        assert validar_fecha(escrita) == "2026-11-11"

    for mala in ("2026-02-30", "31/04/2026", "hola", "11/2026"):
        try:
            validar_fecha(mala)
            assert False
        except ValueError:
            pass


if __name__ == "__main__":
    pruebas = [f for n, f in list(globals().items()) if n.startswith("test_")]

    for prueba in pruebas:
        prueba()
        print("OK ", prueba.__name__)

    print(f"\nTodas las pruebas ({len(pruebas)}) pasaron correctamente.")