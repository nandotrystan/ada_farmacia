from entities import Cliente, MedicamentoQuimioterápico, MedicamentoFitoterápico, Laboratorio, Venda

import datetime


class Farmacia:
    def __init__(self):
        self.clientes = []
        self.medicamentos = []
        self.vendas = []
        self.atendimentos_realizados = 0
        self.remedios_vendidos = {}
        self.remedios_quimioterapicos_vendidos = 0
        self.valor_quimioterapicos_vendidos = 0
        self.remedios_fitoterapicos_vendidos = 0
        self.valor_fitoterapicos_vendidos = 0

    def cadastrar_cliente(self, cpf, nome, data_nascimento):
        try:
            cliente = Cliente(cpf, nome, data_nascimento)
            self.clientes.append(cliente)
            print(f"Cliente {nome} cadastrado com sucesso.")
        except ValueError as e:
            print(e)
            
    def cadastrar_medicamento_quimioterapico(self, nome, principal_composto, laboratorio, descricao, preco, necessita_receita):
        medicamento = MedicamentoQuimioterápico(nome, principal_composto, laboratorio, descricao, preco, necessita_receita)
        if any(m.nome == nome for m in self.medicamentos):
            print(f"Medicamento {nome} já cadastrado.")
            return
        self.medicamentos.append(medicamento)
        print(f"Medicamento Quimioterápico {nome} cadastrado com sucesso.")
    
    def cadastrar_medicamento_fitoterapico(self, nome, principal_composto, laboratorio, descricao, preco):
        medicamento = MedicamentoFitoterápico(nome, principal_composto, laboratorio, descricao, preco)
        if any(m.nome == nome for m in self.medicamentos):
            print(f"Medicamento {nome} já cadastrado.")
            return
        self.medicamentos.append(medicamento)
        print(f"Medicamento Fitoterápico {nome} cadastrado com sucesso.")
    
    def realizar_venda(self, cpf_cliente, produtos):
        cliente = next((c for c in self.clientes if c.cpf == cpf_cliente), None)
        if not cliente:
            print("Cliente não encontrado.")
            return
        valor_total = sum(produto.preco for produto in produtos)
        desconto = 0
        if (datetime.now() - cliente.data_nascimento).days // 365 > 65:
            desconto = max(desconto, 0.20 * valor_total)
        if valor_total > 150:
            desconto = max(desconto, 0.10 * valor_total)
        valor_total -= desconto
        if valor_total < 0:
            valor_total = 0
        venda = Venda(cliente, produtos, valor_total)
        self.vendas.append(venda)
        self.atendimentos_realizados += 1
        for produto in produtos:
            if isinstance(produto, MedicamentoQuimioterápico):
                self.remedios_quimioterapicos_vendidos += 1
                self.valor_quimioterapicos_vendidos += produto.preco
            elif isinstance(produto, MedicamentoFitoterápico):
                self.remedios_fitoterapicos_vendidos += 1
                self.valor_fitoterapicos_vendidos += produto.preco
            if isinstance(produto, MedicamentoQuimioterápico) and produto.necessita_receita:
                print(f"Alerta: Verifique a receita do medicamento {produto.nome}.")
        self.remedios_vendidos[venda] = self.remedios_vendidos.get(venda, 0) + 1
        print(f"Venda realizada com sucesso. Valor total: R$ {valor_total:.2f}")
    
    def relatorio_clientes(self):
        clientes_ordenados = sorted(self.clientes, key=lambda c: c.nome)
        print("Relatório de Clientes:")
        for cliente in clientes_ordenados:
            print(f"CPF: {cliente.cpf}, Nome: {cliente.nome}, Data de Nascimento: {cliente.data_nascimento.strftime('%d/%m/%Y')}")
    
    def relatorio_medicamentos(self):
        medicamentos_ordenados = sorted(self.medicamentos, key=lambda m: m.nome)
        print("Relatório de Medicamentos:")
        for medicamento in medicamentos_ordenados:
            tipo = "Quimioterápico" if isinstance(medicamento, MedicamentoQuimioterápico) else "Fitoterápico"
            print(f"Nome: {medicamento.nome}, Tipo: {tipo}, Laboratório: {medicamento.laboratorio.nome},Preço: {medicamento.preco} Descrição: {medicamento.descricao}")
    
    def relatorio_medicamentos_tipo(self, tipo):
        if tipo == "quimioterapico":
            medicamentos = [m for m in self.medicamentos if isinstance(m, MedicamentoQuimioterápico)]
        elif tipo == "fitoterapico":
            medicamentos = [m for m in self.medicamentos if isinstance(m, MedicamentoFitoterápico)]
        else:
            print("Tipo de medicamento inválido.")
            return
        medicamentos_ordenados = sorted(medicamentos, key=lambda m: m.nome)
        print(f"Relatório de Medicamentos {tipo.capitalize()}:")
        for medicamento in medicamentos_ordenados:
            print(f"Nome: {medicamento.nome}, Laboratório: {medicamento.laboratorio.nome}, Preço: {medicamento.preco} Descrição: {medicamento.descricao}")
    def relatorio_estatisticas(self):
        if not self.vendas:
            print("Nenhuma venda realizada hoje.")
            return
        remedio_mais_vendido = max(self.remedios_vendidos.items(), key=lambda x: x[1], default=(None, 0))
        print("Estatísticas dos Atendimentos Realizados:")  
        print(f"Remédio mais vendido: {remedio_mais_vendido[0].produtos[0].nome if remedio_mais_vendido[0] else 'N/A'} - Quantidade: {remedio_mais_vendido[1]} - Valor Total: R$ {remedio_mais_vendido[0].valor_total:.2f}")
        print(f"Quantidade de pessoas atendidas: {self.atendimentos_realizados}")
        print(f"Número de remédios Quimioterápicos vendidos: {self.remedios_quimioterapicos_vendidos} - Valor Total: R$ {self.valor_quimioterapicos_vendidos:.2f}")
        print(f"Número de remédios Fitoterápicos vendidos: {self.remedios_fitoterapicos_vendidos} - Valor Total: R$ {self.valor_fitoterapicos_vendidos:.2f}")   
    def menu(self):
        while True:
            print("\nMenu Farmácia:")
            print("1. Cadastrar Cliente")
            print("2. Cadastrar Medicamento Quimioterápico")
            print("3. Cadastrar Medicamento Fitoterápico")
            print("4. Realizar Venda")
            print("5. Relatório de Clientes")
            print("6. Relatório de Medicamentos")
            print("7. Relatório de Medicamentos Quimioterápicos")
            print("8. Relatório de Medicamentos Fitoterápicos")
            print("9. Relatório de Estatísticas")
            print("0. Sair\n\n")
            opcao = input("Escolha uma opção: ")
            if opcao == '1':
                cpf = input("Digite o CPF do cliente: ")
                while True:
                    try:
                        Cliente.validar_cpf(cpf)  # Valida o CPF
                        break
                    except ValueError as e:
                        print(e)
                        cpf = input("Digite o CPF do cliente (sem pontuação): ").strip()
                nome = input("Digite o nome do cliente: ").strip().title()
                while True:
                    try:
                        data_nascimento = input("Digite a data de nascimento (dd/mm/yyyy): ")
                        datetime.strptime(data_nascimento, "%d/%m/%Y")  # Valida a data
                        break
                    except ValueError:
                        print("Data inválida. Por favor, use o formato dd/mm/yyyy.")    
                

                self.cadastrar_cliente(cpf, nome, data_nascimento)
            elif opcao == '2':
                nome = input("Digite o nome do medicamento Quimioterápico: ")
                principal_composto = input("Digite o principal composto: ")
                laboratorio_nome = input("Digite o nome do laboratório: ")
                laboratorio_endereco = input("Digite o endereço do laboratório: ")
                laboratorio_telefone = input("Digite o telefone do laboratório: ")
                laboratorio_cidade = input("Digite a cidade do laboratório: ")
                laboratorio_estado = input("Digite o estado do laboratório: ")
                laboratorio = Laboratorio(laboratorio_nome, laboratorio_endereco, laboratorio_telefone, laboratorio_cidade, laboratorio_estado)
                descricao = input("Digite a descrição do medicamento: ")
                while True:
                    try:
                        preco = float(input("Digite o preço do medicamento: "))
                        if preco < 0:
                            print("Preço inválido. O preço deve ser maior ou igual a zero.")
                        break
                    except ValueError:
                        print("Valor inválido. Por favor, digite um número.")
                        
                necessita_receita = input("Necessita receita? (s/n): ").lower() == 's'
                self.cadastrar_medicamento_quimioterapico(nome, principal_composto, laboratorio, descricao, preco, necessita_receita)
            elif opcao == '3':
                nome = input("Digite o nome do medicamento Fitoterápico: ")
                principal_composto = input("Digite o principal composto: ")
                laboratorio_nome = input("Digite o nome do laboratório: ")
                laboratorio_endereco = input("Digite o endereço do laboratório: ")
                laboratorio_telefone = input("Digite o telefone do laboratório: ")
                laboratorio_cidade = input("Digite a cidade do laboratório: ")
                laboratorio_estado = input("Digite o estado do laboratório: ")
                laboratorio = Laboratorio(laboratorio_nome, laboratorio_endereco, laboratorio_telefone, laboratorio_cidade, laboratorio_estado)
                descricao = input("Digite a descrição do medicamento: ")
                
                while True:
                    try:
                        preco = float(input("Digite o preço do medicamento: "))
                        if preco < 0:
                            print("Preço inválido. O preço deve ser maior ou igual a zero.")
                        break
                    except ValueError:
                        print("Valor inválido. Por favor, digite um número.")
                self.cadastrar_medicamento_fitoterapico(nome, principal_composto, laboratorio, descricao, preco)
            elif opcao == '4':
                cpf_cliente = input("Digite o CPF do cliente: ")
                produtos = []
                while True:
                    produto_nome = input("Digite o nome do produto (ou 'sair' para finalizar): ")
                    if produto_nome.lower() == 'sair':
                        break
                    produto_tipo = input("É um medicamento Quimioterápico ou Fitoterápico? (q/f): ").lower()
                    if produto_tipo == 'q':
                        medicamento = next((m for m in self.medicamentos if isinstance(m, MedicamentoQuimioterápico) and m.nome == produto_nome), None) 
                        if medicamento:
                            produtos.append(medicamento)
                        else:
                            print("Medicamento Quimioterápico não encontrado.")
                    elif produto_tipo == 'f':
                        medicamento = next((m for m in self.medicamentos if isinstance(m, MedicamentoFitoterápico) and m.nome == produto_nome), None)
                        if medicamento:
                            produtos.append(medicamento)
                        else:
                            print("Medicamento Fitoterápico não encontrado.")
                if produtos:
                    self.realizar_venda(cpf_cliente, produtos)
            elif opcao == '5':
                self.relatorio_clientes()
            elif opcao == '6':
                self.relatorio_medicamentos()
            elif opcao == '7':
                self.relatorio_medicamentos_tipo("quimioterapico")
            elif opcao == '8':
                self.relatorio_medicamentos_tipo("fitoterapico")
            elif opcao == '9':
                self.relatorio_estatisticas()
            elif opcao == '0':
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida. Tente novamente.")
                if __name__ == "__main__":
                    farmacia = Farmacia()
                    farmacia.menu()
                    
                break


