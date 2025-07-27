
import os
import warnings
import streamlit as sl
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFaceEmbeddings

warnings.filterwarnings("ignore", category=FutureWarning, module="transformers")
load_dotenv()

MAX_SIZE_MB = 10

def load_prompt():
    return ChatPromptTemplate.from_template(
        """
        Você é um assistente que responde à Pergunta baseada no Contexto informado.
        Contexto = {context}
        Pergunta = {question}

        Se a resposta não estiver no PDF, responda:
        "Não consigo responder a essa pergunta com minha base de informações."
        """
    )

def load_llm():
    return ChatGroq(model_name="llama3-8b-8192", temperature=0)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

@sl.cache_resource(show_spinner="Indexando documentos pela primeira vez, aguarde...")
def extract_data(file_paths):
    text_chunks = []
    for file_path in file_paths:
        loader = PyPDFLoader(file_path)
        chunks = loader.load_and_split(
            RecursiveCharacterTextSplitter(
                chunk_size=512,
                chunk_overlap=30,
                length_function=len,
                separators=["\n\n", "\n", ".", " "]
            )
        )
        text_chunks.extend(chunks)

    embeddings = HuggingFaceEmbeddings(model_name="intfloat/e5-small-v2")
    return FAISS.from_documents(text_chunks, embeddings)

def save_uploadedfile(uploadedfile):
    upload_dir = "uploaded"
    os.makedirs(upload_dir, exist_ok=True)
    path = os.path.join(upload_dir, uploadedfile.name)
    with open(path, "wb") as f:
        f.write(uploadedfile.getbuffer())
    return path

def remove_uploaded_pdfs():
    upload_dir = "uploaded"
    for file in os.listdir(upload_dir):
        if file.lower().endswith(".pdf"):
            os.remove(os.path.join(upload_dir, file))

def main():
    sl.set_page_config(page_title="AskRAG com Groq", layout="centered")

    sl.sidebar.title("📚 AskRAG")
    sl.sidebar.markdown("Envie PDFs e interaja diretamente com seu conteúdo via IA.")

    if "knowledge_base" not in sl.session_state:
        sl.session_state["knowledge_base"] = None

    if "chat_history" not in sl.session_state:
        sl.session_state.chat_history = []

    with sl.sidebar:
        with sl.form("upload-form", clear_on_submit=True):
            pdf_docs = sl.file_uploader(
                label="Selecione PDF(s):",
                accept_multiple_files=True,
                type=["pdf"]
            )
            submitted = sl.form_submit_button("Processar")

        if submitted:
            if pdf_docs:
                large_files = [f.name for f in pdf_docs if f.size > MAX_SIZE_MB * 1024 * 1024]
                if large_files:
                    sl.sidebar.warning(f"Arquivos grandes (> {MAX_SIZE_MB}MB): {', '.join(large_files)}")
                else:
                    file_paths = [save_uploadedfile(pdf) for pdf in pdf_docs]
                    sl.session_state["knowledge_base"] = extract_data(tuple(file_paths))
                    remove_uploaded_pdfs()
                    sl.sidebar.success("✅ Upload e indexação concluídos!")
            else:
                sl.sidebar.warning("⚠️ Nenhum PDF selecionado.")

        if sl.sidebar.button("🔄 Limpar memória atual"):
            sl.session_state["knowledge_base"] = None
            sl.session_state.chat_history = []
            sl.sidebar.success("🗑️ Memória limpa com sucesso!")

    sl.header("🔍 AskRAG - Chat com PDF usando Groq")

    if not sl.session_state["knowledge_base"]:
        sl.info("📌 Faça upload de PDFs na barra lateral para habilitar a interação.")
        return

    query = sl.text_input("Pergunte algo sobre o PDF:")

    if query:
        try:
            similar_docs = sl.session_state["knowledge_base"].similarity_search(query)
            context = format_docs(similar_docs)

            rag_chain = load_prompt() | load_llm() | StrOutputParser()
            response = rag_chain.invoke({"context": context, "question": query})

            sl.session_state.chat_history.append({"pergunta": query, "resposta": response})

            for chat in reversed(sl.session_state.chat_history):
                sl.markdown(f"**Pergunta:** {chat['pergunta']}")
                sl.markdown(f"**Resposta:** {chat['resposta']}")
                sl.divider()

        except Exception as e:
            sl.error(f"❌ Erro ao processar: `{str(e)}`")

if __name__ == "__main__":
    main()
