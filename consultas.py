def buscar_medicos_por_especialidad(medicos, especialidad):
    return list(filter(
        lambda medico: medico.especialidad.lower() == especialidad.lower(),
        medicos))


def citas_de_paciente(citas, codigo_paciente):
    return list(filter(
        lambda cita: cita.paciente.codigo == codigo_paciente, citas))


def historial_de_paciente(historial, codigo_paciente):
    return list(historial.get(codigo_paciente, []))


def resumenes(objetos):
    return list(map(lambda objeto: objeto.resumen(), objetos))


def total_atenciones(historial):
    return sum(map(len, historial.values()))