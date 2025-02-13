import streamlit as st  # Import the Streamlit library
import pandas as pd  # Import the pandas library
from PIL import Image  # Import the Image module from PIL (Pillow)
from PyPDF2 import PdfReader  # Import the PdfReader from PyPDF2
from github import Github
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()  # carrega as variáveis do .env
# Configuração do GitHub
GITHUB_TOKEN = os.getenv('token') # Token de acesso ao GitHub
REPO_NAME = "Daniel-JMachado/Recebidos"  # Nome do seu repositório

st.set_page_config(  # Set the page configuration
    layout="centered",  # Set the layout to centered
    page_icon="🚀",  # Set the page icon
    page_title="primeiro app"  # Set the page title
)
st.title("Meu primeiro app nas nuvens 🚀")  # Set the title of the app
st.markdown("---")  # Display a horizontal line

select = st.selectbox("Selecione uma cor", [" ","Vermelho", "Verde", "Azul"])  # Create a SelectBox with color options
st.write(f"Você selecionou a cor {select}")  # Display the selected color
if select == "Vermelho":
    st.warning("Essa cor é errada")
elif select == "Verde":
    st.error("Essa cor ainda está errada")
elif select == "Azul":
    st.success("Essa cor é a certa")
else:
    st.write("Você precisa selecionar uma cor")

# Upload de arquivo PDF
pdf_file = st.file_uploader(
    "Escolha um arquivo pdf",  # Prompt for PDF file upload
    type=['pdf'],  # Allow only PDF files
    help="Arquivos permitidos: PDF",  # Display help text
    key="pdf_uploader"  # Set a unique key for the uploader
)

# Upload de imagem
image_file = st.file_uploader(
    "Escolha uma imagem",  # Prompt for image file upload
    type=['jpg', 'png', 'jpeg'],  # Allow only JPG, PNG, and JPEG files
    help="Arquivos permitidos: JPG, PNG, JPEG",  # Display help text
    key="image_uploader"  # Set a unique key for the uploader
)

# criação da pasta de upload de pdf:
if pdf_file is not None:
    try:
        # Conecta ao GitHub usando o token de autenticação
        g = Github(GITHUB_TOKEN)
        # Acessa o repositório específico
        repo = g.get_repo(REPO_NAME)
        
        # Cria um nome único para o arquivo usando timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Define o caminho onde o PDF será salvo no GitHub (pasta PDFs)
        file_name = f"PDFs/{timestamp}_{pdf_file.name}"
        
        # Pega o conteúdo binário do PDF
        content = pdf_file.getvalue()
        
        # Cria o arquivo no GitHub
        repo.create_file(
            file_name,  # Caminho/nome do arquivo
            f"Upload PDF {pdf_file.name}",  # Mensagem do commit
            content  # Conteúdo binário do PDF
        )
        
        # Processa e mostra informações do PDF
        pdf = PdfReader(pdf_file)
        st.write(f"Número de páginas: {len(pdf.pages)}")
        
        # Cria URLs para visualização
        # URL para ver o PDF no GitHub
        #github_url = f"https://github.com/{REPO_NAME}/blob/main/{file_name}"
        # URL para download direto do PDF
        #raw_url = f"https://raw.githubusercontent.com/{REPO_NAME}/main/{file_name}"
        
        # Mostra mensagem de sucesso com links
        st.success("PDF enviado com sucesso!")
        
    except Exception as e:
        st.error(f"Erro ao fazer upload do PDF: {str(e)}")


if image_file is not None:  # Verifica se uma imagem foi enviada
    try:
        # Conecta ao GitHub usando o token de autenticação
        g = Github(GITHUB_TOKEN)
        # Acessa o repositório específico
        repo = g.get_repo(REPO_NAME)
        
        # Cria um nome único para o arquivo usando timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Define o caminho onde a imagem será salva no GitHub (pasta images)
        file_name = f"images/{timestamp}_{image_file.name}"
        
        # Pega o conteúdo binário da imagem diretamente
        # Não precisa mais converter para base64
        content = image_file.getvalue()
        
        # Cria o arquivo no GitHub
        repo.create_file(
            file_name,  # Caminho/nome do arquivo
            f"Upload imagem {image_file.name}",  # Mensagem do commit
            content  # Conteúdo binário da imagem
        )
        
        # Mostra a imagem no Streamlit
        img = Image.open(image_file)
        st.image(img)
        
        # Cria URLs para visualização
        # URL para ver a imagem raw (direta)
        #raw_url = f"https://raw.githubusercontent.com/{REPO_NAME}/main/{file_name}"
        
        # Mostra mensagem de sucesso com dois links:
        # 1. Link para ver no GitHub (interface do GitHub)
        # 2. Link para ver a imagem diretamente (raw)
        st.success(f"""
        Imagem ENVIADA com sucesso! 
        """)
        
    except Exception as e:
        # Se ocorrer algum erro, mostra a mensagem de erro
        st.error(f"Erro ao fazer upload: {str(e)}")
        # Mostra a imagem no Streamlit


