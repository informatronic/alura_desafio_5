import tkinter as tk
from tkinter import scrolledtext
import google.generativeai as genai
import textwrap
from markdown import markdown
import pyperclip

genai.configure(api_key="AIzaSyAkP_gFyKpF4XD_1DNbixc1bTe-b8voANo")  # Substitua 'SUA_API_KEY' pela sua chave da API
model = genai.GenerativeModel('gemini-pro')

def to_markdown(text):
    text = text.replace('*', ' *')
    return markdown.markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def enviar_pergunta():
    global contador_perguntas, contador_palavras_enviadas, contador_palavras_recebidas, historico_conversa
    pergunta = input_text.get("1.0", tk.END).strip()
    if pergunta:
        contador_perguntas += 1

        # Desabilita os botões
        desabilitar_botoes()

        # Torna o texto "Processando..." visível
        processando_label.grid()
        root.update()

        # Constrói o prompt
        prompt = "".join([f"{mensagem['role']}: {mensagem['conteudo']}\n\n" for mensagem in historico_conversa]) + f"Você: {pergunta}\n\nGemini:"
        resposta = model.generate_content(prompt)

        # Torna o texto "Processando..." invisível
        processando_label.grid_remove()

        # Reativa os botões
        reativar_botoes()

        # Armazena a pergunta e a resposta
        historico_conversa.append({"role": "Você", "conteudo": pergunta})
        historico_conversa.append({"role": "Gemini", "conteudo": resposta.text})

        # Imprime a conversa
        output_text.config(state=tk.NORMAL)
        output_text.insert(tk.END, "=" * 80 + "\n")
        output_text.insert(tk.END, f"{contador_perguntas}) Você: {pergunta}\n")
        output_text.insert(tk.END, "+" + "-" * 80 + "+\n")
        output_text.insert(tk.END, f"Gemini: {resposta.text}\n")
        output_text.insert(tk.END, "=" * 80 + "\n")
        output_text.config(state=tk.DISABLED)
        output_text.see(tk.END)

        input_text.delete("1.0", tk.END)

        # Atualiza os contadores
        contador_palavras_enviadas += len(pergunta.split())
        contador_palavras_recebidas += len(resposta.text.split())
        atualizar_contadores()

def reiniciar_contadores():
    global contador_perguntas, contador_palavras_enviadas, contador_palavras_recebidas, historico_conversa
    contador_perguntas = 0
    contador_palavras_enviadas = 0
    contador_palavras_recebidas = 0
    historico_conversa = []

    atualizar_contadores()
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.config(state=tk.DISABLED)

def mostrar_historico():
    historico_formatado = ""
    for mensagem in historico_conversa:
        historico_formatado += f"**{mensagem['role']}**: {mensagem['conteudo']}\n\n"

    historico_window = tk.Toplevel(root)
    historico_window.title("Histórico da Conversa")

    historico_text = scrolledtext.ScrolledText(historico_window, wrap=tk.WORD)
    historico_text.pack(expand=True, fill="both")
    historico_text.insert(tk.END, historico_formatado)
    historico_text.config(state=tk.DISABLED)

def copiar_conversa():
    texto_conversa = output_text.get("1.0", tk.END)
    pyperclip.copy(texto_conversa)

    # Cria o popup de sucesso
    popup = tk.Toplevel()
    popup.overrideredirect(True)  # Remove a barra de título
    popup.geometry("250x50")  # Define o tamanho do popup

    # Calcula a posição para centralizar o popup
    largura_popup = popup.winfo_reqwidth()
    altura_popup = popup.winfo_reqheight()
    posicao_x = int(root.winfo_screenwidth() / 2 - largura_popup / 2)
    posicao_y = int(root.winfo_screenheight() / 2 - altura_popup / 2)
    popup.geometry(f"+{posicao_x}+{posicao_y}")  # Define a posição centralizada

    popup_label = tk.Label(popup, text="Mensagens copiadas com sucesso!", fg="green", font=("Helvetica", 12))
    popup_label.pack(pady=10)
    popup.after(2000, popup.destroy)  # Fecha o popup após 2 segundos

def desabilitar_botoes():
    enviar_button.config(state=tk.DISABLED, bg="gray")
    cancelar_button.config(state=tk.DISABLED, bg="gray")
    reiniciar_button.config(state=tk.DISABLED, bg="gray")
    historico_button.config(state=tk.DISABLED, bg="gray")
    copiar_button.config(state=tk.DISABLED, bg="gray")

def reativar_botoes():
    enviar_button.config(state=tk.NORMAL, bg="#4CAF50")
    cancelar_button.config(state=tk.NORMAL, bg="#f44336")
    reiniciar_button.config(state=tk.NORMAL, bg="SystemButtonFace")
    historico_button.config(state=tk.NORMAL, bg="SystemButtonFace")
    copiar_button.config(state=tk.NORMAL, bg="SystemButtonFace")

def atualizar_contadores():
    perguntas_label.config(text=f"Perguntas: {contador_perguntas}")
    enviadas_label.config(text=f"Palavras enviadas: {contador_palavras_enviadas}")
    recebidas_label.config(text=f"Palavras recebidas: {contador_palavras_recebidas}")

# Inicializando contadores
contador_perguntas = 0
contador_palavras_enviadas = 0
contador_palavras_recebidas = 0
historico_conversa = []

# Criando a janela principal
root = tk.Tk()
root.title("byCelso - Perguntas ao Gemini - v1.0")
root.configure(bg="#607d8b")

# Maximiza a janela
root.state('zoomed')

# Labels dos contadores
perguntas_label = tk.Label(root, text=f"Perguntas: {contador_perguntas}", bg="#607d8b", fg="white")
perguntas_label.grid(row=0, column=0, padx=5, pady=5)
enviadas_label = tk.Label(root, text=f"Palavras enviadas: {contador_palavras_enviadas}", bg="#607d8b", fg="white")
enviadas_label.grid(row=0, column=1, padx=5, pady=5)
recebidas_label = tk.Label(root, text=f"Palavras recebidas: {contador_palavras_recebidas}", bg="#607d8b", fg="white")
recebidas_label.grid(row=0, column=2, padx=5, pady=5)

# Label "Processando..." (inicialmente invisível)
processando_label = tk.Label(root, text="Processando...", fg="white", bg="red")
processando_label.grid(row=0, column=3, padx=5, pady=5)
processando_label.grid_remove()

# Output Text
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, bg="#f5f5f5")
output_text.grid(row=1, column=0, columnspan=5, padx=5, pady=5, sticky="nsew")

# Label "Faça sua pergunta:"
input_label = tk.Label(root, text="Faça sua pergunta:", bg="#607d8b", fg="white")
input_label.grid(row=2, column=0, columnspan=5, padx=5, pady=(5, 0), sticky="w")

# Input Text
input_text = tk.Text(root, height=5, wrap=tk.WORD)
input_text.grid(row=3, column=0, columnspan=5, padx=5, pady=(0, 5), sticky="nsew")

# Botões
enviar_button = tk.Button(root, text="Enviar", command=enviar_pergunta, bg="#4CAF50", fg="white")
enviar_button.grid(row=4, column=0, padx=(10, 5), pady=5, sticky="w")  # Alinha à esquerda

cancelar_button = tk.Button(root, text="Cancelar", command=root.destroy, bg="#f44336", fg="white")
cancelar_button.grid(row=4, column=1, padx=(1, 5), pady=5, sticky="w")  # Alinha à esquerda

reiniciar_button = tk.Button(root, text="Reiniciar Contadores", command=reiniciar_contadores)
reiniciar_button.grid(row=4, column=2, padx=(1, 5), pady=5, sticky="w")  # Alinha à esquerda

historico_button = tk.Button(root, text="Mostrar Histórico", command=mostrar_historico)
historico_button.grid(row=4, column=3, padx=(1, 5), pady=5, sticky="w")  # Alinha à esquerda

copiar_button = tk.Button(root, text="Copiar Conversa", command=copiar_conversa)
copiar_button.grid(row=4, column=4, padx=(1, 5), pady=5, sticky="w")  # Alinha à esquerda

# Ajustando pesos para redimensionamento
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_columnconfigure(4, weight=1)

# Foca no input text
input_text.focus()

root.mainloop()