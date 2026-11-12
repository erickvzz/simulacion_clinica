def ocultar_nombre(nombre):
    # Privacidad: "Ana Torres" se muestra como "A** T*****"
    return " ".join(p[0] + "*" * (len(p) - 1) for p in nombre.split())


class Paciente:

    def __init__(self, codigo, nombre, edad):
        self._codigo = codigo
        self._nombre = nombre
        self.edad = edad  

    # Getters
    @property
    def codigo(self):
        return self._codigo

    @property
    def nombre_oculto(self):
        return ocultar_nombre(self._nombre)

    @property
    def edad(self):
        return self._edad

    # Setters
    @edad.setter
    def edad(self, valor):
        if not isinstance(valor, int) or not 0 <= valor <= 120:
            raise ValueError("La edad debe ser un número entre 0 y 120.")
        self._edad = valor

    # Metodos
    def detalle(self):
        return [f"Paciente : {self.nombre_oculto}",
                f"Código : {self.codigo}",
                f"Edad : {self.edad}"]

    def resumen(self):
        return f"Paciente {self.codigo}: {self.nombre_oculto} ({self.edad} años)"


class Medico:

    def __init__(self, codigo, nombre, especialidad):
        self._codigo = codigo
        self._nombre = nombre
        self.especialidad = especialidad  
    # Getters
    @property
    def codigo(self):
        return self._codigo

    @property
    def nombre_oculto(self):
        return ocultar_nombre(self._nombre)

    @property
    def especialidad(self):
        return self._especialidad

    # Setters
    @especialidad.setter
    def especialidad(self, valor):
        if not valor.strip():
            raise ValueError("Debe indicar una especialidad.")
        self._especialidad = valor

    # Metodos
    def detalle(self):
        return [f"Médico : {self.nombre_oculto}",
                f"Código : {self.codigo}",
                f"Especialidad : {self.especialidad}"]

    def resumen(self):
        return f"Medico {self.codigo}: {self.nombre_oculto} - {self.especialidad}"


class Cita:
    # Asociación con Paciente y agregación de Medico

    def __init__(self, codigo, paciente, medico, fecha):
        self._codigo = codigo
        self._paciente = paciente
        self._medico = medico
        self._fecha = fecha

    # Getters
    @property
    def codigo(self):
        return self._codigo

    @property
    def paciente(self):
        return self._paciente

    @property
    def medico(self):
        return self._medico

    @property
    def fecha(self):
        return self._fecha

    # Metodos
    def detalle(self):
        return [f"Fecha : {self.fecha}",
                f"Código de la cita : {self.codigo}",
                f"Paciente : {self.paciente.nombre_oculto} - {self.paciente.codigo}",
                f"Médico : {self.medico.nombre_oculto} - {self.medico.codigo}",
                f"Especialidad : {self.medico.especialidad}"]

    def resumen(self):
        return (f"Cita {self.codigo} el {self.fecha}: "
                f"{self.paciente.nombre_oculto} con médico {self.medico.codigo} "
                f"({self.medico.especialidad})")