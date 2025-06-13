from datetime import datetime

class Medicamento:
    def __init__(self, nome, principal_composto, laboratorio, descricao, preco):
        self.nome = nome
        self.principal_composto = principal_composto
        self.laboratorio = laboratorio
        self.descricao = descricao
        self.preco = preco
    def __str__(self):
        return f"{self.nome} - {self.principal_composto} - {self.laboratorio.nome} - {self.descricao} - R$ {self.preco:.2f}"


class MedicamentoQuimioterápico(Medicamento):
    def __init__(self, nome, principal_composto, laboratorio, descricao, preco, necessita_receita):
        super().__init__(nome, principal_composto, laboratorio, descricao, preco)
        self.necessita_receita = necessita_receita



class MedicamentoFitoterápico(Medicamento):
    def __init__(self, nome, principal_composto, laboratorio, descricao, preco):
        super().__init__(nome, principal_composto, laboratorio, descricao, preco)

class Venda:
    def __init__(self, cliente, produtos, valor_total):
        self.cliente = cliente
        self.produtos = produtos
        self.valor_total = valor_total
        self.data_hora = datetime.now()

    def __str__(self):
        produtos_nomes = ', '.join(produto.nome for produto in self.produtos)
        return f"Venda em {self.data_hora.strftime('%d/%m/%Y %H:%M:%S')} - Cliente: {self.cliente.nome} - Produtos: {produtos_nomes} - Valor Total: R$ {self.valor_total:.2f}"
