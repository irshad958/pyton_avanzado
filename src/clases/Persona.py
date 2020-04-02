from abc import ABC, abstractmethod


class PersonaAbstracta(ABC): # abstract class PersonaAbstracta

    def __init__(self, edad, nombre):
        self.nombre = nombre
        self.edad = edad

    @abstractmethod
    def saludar(self):
        pass

    def get_nombre(self):
        return self.nombre

    def get_edad(self):
        return self.edad


class Persona(PersonaAbstracta):
    cant_personas = 0

    def __init__(self):
        super().__init__(0, "sin nombre")
        self.color_de_cabello = "Negro"
        Persona.cant_personas += 1

    def saludar(self):
        print(f" Hola")

    def obtener_edad(self):
        # self -> this en java
        return self.edad

    def set_edad(self, edad):
        self.edad = edad

    @staticmethod
    def imprimir_cant_personas():
        print(f"La cant de personas es {Persona.cant_personas}")


class Trabajador(Persona):

    def __init__(self):
        super().__init__()  # Persona

        self.lugar_de_trabajo = "Retailcompass"

    def obtener_edad(self):
        super().obtener_edad()
        return f"{self._edad + 1}"


if __name__ == '__main__':
    a = Persona()
    b = Persona()
    a.saludar()
    b.saludar()
    print(f"la edad es: {a.edad}")
    Persona.imprimir_cant_personas()
