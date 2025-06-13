import datetime


class Venda:
    def __init__(self, cliente, produtos, valor_total):
        self.cliente = cliente
        self.produtos = produtos
        self.valor_total = valor_total
        self.data_hora = datetime.now()

    def __str__(self):
        produtos_nomes = ', '.join(produto.nome for produto in self.produtos)
        return f"Venda em {self.data_hora.strftime('%d/%m/%Y %H:%M:%S')} - Cliente: {self.cliente.nome} - Produtos: {produtos_nomes} - Valor Total: R$ {self.valor_total:.2f}"
