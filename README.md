# 📌 Processamento e Análise de Exames Médicos

## 📖 Sobre o Projeto

Este projeto processa e analisa **dados estruturados e não estruturados** de exames médicos para identificar exames solicitados e gerar mensagens automáticas para pacientes. Além disso, cria um **gráfico dos exames mais solicitados** e exporta um arquivo CSV com os dados processados.

## 🏗️ Arquitetura do Projeto

### 🔹 **Diagrama da Arquitetura**

![image](https://github.com/user-attachments/assets/ac33027b-fa35-47ba-b1ee-4ecca27259e9)

### 🔹 **Componentes da Solução**

1. **Interface de Seleção de Arquivos** → Tkinter permite que o usuário escolha os arquivos CSV.

        import tkinter as tk
        from tkinter import filedialog

        def selecionar_arquivo():
        root = tk.Tk()
        root.withdraw()
        caminho_arquivo = filedialog.askopenfilename(title="Selecione um arquivo CSV", filetypes=[("Arquivos CSV", "*.csv")])
        return caminho_arquivo

2. **Processamento de Dados** → Pandas lida com dados estruturados e regex extrai exames de textos.

        import pandas as pd
        import re

        def extrair_exames(texto):
            sinonimos_exames = {
        "RX": "RADIOGRAFIA",
        "ULTRASSOM": "ULTRASSONOGRAFIA",
        "ECG": "ELETROCARDIOGRAMA",
        "HEMOGRAMA COMPLETO": "HEMOGRAMA"
            }
    
           # Padrão regex para capturar os principais exames médicos
            padrao_exames = r"(?i)\b(ressonância magnética|tomografia computadorizada|ultrassonografia|ultrassom|mamografia|radiografia|ecocardiograma|eletrocardiograma|rx|hemograma|teste                                ergométrico|fisioterapia|endoscopia|colonoscopia|doppler|angiografia|cintilografia|espirometria|densitometria óssea|polissonografia|biopsia|exame de sangue|exame laboratorial|exame                           clínico|eletroneuromiografia|holter|mapa|radioterapia|pet-scan|cintilografia óssea|urodinâmica|manometria esofágica|capsuloscopia)\b"
    
            exames_encontrados = re.findall(padrao_exames, str(texto))
            exames_encontrados = [sinonimos_exames.get(exame.upper(), exame) for exame in exames_encontrados]
            return ", ".join(set(exames_encontrados)) if exames_encontrados else None
    
3. **Filtragem de Pacientes** → Verifica quais pacientes têm telefone, CPF e exames identificados.
   
        if df_nao_estruturados is not None:
             df_nao_estruturados["EXAMES_IDENTIFICADOS"] = df_nao_estruturados["DS_RECEITA"].astype(str).apply(extrair_exames)
            df_pacientes_elegiveis = df_nao_estruturados[
                (df_nao_estruturados["EXAMES_IDENTIFICADOS"].notnull()) &
                (df_nao_estruturados["TEL"].notnull()) &
                (df_nao_estruturados["CPF"].notnull())
            ][["ID", "DATA", "TEL", "CPF", "SOLICITANTE", "EXAMES_IDENTIFICADOS"]]

5. **Geração de Mensagens Personalizadas** → Cria mensagens dinâmicas para WhatsApp.
   
        def gerar_mensagem(row):
            mensagem = (
        f"Olá 👋, {row['SOLICITANTE']}! Notamos que você tem um exame pendente: {row['EXAMES_IDENTIFICADOS']}. "
        "Para maior comodidade, agende seu exame em nossa rede hospitalar agora mesmo!🗓 "
        "Caso já tenha realizado o exame, desconsidere esta mensagem. Estamos à disposição!"
            )
            return mensagem

7. **Registro de Logs** → Logging armazena informações sobre as mensagens enviadas.
   
        import logging
        logging.basicConfig(filename="envio_mensagens.log", level=logging.INFO, format="%(asctime)s - %(message)s")

        def simular_envio_mensagem(row):
           mensagem_log = f"Mensagem enviada para {row['TEL']} - Exame: {row['EXAMES_IDENTIFICADOS']}"
           logging.info(mensagem_log)
           return "Enviado"

6. **Dashboard Interativo** → Streamlit exibe gráficos de exames mais solicitados.
   
        import streamlit as st
        import plotly.express as px

        def dashboard():
            st.title("Dashboard de Exames")
            if df_pacientes_elegiveis is not None and not df_pacientes_elegiveis.empty:
                exames_mais_frequentes = df_pacientes_elegiveis["EXAMES_IDENTIFICADOS"].value_counts().reset_index()
                exames_mais_frequentes.columns = ["Exame", "Quantidade"]
        fig = px.bar(exames_mais_frequentes, x="Quantidade", y="Exame", orientation='h', title="Top Exames Solicitados")
        st.plotly_chart(fig)


### 🔹 **Comunicação Entre Componentes**

- A interface Tkinter seleciona arquivos e os passa para o processamento com Pandas.
- Regex extrai exames e os dados processados são filtrados.
- As mensagens geradas podem ser integradas a uma API de envio real de WhatsApp.
- O Streamlit exibe os dados processados dinamicamente.

## 🚀 Justificativas Tecnológicas

| Tecnologia | Motivo da Escolha |
|------------|------------------|
| **Python** | Facilidade de manipulação de dados e vasta biblioteca de suporte. |
| **Pandas** | Manipulação eficiente de grandes volumes de dados. |
| **Matplotlib & Plotly** | Visualização de dados interativa. |
| **Regex (re)** | Extração de exames de textos não estruturados. |
| **Logging** | Registro de eventos e depuração do sistema. |
| **Tkinter** | Simples para seleção de arquivos. |
| **Streamlit** | Criação rápida de dashboards interativos. |

## 📈 Escalabilidade

- Para lidar com um aumento de volume de dados:
  - **Uso de Banco de Dados** → Em vez de CSVs, os dados seriam armazenados no PostgreSQL ou MongoDB.
  - **Processamento Paralelo** → Uso de **Dask** para manipulação de grandes arquivos CSV.
  - **Serviço em Nuvem** → Armazenamento e execução no AWS Lambda ou Google Cloud Functions.

## 🔒 Segurança

- **Anonimização de Dados** → Remover informações sensíveis desnecessárias.
- **Criptografia** → Uso de AES para dados sensíveis.
- **Controle de Acesso** → Autenticação via OAuth2.
- **Conformidade com LGPD** → Apenas os dados essenciais são armazenados.

## 💰 Estimativa de Custos

| Recurso | Custo Estimado |
|---------|---------------|
| Armazenamento (S3, BigQuery) | ~10 USD/mês |
| Processamento em Nuvem (Lambda) | ~20 USD/mês |
| API de Mensageria (Twilio) | ~0.005 USD por mensagem |
| Infraestrutura Total | ~30-50 USD/mês |

## 🚀 Melhorias Futuras

1. **Machine Learning** para identificar padrões de exames e prever agendamentos.
2. **Integração com Prontuários Eletrônicos** para maior precisão nos diagnósticos.
3. **Canal Bidirecional** onde pacientes podem responder às mensagens recebidas.

## ⚠️ Desafios e Riscos

- **Qualidade dos Dados** → Textos médicos podem ser inconsistentes.
- **Escalabilidade** → Grande volume de dados pode tornar o processamento lento.
- **Conformidade com a LGPD** → Necessário garantir anonimização e segurança dos dados.

## 📊 Métricas de Sucesso

- **Taxa de Conversão** → Quantos exames identificados resultam em agendamentos.
- **Tempo de Processamento** → Tempo médio para identificar exames e gerar mensagens.
- **Satisfação dos Pacientes** → Coletar feedback via pesquisas.

## 📜 Licença

Este projeto é de uso livre e pode ser modificado conforme necessário.

---

🚀 **Agora você pode processar e analisar exames médicos com eficiência!** Qualquer dúvida, me avise. 😊
