import os
import random
from datetime import datetime

# Obtém o diretório atual do arquivo Python
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
# Define o caminho completo para o arquivo de usuários
arquivo_usuarios = os.path.join(diretorio_atual, "usuarios.txt")
# Define o caminho completo para o arquivo de extrato
arquivo_extrato = os.path.join(diretorio_atual, "extrato.txt")


cotacoes = {
    "Bitcoin": 325751,   # Valor inicial
    "Ethereum": 15325,   # Valor inicial
    "Ripple": 2         # Valor inicial
}

# Função para exibir o resumo das informações do usuárioSSS
def exibir_resumo(cpf):
    usuarios = ler_usuarios()
    if cpf in usuarios:
        usuario = usuarios[cpf]
        print(f"CPF: {cpf}")
        print(f"Reais: R${usuario['saldo']:.2f}")
        for moeda in ["Bitcoin", "Ethereum", "Ripple"]:
            quantidade = usuario.get(moeda.lower(), 0)
            print(f"{moeda}: {quantidade:.8f}")
    else:
        print("CPF não encontrado.")


# Função para ler os usuários e saldos do arquivo
def ler_usuarios():
    usuarios = {}
    if os.path.exists(arquivo_usuarios):
        with open(arquivo_usuarios, "r") as j:
            for linha_numero, linha in enumerate(j, start=1):
                partes = linha.strip().split(":")
                if len(partes) >= 2:
                    cpf, senha = partes[:2]  # As duas primeiras partes são CPF e senha
                    saldo = float(partes[2]) if len(partes) > 2 else 0.0  # Saldo é a terceira parte
                    usuario = {"senha": senha, "saldo": saldo}
                    # Adiciona as quantidades de criptomoedas do usuário, se houver
                    for i in range(3, len(partes), 2):
                        moeda = partes[i]
                        quantidade = float(partes[i + 1])
                        usuario[moeda] = quantidade
                    usuarios[cpf] = usuario
                else:
                    print(f"Formato inválido encontrado na linha {linha_numero} do arquivo de usuários.")
    return usuarios


# Função para salvar os usuários e saldos no arquivo
def salvar_usuarios(usuarios):
    with open(arquivo_usuarios, "w") as j:
        for cpf, dados in usuarios.items():
            linha = f"{cpf}:{dados['senha']}:{dados['saldo']}"
            # Adiciona as quantidades de criptomoedas compradas
            for moeda, quantidade in dados.items():
                if moeda not in ["senha", "saldo"]:
                    linha += f":{moeda}:{quantidade}"
            linha += "\n"
            j.write(linha)

# Função para verificar se o usuário existe e senha está correta
def verificar_usuario(cpf, senha):
    usuarios = ler_usuarios()
    if cpf in usuarios and usuarios[cpf]["senha"] == senha:
        return True
    return False

# Função para registrar novo usuário
def registrar():
    cpf = input("Informe seu CPF (somente números): ")
    if not cpf.isdigit() or len(cpf) != 11:
        print("CPF inválido. Deve conter apenas 11 números.")
        return
    senha = input("Informe sua senha (6 dígitos, somente números): ")
    if len(senha) != 6 or not senha.isdigit():
        print("Senha inválida. Deve ter 6 dígitos e conter somente números.")
        return
    with open(arquivo_usuarios, "a") as j:
        j.write(f"{cpf}:{senha}\n")
    print("Usuário registrado com sucesso!")

# Função para login do usuário
def login():
    cpf = input("Informe seu CPF (sem pontos e sem traços): ")
    senha = input("Informe sua senha (6 dígitos): ")
    if verificar_usuario(cpf, senha):
        print("Login realizado com sucesso!")
        return cpf
    else:
        print("CPF ou senha incorretos. Tente novamente.")
        return None

# Função para sair do menu do investidor
def sair(cpf):
    print("Saindo...")
    main()


# Função auxiliar para atualizar o saldo e as quantidades de criptomoedas no arquivo de usuários
def atualizar_saldo_e_criptomoedas(cpf, saldo, criptomoedas):
    usuarios = ler_usuarios()
    if cpf in usuarios:
        usuarios[cpf]["saldo"] = saldo
        for moeda, quantidade in criptomoedas.items():
            usuarios[cpf][moeda] = quantidade
        salvar_usuarios(usuarios)



# Função para salvar uma transação no extrato
def salvar_transacao_extrato(cpf, valor, tipo, moeda, quantidade=0):
    # Formata a transação
    data_hora = datetime.now().strftime("%d-%m-%Y %H:%M")
    if tipo in ['+', '-']:
        transacao = f"{data_hora} {tipo} {valor:.2f} {moeda}"
    elif tipo in ['COMPRA', 'VENDA']:
        transacao = f"{data_hora} {tipo} {quantidade:.8f} {moeda} por R${valor:.2f}"
    
    # Salva a transação no arquivo de extrato
    with open(arquivo_extrato, "a") as f:
        f.write(f"CPF: {cpf}\n")
        f.write(transacao + "\n")

# Função para consultar saldo do investidor
def consultar_saldo(cpf):
    usuarios = ler_usuarios()
    if cpf in usuarios:
        saldo = usuarios[cpf]["saldo"]
        print(f"Saldo do CPF {cpf}: R${saldo:.2f}")
    else:
        print("CPF não encontrado.")

def consultar_extrato(cpf):
    usuarios = ler_usuarios()
    if cpf in usuarios:
        print(f"Extrato do CPF {cpf}:")
        with open(arquivo_extrato, "r") as f:
            extrato_linhas = f.readlines()
            for i in range(0, len(extrato_linhas), 2):
                if extrato_linhas[i].strip() == f"CPF: {cpf}":
                    transacao = extrato_linhas[i + 1].strip().split()
                    tipo = transacao[1]
                    if tipo == "COMPRA":
                        tipo_abreviado = "CT"
                    elif tipo == "VENDA":
                        tipo_abreviado = "VD"
                    else:
                        tipo_abreviado = tipo
                    valor = float(transacao[3])
                    moedas = " ".join([f"{m[0]}:{m[1]}" for m in zip(["BTC", "ETH", "XRP"], transacao[7:])])
                    # Atualizar informações das criptomoedas no extrato
                    saldo = usuarios[cpf]["saldo"]
                    btc = usuarios[cpf].get("Bitcoin", 0)  
                    eth = usuarios[cpf].get("Ethereum", 0)  
                    xrp = usuarios[cpf].get("Ripple", 0)  
                    print(f"{transacao[0]} {transacao[1]} {transacao[2]} {tipo_abreviado}: {valor:.2f} BTC:{btc} ETH:{eth} XRP:{xrp} REAL:{saldo}")
    else:
        print("CPF não encontrado.")



# Função para depositar dinheiro na conta do investidor
def depositar(cpf):
    valor = float(input("Informe o valor a ser depositado: R$"))
    if valor <= 0:
        print("Valor inválido. O valor a ser depositado deve ser maior que zero.")
        return
    usuarios = ler_usuarios()
    if cpf in usuarios:
        usuarios[cpf]["saldo"] += valor
        salvar_usuarios(usuarios)
        print(f"Depósito de R${valor:.2f} realizado com sucesso!")
        consultar_saldo(cpf)
        salvar_transacao_extrato(cpf, valor, '+', 'REAL')
    else:
        print("CPF não encontrado.")

# Função para sacar dinheiro da conta do investidor
def sacar(cpf):
    senha = input("Informe sua senha (6 dígitos): ")
    if verificar_usuario(cpf, senha):
        valor = float(input("Informe o valor a ser sacado: R$"))
        if valor <= 0:
            print("Valor inválido. O valor a ser sacado deve ser maior que zero.")
            return
        usuarios = ler_usuarios()
        if cpf in usuarios:
            if usuarios[cpf]["saldo"] >= valor:
                usuarios[cpf]["saldo"] -= valor
                salvar_usuarios(usuarios)
                print(f"Saque de R${valor:.2f} realizado com sucesso!")
                consultar_saldo(cpf)
                salvar_transacao_extrato(cpf, valor, '-', 'REAL')
            else:
                print("Saldo insuficiente para realizar o saque.")
        else:
            print("CPF não encontrado.")
    else:
        print("Senha incorreta.")

# Função para obter a cotação de uma criptomoeda
def obter_cotacao(criptomoeda):
    # Verifica se a criptomoeda está no dicionário de cotações
    if criptomoeda in cotacoes:
        # Variação aleatória entre -5% e +5%
        variacao = random.uniform(-0.05, 0.05)
        # Aplica a variação na cotação atual
        nova_cotacao = cotacoes[criptomoeda] * (1 + variacao)
        # Atualiza a cotação no dicionário
        cotacoes[criptomoeda] = nova_cotacao
        # Retorna a nova cotação
        return nova_cotacao
    else:
        print("Criptomoeda não encontrada.")
        return None

# Função para comprar criptomoedas
def comprar_criptomoedas(cpf):
    senha = input("Informe sua senha (6 dígitos): ")
    if verificar_usuario(cpf, senha):
        print("Opções disponíveis para compra:")
        print("1. Bitcoin")
        print("2. Ethereum")
        print("3. Ripple")
        opcao = input("Informe o número correspondente à criptomoeda desejada: ")
        
        if opcao == "1":
            moeda = "Bitcoin"
            taxa = 0.02
        elif opcao == "2":
            moeda = "Ethereum"
            taxa = 0.01
        elif opcao == "3":
            moeda = "Ripple"
            taxa = 0.01
        else:
            print("Opção inválida.")
            return
        
        quantidade = float(input(f"Informe a quantidade de {moeda} a comprar: "))
        valor_unitario = obter_cotacao(moeda)  # Função para obter a cotação da criptomoeda
        if valor_unitario is not None:
            total_sem_taxa = quantidade * valor_unitario
            taxa_cobrada = total_sem_taxa * taxa
            total_com_taxa = total_sem_taxa + taxa_cobrada
            
            # Atualizar saldo e carteira do usuário
            usuarios = ler_usuarios()
            if cpf in usuarios:
                saldo = usuarios[cpf]["saldo"]
                if saldo >= total_com_taxa:
                    saldo -= total_com_taxa
                    if moeda in usuarios[cpf]:
                        usuarios[cpf][moeda] += quantidade
                    else:
                        usuarios[cpf][moeda] = quantidade
                    usuarios[cpf]["saldo"] = saldo  # Atualizar o saldo do usuário
                    salvar_usuarios(usuarios)
                    print(f"Compra de {quantidade} {moeda} realizada com sucesso por R${total_com_taxa:.2f}, incluindo uma taxa de {taxa*100:.2f}%.")
                    consultar_saldo(cpf)  # Mostrar o saldo atualizado
                    salvar_transacao_extrato(cpf, total_com_taxa, 'COMPRA', moeda, quantidade)
                else:
                    print("Saldo insuficiente para realizar a compra.")
            else:
                print("CPF não encontrado.")
    else:
        print("Senha incorreta.")

# Função para vender criptomoedas
def vender_criptomoedas(cpf):
    senha = input("Informe sua senha (6 dígitos): ")
    if verificar_usuario(cpf, senha):
        print("Opções disponíveis para venda:")
        print("1. Bitcoin")
        print("2. Ethereum")
        print("3. Ripple")
        opcao = input("Informe o número correspondente à criptomoeda desejada: ")
        
        if opcao == "1":
            moeda = "Bitcoin"
            taxa = 0.03
        elif opcao == "2":
            moeda = "Ethereum"
            taxa = 0.02
        elif opcao == "3":
            moeda = "Ripple"
            taxa = 0.01
        else:
            print("Opção inválida.")
            return
        
        # Verifica se o usuário está cadastrado no sistema
        usuarios = ler_usuarios()
        if cpf in usuarios:
            # Verifica se a criptomoeda está disponível para o usuário
            if moeda in usuarios[cpf]:
                quantidade_disponivel = usuarios[cpf][moeda]
                print(f"Você possui {quantidade_disponivel} {moeda} disponíveis para venda.")
                quantidade = float(input(f"Informe a quantidade de {moeda} a vender: "))
                if quantidade <= quantidade_disponivel:
                    valor_unitario = obter_cotacao(moeda)  # Função para obter a cotação da criptomoeda
                    if valor_unitario is not None:
                        total_sem_taxa = quantidade * valor_unitario
                        taxa_cobrada = total_sem_taxa * taxa
                        total_com_taxa = total_sem_taxa - taxa_cobrada
                        
                        # Atualizar saldo e carteira do usuário
                        saldo = usuarios[cpf]["saldo"]
                        saldo += total_com_taxa
                        usuarios[cpf][moeda] -= quantidade
                        atualizar_saldo_e_criptomoedas(cpf, saldo, usuarios[cpf])
                        print(f"Venda de {quantidade} {moeda} realizada com sucesso por R${total_com_taxa:.2f}, descontando uma taxa de {taxa*100:.2f}%.")
                        salvar_transacao_extrato(cpf, total_com_taxa, 'VENDA', moeda, quantidade)
                else:
                    print("Quantidade informada maior que a quantidade disponível para venda.")
            else:
                print(f"Usuário não possui a criptomoeda {moeda}.")
        else:
            print("CPF não encontrado.")
    else:
        print("Senha incorreta.")

# Função para exibir o resumo das informações do usuário
def exibir_resumo(cpf):
    usuarios = ler_usuarios()
    if cpf in usuarios:
        usuario = usuarios[cpf]
        print(f"CPF: {cpf}")
        print(f"Reais: R${usuario['saldo']:.2f}")
        for moeda in ["Bitcoin", "Ethereum", "Ripple"]:
            quantidade = usuario.get(moeda, 0)
            print(f"{moeda}: {quantidade:.8f}")
    else:
        print("CPF não encontrado.")


# Função para atualizar a cotação das criptomoedas
def atualizar_cotacao():
    print("Atualizando cotações das criptomoedas...")
    for moeda in cotacoes:
        nova_cotacao = obter_cotacao(moeda)
        print(f"Cotação de {moeda}: R${nova_cotacao:.2f}")
    print("Cotações atualizadas com sucesso!")

# Função principal
def main():
    print("== Sistema de Investimentos ==")
    while True:
        print("\n== Menu Principal ==")
        print("1. Registrar")
        print("2. Login")
        print("3. Sair")
        opcao = input("Informe a opção desejada: ")

        if opcao == "1":
            registrar()
        elif opcao == "2":
            cpf = login()
            if cpf:
                while True:
                    exibir_resumo(cpf)

                    print("\n== Menu do Investidor ==")
                    print("1. Consultar saldo")
                    print("2. Consultar extrato")
                    print("3. Depositar")
                    print("4. Sacar")
                    print("5. Comprar criptomoedas")
                    print("6. Vender criptomoedas")
                    print("7. Atualizar cotação")
                    print("8. Sair")
                    opcao = input("\nInforme a opção desejada: ")

                    if opcao == "1":
                        consultar_saldo(cpf)
                    elif opcao == "2":
                        consultar_extrato(cpf)
                    elif opcao == "3":
                        depositar(cpf)
                    elif opcao == "4":
                        sacar(cpf)
                    elif opcao == "5":
                        comprar_criptomoedas(cpf)
                    elif opcao == "6":
                        vender_criptomoedas(cpf)
                    elif opcao == "7":
                        atualizar_cotacao()
                    elif opcao == "8":
                        sair(cpf)
                        break
                    else:
                        print("Opção inválida.")
        elif opcao == "3":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

# Iniciar o programa
if __name__ == "__main__":
    main()
