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
FONTE = "Consolas"


#Lógica
def mostrar_erro(mensagem):
    label_resultado.config(text=mensagem, fg=ERRO)


def ler_numeros():
    try:
        n1 = float(entrada_n1.get().replace(",", "."))
        n2 = float(entrada_n2.get().replace(",", "."))
        return n1, n2
    except ValueError:
        mostrar_erro("Erro: digite apenas números")
        return None


def registrar(operacao, resultado):
    texto = f"{operacao} = {resultado:.2f}"
    label_resultado.config(text=f"= {resultado:.2f}", fg=SUCESSO)
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
            mostrar_erro("Erro: divisão por zero")
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
janela.geometry("340x560")
janela.configure(bg=FUNDO)
janela.resizable(False, False)


def criar_botao(texto, comando, linha, coluna, cor=OPERADOR):
    botao = tk.Button(
        janela, text=texto, command=comando, width=6, height=2,
        bg=cor, fg=TEXTO, activebackground=DESTAQUE, activeforeground=FUNDO,
        relief="flat", font=(FONTE, 12, "bold"), cursor="hand2",
    )
    botao.grid(row=linha, column=coluna, padx=5, pady=5)
    botao.bind("<Enter>", lambda e: botao.config(bg=DESTAQUE, fg=FUNDO))
    botao.bind("<Leave>", lambda e: botao.config(bg=cor, fg=TEXTO))
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
         font=(FONTE, 9)).grid(row=1, column=0, columnspan=3, pady=(0, 10))

# Entradas
tk.Label(janela, text="primeiro número", bg=FUNDO, fg=TEXTO,
         font=(FONTE, 9)).grid(row=2, column=0, columnspan=3, padx=20, sticky="w")
entrada_n1 = criar_entrada(3)

tk.Label(janela, text="segundo número", bg=FUNDO, fg=TEXTO,
         font=(FONTE, 9)).grid(row=4, column=0, columnspan=3, padx=20, sticky="w")
entrada_n2 = criar_entrada(5)

# Botões
criar_botao("+", calcular_soma, 6, 0)
criar_botao("-", calcular_subtracao, 6, 1)
criar_botao("*", calcular_multiplicacao, 6, 2)
criar_botao("/", calcular_divisao, 7, 0)
criar_botao("**", calcular_potencia, 7, 1, cor="#475569")
criar_botao("r", calcular_raiz, 7, 2, cor="#475569")

# Resultado
label_resultado = tk.Label(janela, text="= ?", bg=FUNDO, fg=DESTAQUE,
                           font=(FONTE, 16, "bold"), wraplength=300)
label_resultado.grid(row=8, column=0, columnspan=3, pady=12)

# Histórico
lista_historico = tk.Listbox(
    janela, height=6, bg=PAINEL, fg=TEXTO, relief="flat",
    highlightthickness=0, selectbackground=DESTAQUE, selectforeground=FUNDO,
    font=(FONTE, 10),
)
lista_historico.grid(row=9, column=0, columnspan=3, padx=20, sticky="ew")

botao_limpar = tk.Button(
    janela, text="limpar histórico", command=limpar_historico,
    bg=FUNDO, fg=ERRO, activebackground=ERRO, activeforeground=FUNDO,
    relief="flat", font=(FONTE, 9), cursor="hand2",
)
botao_limpar.grid(row=10, column=0, columnspan=3, pady=8)

# Assinatura
tk.Label(janela, text=ASSINATURA, bg=FUNDO, fg=DESTAQUE,
         font=(FONTE, 8)).grid(row=11, column=0, columnspan=3, pady=(5, 0))

carregar_historico()

janela.mainloop()