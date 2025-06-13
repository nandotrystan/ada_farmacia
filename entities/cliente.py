
from datetime import datetime


class Cliente:
    def __init__(self, cpf, nome, data_nascimento):
        self.__cpf = self.validar_cpf(cpf)
        self.nome = nome
        self.data_nascimento = datetime.strptime(data_nascimento, "%d/%m/%Y")

    @property
    def cpf(self):
        return self.__cpf

    @staticmethod
    def validar_cpf(cpf):
        cpf = cpf.replace('.', '').replace('-', '')
        if len(cpf) != 11 or not cpf.isdigit():
            raise ValueError("CPF inválido")
        return cpf