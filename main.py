import tkinter as tk
import math

ARQUIVO_HISTORICO = "historico_interface.txt"
ASSINATURA = "Feito por Israel Soares  •  github.com/israelsoares-dev"

# Paleta
FUNDO = "#0f172a"
PAINEL = "#1e293b"
OPERADOR = "#334155"
TEXTO = "#e2e8f0"
DESTAQUE = "#f59e0b"
SUCESSO = "#34d399"
ERRO = "#f87171"
CINZA = "#94a3b8"   # cor suave para textos de apoio
FONTE = "Consolas"

# texto de ajuda
AJUDA_PADRAO = "Dica: passe o mouse sobre um botão para ver o que ele faz."
AJUDA_SOMA = "Somar: soma o 1º com o 2º.  Ex.: 2 + 3 = 5"
AJUDA_SUBTRACAO = "Subtrair: tira o 2º do 1º.  Ex.: 5 - 3 = 2"
AJUDA_MULTIPLICACAO = "Multiplicar: multiplica os dois.  Ex.: 4 * 3 = 12"
AJUDA_DIVISAO = "Dividir: divide o 1º pelo 2º (2º não pode ser zero).  Ex.: 10 / 4 = 2.5"
AJUDA_POTENCIA = "Potência: eleva o 1º ao 2º.  Ex.: 2 ** 3 = 8"
AJUDA_RAIZ = "Raiz quadrada: usa SÓ o 1º número.  Ex.: raiz de 9 = 3"


#Lógica
def mostrar_erro(mensagem):
    label_conta.config(text="Algo deu errado:")  # NOVO
    label_resultado.config(text=mensagem, fg=ERRO)


def ler_numeros():
    try:
        n1 = float(entrada_n1.get().replace(",", "."))
        n2 = float(entrada_n2.get().replace(",", "."))
        return n1, n2
    except ValueError:
        mostrar_erro("Erro: digite apenas números nos dois campos")
        return None


def registrar(operacao, resultado):
    texto = f"{operacao} = {resultado:.2f}"
    label_conta.config(text=f"{operacao} =")  # NOVO: mostra a conta feita
    label_resultado.config(text=f"{resultado:.2f}", fg=SUCESSO)
    lista_historico.insert(tk.END, texto)
    lista_historico.see(tk.END)
    with open(ARQUIVO_HISTORICO, "a", encoding="utf-8") as arquivo:
        arquivo.write(texto + "\n")


def carregar_historico():
    try:
        with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                lista_historico.insert(tk.END, linha.strip())
    except FileNotFoundError:
        pass


def limpar_historico():
    lista_historico.delete(0, tk.END)
    with open(ARQUIVO_HISTORICO, "w", encoding="utf-8"):
        pass


def limpar_campos():
    entrada_n1.delete(0, tk.END)
    entrada_n2.delete(0, tk.END)
    label_conta.config(text="A conta aparece aqui")
    label_resultado.config(text="= ?", fg=DESTAQUE)
    entrada_n1.focus()


def calcular_soma():
    numeros = ler_numeros()
    if numeros:
        n1, n2 = numeros
        registrar(f"{n1:g} + {n2:g}", n1 + n2)


def calcular_subtracao():
    numeros = ler_numeros()
    if numeros:
        n1, n2 = numeros
        registrar(f"{n1:g} - {n2:g}", n1 - n2)


def calcular_multiplicacao():
    numeros = ler_numeros()
    if numeros:
        n1, n2 = numeros
        registrar(f"{n1:g} * {n2:g}", n1 * n2)


def calcular_divisao():
    numeros = ler_numeros()
    if numeros:
        n1, n2 = numeros
        if n2 == 0:
            mostrar_erro("Erro: divisão por zero. Troque o 2º número")
        else:
            registrar(f"{n1:g} / {n2:g}", n1 / n2)


def calcular_potencia():
    numeros = ler_numeros()
    if numeros:
        n1, n2 = numeros
        try:
            resultado = n1 ** n2
        except ZeroDivisionError:
            mostrar_erro("Erro: zero elevado a expoente negativo")
            return
        except OverflowError:
            mostrar_erro("Erro: resultado muito grande")
            return
        if isinstance(resultado, complex):
            mostrar_erro("Erro: resultado não é um número real")
        else:
            registrar(f"{n1:g} ** {n2:g}", resultado)


def calcular_raiz():
    try:
        n1 = float(entrada_n1.get().replace(",", "."))
    except ValueError:
        mostrar_erro("Erro: digite um número no primeiro campo")
        return
    if n1 < 0:
        mostrar_erro("Erro: raiz de número negativo")
    else:
        registrar(f"raiz de {n1:g}", math.sqrt(n1))


#Interface
janela = tk.Tk()
janela.title("Calculadora Autoral")
janela.geometry("380x740")
janela.configure(bg=FUNDO)
janela.resizable(False, False)
janela.columnconfigure((0, 1, 2), weight=1)


#  texto de ajuda do botão
def criar_botao(texto, comando, linha, coluna, ajuda, cor=OPERADOR):
    botao = tk.Button(
        janela, text=texto, command=comando, width=11, height=2,
        bg=cor, fg=TEXTO, activebackground=DESTAQUE, activeforeground=FUNDO,
        relief="flat", font=(FONTE, 11, "bold"), cursor="hand2",
    )
    botao.grid(row=linha, column=coluna, padx=5, pady=5)

    def ao_entrar(evento):
        botao.config(bg=DESTAQUE, fg=FUNDO)
        label_ajuda.config(text=ajuda)

    def ao_sair(evento):
        botao.config(bg=cor, fg=TEXTO)
        label_ajuda.config(text=AJUDA_PADRAO)

    botao.bind("<Enter>", ao_entrar)
    botao.bind("<Leave>", ao_sair)
    return botao


def criar_entrada(linha):
    entrada = tk.Entry(
        janela, bg=PAINEL, fg=TEXTO, insertbackground=DESTAQUE,
        relief="flat", font=(FONTE, 14), justify="right",
    )
    entrada.grid(row=linha, column=0, columnspan=3, padx=20, pady=(0, 8), sticky="ew")
    return entrada


# Cabeçalho
tk.Label(janela, text="CALCULADORA", bg=FUNDO, fg=DESTAQUE,
         font=(FONTE, 20, "bold")).grid(row=0, column=0, columnspan=3, pady=(15, 0))
tk.Label(janela, text="python + tkinter  |  projeto autoral", bg=FUNDO, fg=TEXTO,
         font=(FONTE, 9)).grid(row=1, column=0, columnspan=3, pady=(0, 6))

#guia de uso em 2 passos
tk.Label(janela, text="Passo 1: digite os números\nPasso 2: clique na operação",
         bg=FUNDO, fg=CINZA, font=(FONTE, 10), justify="center"
         ).grid(row=2, column=0, columnspan=3, pady=(0, 10))

# Entradas
tk.Label(janela, text="primeiro número (ex.: 12 ou 3,5)", bg=FUNDO, fg=TEXTO,
         font=(FONTE, 9)).grid(row=3, column=0, columnspan=3, padx=20, sticky="w")
entrada_n1 = criar_entrada(4)

tk.Label(janela, text="segundo número (a raiz não usa este)", bg=FUNDO, fg=TEXTO,
         font=(FONTE, 9)).grid(row=5, column=0, columnspan=3, padx=20, sticky="w")
entrada_n2 = criar_entrada(6)

# Texto de ajuda
label_ajuda = tk.Label(janela, text=AJUDA_PADRAO, bg=FUNDO, fg=CINZA,
                       font=(FONTE, 9, "italic"), wraplength=330, justify="left")

# Botões
criar_botao("+\nSomar", calcular_soma, 7, 0, AJUDA_SOMA)
criar_botao("-\nSubtrair", calcular_subtracao, 7, 1, AJUDA_SUBTRACAO)
criar_botao("*\nMultiplicar", calcular_multiplicacao, 7, 2, AJUDA_MULTIPLICACAO)
criar_botao("/\nDividir", calcular_divisao, 8, 0, AJUDA_DIVISAO)
criar_botao("**\nPotência", calcular_potencia, 8, 1, AJUDA_POTENCIA, cor="#475569")
criar_botao("r\nRaiz", calcular_raiz, 8, 2, AJUDA_RAIZ, cor="#475569")

label_ajuda.grid(row=9, column=0, columnspan=3, padx=20, pady=(4, 8), sticky="w")

# Resultado
label_conta = tk.Label(janela, text="A conta aparece aqui", bg=FUNDO, fg=CINZA,
                       font=(FONTE, 10))
label_conta.grid(row=10, column=0, columnspan=3)

label_resultado = tk.Label(janela, text="= ?", bg=FUNDO, fg=DESTAQUE,
                           font=(FONTE, 18, "bold"), wraplength=330)
label_resultado.grid(row=11, column=0, columnspan=3, pady=(0, 6))

#botão para limpar as caixas
tk.Button(
    janela, text="limpar campos", command=limpar_campos,
    bg=PAINEL, fg=TEXTO, activebackground=DESTAQUE, activeforeground=FUNDO,
    relief="flat", font=(FONTE, 9), cursor="hand2",
).grid(row=12, column=0, columnspan=3, pady=4)

# Histórico
tk.Label(janela, text="histórico (salvo em historico_interface.txt)", bg=FUNDO, fg=TEXTO,
         font=(FONTE, 9)).grid(row=13, column=0, columnspan=3, padx=20, pady=(8, 2), sticky="w")

quadro_historico = tk.Frame(janela, bg=FUNDO)
quadro_historico.grid(row=14, column=0, columnspan=3, padx=20, sticky="ew")

barra = tk.Scrollbar(quadro_historico)  # NOVO: barra de rolagem
lista_historico = tk.Listbox(
    quadro_historico, height=6, bg=PAINEL, fg=TEXTO, relief="flat",
    highlightthickness=0, selectbackground=DESTAQUE, selectforeground=FUNDO,
    font=(FONTE, 10), yscrollcommand=barra.set,
)
barra.config(command=lista_historico.yview)
lista_historico.pack(side="left", fill="both", expand=True)
barra.pack(side="right", fill="y")

botao_limpar = tk.Button(
    janela, text="limpar histórico", command=limpar_historico,
    bg=FUNDO, fg=ERRO, activebackground=ERRO, activeforeground=FUNDO,
    relief="flat", font=(FONTE, 9), cursor="hand2",
)
botao_limpar.grid(row=15, column=0, columnspan=3, pady=8)

# Assinatura
tk.Label(janela, text=ASSINATURA, bg=FUNDO, fg=DESTAQUE,
         font=(FONTE, 8)).grid(row=16, column=0, columnspan=3, pady=(5, 0))

carregar_historico()
entrada_n1.focus()
janela.mainloop()