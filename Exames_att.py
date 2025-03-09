# Para instalar todas as bibliotecas necessárias de uma vez, execute este comando no terminal:
#pip install pandas matplotlib streamlit plotly

import pandas as pd  # Biblioteca para manipulação de dados
import re            # Biblioteca para trabalhar com expressões regulares
import logging       # Biblioteca para registrar logs do sistema
import matplotlib.pyplot as plt  # Biblioteca para visualização de gráficos
import os           # Biblioteca para manipulação de caminhos de arquivos
import tkinter as tk  # Biblioteca para interface gráfica
from tkinter import filedialog  # Módulo para abertura de diálogos de arquivos
import streamlit as st  # Biblioteca para criação de dashboards interativos
import plotly.express as px  # Biblioteca para visualizações interativas

# Função para abrir um seletor de arquivos e retornar o caminho do arquivo escolhido
def selecionar_arquivo():
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal do tkinter
    caminho_arquivo = filedialog.askopenfilename(title="Selecione um arquivo CSV", filetypes=[("Arquivos CSV", "*.csv")])
    return caminho_arquivo

# Solicita ao usuário a seleção dos arquivos de dados estruturados e não estruturados
print("Selecione o arquivo de dados estruturados")
caminho_estruturados = selecionar_arquivo()
df_estruturados = pd.read_csv(caminho_estruturados) if caminho_estruturados else None

print("Selecione o arquivo de dados não estruturados")
caminho_nao_estruturados = selecionar_arquivo()
df_nao_estruturados = pd.read_csv(caminho_nao_estruturados) if caminho_nao_estruturados else None

# Função para extrair nomes de exames médicos mencionados no texto usando regex
def extrair_exames(texto):
    sinonimos_exames = {
        "RX": "RADIOGRAFIA",
        "ULTRASSOM": "ULTRASSONOGRAFIA",
        "ECG": "ELETROCARDIOGRAMA",
        "HEMOGRAMA COMPLETO": "HEMOGRAMA"
    }
    
    # Padrão regex para capturar os principais exames médicos
    padrao_exames = r"(?i)\b(ressonância magnética|tomografia computadorizada|ultrassonografia|ultrassom|mamografia|radiografia|ecocardiograma|eletrocardiograma|rx|hemograma|teste ergométrico|fisioterapia|endoscopia|colonoscopia|doppler|angiografia|cintilografia|espirometria|densitometria óssea|polissonografia|biopsia|exame de sangue|exame laboratorial|exame clínico|eletroneuromiografia|holter|mapa|radioterapia|pet-scan|cintilografia óssea|urodinâmica|manometria esofágica|capsuloscopia)\b"
    
    exames_encontrados = re.findall(padrao_exames, str(texto))
    exames_encontrados = [sinonimos_exames.get(exame.upper(), exame) for exame in exames_encontrados]
    return ", ".join(set(exames_encontrados)) if exames_encontrados else None

# Processamento dos dados não estruturados para identificar exames e pacientes elegíveis
if df_nao_estruturados is not None:
    df_nao_estruturados["EXAMES_IDENTIFICADOS"] = df_nao_estruturados["DS_RECEITA"].astype(str).apply(extrair_exames)
    df_pacientes_elegiveis = df_nao_estruturados[
        (df_nao_estruturados["EXAMES_IDENTIFICADOS"].notnull()) &
        (df_nao_estruturados["TEL"].notnull()) &
        (df_nao_estruturados["CPF"].notnull())
    ][["ID", "DATA", "TEL", "CPF", "SOLICITANTE", "EXAMES_IDENTIFICADOS"]]
else:
    df_pacientes_elegiveis = None

# Função para gerar mensagens personalizadas para WhatsApp
def gerar_mensagem(row):
    mensagem = (
        f"Olá 👋, {row['SOLICITANTE']}! Notamos que você tem um exame pendente: {row['EXAMES_IDENTIFICADOS']}."
        "Para maior comodidade, agende seu exame em nossa rede hospitalar agora mesmo!🗓 "
        "Caso já tenha realizado o exame, desconsidere esta mensagem. Estamos à disposição!"
    )
    print(mensagem)
    return mensagem

# Gerando mensagens personalizadas para pacientes elegíveis
if df_pacientes_elegiveis is not None:
    df_pacientes_elegiveis["MENSAGEM_WHATSAPP"] = df_pacientes_elegiveis.apply(gerar_mensagem, axis=1)

# Configuração do sistema de logs para registrar o envio de mensagens
logging.basicConfig(filename="envio_mensagens.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Função para simular o envio de mensagens e registrar logs
def simular_envio_mensagem(row):
    mensagem_log = f"Mensagem enviada para {row['TEL']} - Exame: {row['EXAMES_IDENTIFICADOS']}"
    logging.info(mensagem_log)
    return "Enviado"

# Processando o envio simulado das mensagens e registrando os dados
if df_pacientes_elegiveis is not None:
    df_pacientes_elegiveis["STATUS_ENVIO"] = df_pacientes_elegiveis.apply(simular_envio_mensagem, axis=1)
    df_pacientes_elegiveis["EXAMES_IDENTIFICADOS"] = df_pacientes_elegiveis["EXAMES_IDENTIFICADOS"].str.upper()
    sinonimos_exames = {
        "RX": "RADIOGRAFIA",
        "ULTRASSOM": "ULTRASSONOGRAFIA",
    }
    df_pacientes_elegiveis["EXAMES_IDENTIFICADOS"] = df_pacientes_elegiveis["EXAMES_IDENTIFICADOS"].replace(sinonimos_exames)
    df_pacientes_elegiveis.to_csv("pacientes_elegiveis.csv", index=False)
    print("Processo concluído. Arquivo 'pacientes_elegiveis.csv' gerado com sucesso.")

# Função para gerar um dashboard interativo com os exames mais solicitados
def dashboard():
    st.title("Dashboard de Exames")
    
    if df_pacientes_elegiveis is not None and not df_pacientes_elegiveis.empty:
        exames_mais_frequentes = df_pacientes_elegiveis["EXAMES_IDENTIFICADOS"].value_counts().reset_index()
        exames_mais_frequentes.columns = ["Exame", "Quantidade"]
        
        # Criando gráfico de barras interativo
        fig = px.bar(exames_mais_frequentes, x="Quantidade", y="Exame", orientation='h',
                     title="Top Exames Solicitados", labels={"Quantidade": "Número de Pacientes"})
        st.plotly_chart(fig)
    else:
        st.write("Nenhum dado disponível para exibição.")

# Executa o dashboard quando o script for rodado diretamente
if __name__ == "__main__":
    dashboard()
