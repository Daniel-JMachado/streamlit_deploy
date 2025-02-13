import streamlit as st  # Import the Streamlit library
import pandas as pd  # Import the pandas library
from PIL import Image  # Import the Image module from PIL (Pillow)
from PyPDF2 import PdfReader  # Import the PdfReader from PyPDF2
from github import Github
import base64
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()  # carrega as variáveis do .env

st.set_page_config(  # Set the page configuration
    layout="centered",  # Set the layout to centered
    page_icon="🚀",  # Set the page icon
    page_title="primeiro app"  # Set the page title
)
st.title("Meu primeiro app nas nuvens 🚀")  # Set the title of the app
st.markdown("---")  # Display a horizontal line

select = st.selectbox("Selecione uma cor", ["Vermelho", "Verde", "Azul"])  # Create a SelectBox with color options
st.write(f"Você selecionou a cor {select}")  # Display the selected color
if select == "Vermelho":
    st.warning("Essa cor é errada")
elif select == "Verde":
    st.error("Essa cor ainda está errada")
else:
    st.success("Essa cor é a certa")

# Upload de arquivo PDF
pdf_file = st.file_uploader(
    "Arraste e solte seu arquivo PDF aqui",  # Prompt for PDF file upload
    type=['pdf'],  # Allow only PDF files
    help="Arquivos permitidos: PDF",  # Display help text
    key="pdf_uploader"  # Set a unique key for the uploader
)

# Upload de imagem
image_file = st.file_uploader(
    "Arraste e solte sua imagem aqui",  # Prompt for image file upload
    type=['jpg', 'png', 'jpeg'],  # Allow only JPG, PNG, and JPEG files
    help="Arquivos permitidos: JPG, PNG, JPEG",  # Display help text
    key="image_uploader"  # Set a unique key for the uploader
)

# Criar pasta para PDF se não existir
if not os.path.exists("PDF"):
    os.makedirs("PDF")  # Create a directory for PDF files if it doesn't exist
if pdf_file is not None:
    # Salvar arquivo PDF
    with open(os.path.join("PDF", pdf_file.name), "wb") as f:
        f.write(pdf_file.getbuffer())  # Save the uploaded PDF file
    st.success(f"Arquivo PDF {pdf_file.name} salvo com sucesso!")  # Display a success message
    # Processar PDF
    pdf = PdfReader(pdf_file)  # Read the PDF file
    st.write(f"Número de páginas: {len(pdf.pages)}")  # Display the number of pages in the PDF


# Configuração do GitHub
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN') # Token de acesso ao GitHub
REPO_NAME = "Daniel-JMachado/Recebidos"  # Nome do seu repositório

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
        raw_url = f"https://raw.githubusercontent.com/{REPO_NAME}/main/{file_name}"
        
        # Mostra mensagem de sucesso com dois links:
        # 1. Link para ver no GitHub (interface do GitHub)
        # 2. Link para ver a imagem diretamente (raw)
        st.success(f"""
        Imagem salva com sucesso! 
        - [Ver no GitHub](https://github.com/{REPO_NAME}/blob/main/{file_name})
        - [Ver imagem direta]({raw_url})
        """)
        
    except Exception as e:
        # Se ocorrer algum erro, mostra a mensagem de erro
        st.error(f"Erro ao fazer upload: {str(e)}")
        # Mostra a imagem no Streamlit


