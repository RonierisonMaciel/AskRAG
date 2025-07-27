# PDF Chat com Groq

Este projeto permite realizar perguntas em linguagem natural sobre o conteúdo de arquivos PDF. Utiliza a abordagem **RAG (Retrieval-Augmented Generation)**, que combina técnicas de recuperação de informação com geração de texto para fornecer respostas precisas. A aplicação usa as seguintes tecnologias principais:

* **LangChain** para gerenciamento do fluxo do chat.
* **FAISS** para armazenamento e busca rápida dos embeddings (representações vetoriais dos textos).
* **Groq** como provedor do modelo de linguagem LLM para geração de respostas.

---

## Como funciona?

O fluxo básico da aplicação é:

1. Upload do arquivo PDF.
2. Extração e divisão do texto em pequenos trechos.
3. Transformação desses textos em embeddings vetoriais usando modelos pré-treinados.
4. Armazenamento dos embeddings num banco vetorial (FAISS).
5. Ao fazer uma pergunta, a aplicação recupera automaticamente os trechos mais relevantes do PDF e usa o modelo de linguagem da Groq para gerar respostas contextualizadas.

---

## Requisitos do projeto

* Python **3.9** ou superior.
* Uma conta gratuita na [Groq Cloud](https://groq.com/).
* Chave (API Key) da Groq.

---

## Instalação passo a passo

### 1. Clone este repositório

```bash
git clone https://github.com/ronierisonmaciel/AskRAG.git
cd AskRAG
```

### 2. Crie e ative um ambiente virtual

**macOS ou Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (CMD ou PowerShell):**

```cmd
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instale as dependências necessárias

```bash
pip install -r requirements.txt
```

---

## Configurando a chave da Groq API

Siga estes passos para obter e configurar sua chave:

1. Acesse a página: [https://console.groq.com/keys](https://console.groq.com/keys).
2. Faça login ou crie uma nova conta gratuita.
3. Clique em **"Create API Key"** para gerar uma nova chave.
4. Copie a chave gerada, que começa com `gsk_live_...`.
5. Crie um arquivo `.env` na raiz do projeto e adicione sua chave assim:

```env
GROQ_API_KEY=gsk_live_sua_chave_aqui
```

**Importante:** Não compartilhe sua chave pública ou suba esse arquivo `.env` em repositórios públicos.

---

## Executando o aplicativo localmente

Execute o seguinte comando para iniciar a aplicação Streamlit:

```bash
streamlit run app.py
```

O aplicativo será aberto automaticamente em seu navegador padrão. Caso contrário, acesse a URL informada no terminal, geralmente:
[http://localhost:8501](http://localhost:8501).

---

## Estrutura dos arquivos do projeto

```bash
AskRAG/
│
├── app.py                 # Código principal da aplicação
├── uploaded/              # Pasta temporária para PDFs carregados
├── requirements.txt       # Dependências Python
├── .env                   # Arquivo contendo sua chave Groq API (você deve criar)
├── README.md              # Instruções detalhadas do projeto
└── LICENSE                # Licença do projeto
```

**Observação:**
A pasta `uploaded/` é utilizada temporariamente apenas para processar arquivos. Após o processamento, os PDFs são automaticamente removidos.

---

## Tecnologias utilizadas

* [LangChain](https://www.langchain.com/)
* [Groq API](https://groq.com/)
* [HuggingFace Embeddings (intfloat/e5-small-v2)](https://huggingface.co/intfloat/e5-small-v2)
* [FAISS](https://github.com/facebookresearch/faiss)
* [Streamlit](https://streamlit.io/)

---

## Exemplo prático de uso

Siga os passos abaixo para testar o aplicativo:

1. Após rodar o aplicativo, utilize a barra lateral para enviar um ou mais arquivos PDF.
2. Aguarde o processamento terminar.
3. Agora você pode fazer perguntas diretamente sobre o conteúdo carregado. Por exemplo:

   * Qual o objetivo principal deste documento?
   * Quais tópicos são abordados no texto?

---

## Licença

Este projeto está sob a licença **MIT**.
Utilize à vontade, desde que mantenha os créditos originais.

---
