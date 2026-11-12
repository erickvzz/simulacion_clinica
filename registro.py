import re
from datetime import date
from modelos import Paciente, Medico, Cita


# ---------- Validaciones: rechazan datos mal escritos y corrigen los nombres ----------

def validar_codigo(texto, letra):
    # Formato: la letra indicada en MAYÚSCULA + 3 números (P001, M001, C001)
    codigo = texto.strip()
    if not re.fullmatch(letra + r"\d{3}", codigo):
        raise ValueError(f"El código debe tener el formato {letra}001: letra {letra} "
                         f"en mayúscula y 3 números, sin espacios ni comas.")
    return codigo


def validar_nombre(texto):
    palabras = texto.split()
    if not palabras or not all(p.isalpha() for p in palabras):
        raise ValueError("El nombre solo debe tener letras (ejemplo: Ana Torres).")
    return " ".join(palabras).title()


def validar_edad(valor):
    try:
        edad = int(valor)
    except ValueError:
        raise ValueError("La edad debe ser un número entero entre 0 y 120.")
    if not 0 <= edad <= 120:
        raise ValueError("La edad debe ser un número entero entre 0 y 120.")
    return edad


def validar_especialidad(texto):
    palabras = texto.split()
    if not palabras or not all(p.isalpha() for p in palabras):
        raise ValueError("La especialidad solo debe tener letras (ejemplo: Pediatría).")
    return " ".join(palabras).capitalize()


def validar_fecha(texto):
    mensaje = "La fecha no es válida. Ejemplos: 10/11/2026, 10/11/26 o 2026-11-10."
    partes = re.split(r"[-/.]", texto.strip())
    if len(partes) != 3 or not all(p.isdigit() for p in partes):
        raise ValueError(mensaje)
    if len(partes[0]) == 4:
        anio, mes, dia = partes
    else:
        dia, mes, anio = partes
    if len(anio) == 2:
        anio = "20" + anio
    if len(anio) != 4:
        raise ValueError(mensaje)
    try:
        return date(int(anio), int(mes), int(dia)).isoformat()
    except ValueError:
        raise ValueError(mensaje)


def validar_nota(texto):
    if not texto.strip():
        raise ValueError("La nota no puede estar vacía.")
    return texto.strip()


# ---------- Paradigma estructurado: funciones, listas y diccionarios ----------

def crear_persona(tipo, codigo, nombre, dato):
    # Factory: crea Paciente (dato = edad) o Medico (dato = especialidad)
    if tipo == "paciente":
        return Paciente(codigo, nombre, dato)
    if tipo == "medico":
        return Medico(codigo, nombre, dato)
    raise ValueError("Tipo de persona no válido.")


def buscar_por_codigo(lista, codigo):
    for elemento in lista:
        if elemento.codigo == codigo:
            return elemento
    return None


def registrar_paciente(pacientes, codigo, nombre, edad):
    try:
        codigo = validar_codigo(codigo, "P")
        nombre = validar_nombre(nombre)
        edad = validar_edad(edad)
    except ValueError as error:
        return f"Error: {error}"
    if buscar_por_codigo(pacientes, codigo):
        return f"Error: el código {codigo} ya está registrado."
    paciente = crear_persona("paciente", codigo, nombre, edad)
    pacientes.append(paciente)
    return f"Paciente registrado correctamente: {paciente.resumen()}"


def registrar_medico(medicos, codigo, nombre, especialidad):
    try:
        codigo = validar_codigo(codigo, "M")
        nombre = validar_nombre(nombre)
        especialidad = validar_especialidad(especialidad)
    except ValueError as error:
        return f"Error: {error}"
    if buscar_por_codigo(medicos, codigo):
        return f"Error: el código {codigo} ya está registrado."
    medico = crear_persona("medico", codigo, nombre, especialidad)
    medicos.append(medico)
    return f"Médico registrado correctamente: {medico.resumen()}"


def programar_cita(citas, pacientes, medicos, codigo_cita,
                   codigo_paciente, codigo_medico, fecha):
    try:
        codigo_cita = validar_codigo(codigo_cita, "C")
        codigo_paciente = validar_codigo(codigo_paciente, "P")
        codigo_medico = validar_codigo(codigo_medico, "M")
        fecha = validar_fecha(fecha)
    except ValueError as error:
        return f"Error: {error}"
    paciente = buscar_por_codigo(pacientes, codigo_paciente)
    if paciente is None:
        return f"Error: no existe un paciente con código {codigo_paciente}."
    medico = buscar_por_codigo(medicos, codigo_medico)
    if medico is None:
        return f"Error: no existe un médico con código {codigo_medico}."
    if buscar_por_codigo(citas, codigo_cita):
        return f"Error: el código de cita {codigo_cita} ya está registrado."
    cita = Cita(codigo_cita, paciente, medico, fecha)
    citas.append(cita)
    return f"Cita creada correctamente: {cita.resumen()}"


def registrar_atencion(historial, pacientes, codigo_paciente, nota):
    # El historial es un diccionario: código de paciente -> lista de notas
    try:
        codigo_paciente = validar_codigo(codigo_paciente, "P")
        nota = validar_nota(nota)
    except ValueError as error:
        return f"Error: {error}"
    if buscar_por_codigo(pacientes, codigo_paciente) is None:
        return f"Error: no existe un paciente con código {codigo_paciente}."
    historial.setdefault(codigo_paciente, []).append(nota)
    return f"Atención registrada para el paciente {codigo_paciente}."


def mostrar_menu():
    return """
--- SISTEMA KAWSAY ---
1. Registrar paciente
2. Registrar médico
3. Programar cita
4. Registrar atención
5. Buscar médicos por especialidad
6. Consultar historial de un paciente
7. Salir
"""