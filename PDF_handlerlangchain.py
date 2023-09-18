import os
import warnings
import dotenv
import chromadb
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.text_splitter import TokenTextSplitter
from langchain.prompts import PromptTemplate

warnings.filterwarnings("ignore")
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # TO SURPRESS Tensorflow warnings
warnings.filterwarnings("default")

dotenv.load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
vector_db_path = os.getenv("VECTOR_DB_PATH")
client = chromadb.PersistentClient(path=vector_db_path)


class ChatWithPDF:
    def __init__(self, filename, api_key, message_limit=1200):
        # record history of dialog
        self.filename = filename
        self.message_limit = message_limit

        # initialize models
        self.llm = OpenAI(temperature=0.2, openai_api_key=api_key)
        self.embeddings = OpenAIEmbeddings(openai_api_key=api_key)

    def memorize_content(self):
        # read file chunk by chunk
        self.chunks = PyPDFLoader(self.filename).load()
        print(f"The file <{self.filename}> has been read")

        token_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=100)

        self.chunks = token_splitter.split_documents(self.chunks)  # split by tokens

        # write embeddings of chunks to vecDb
        self.vec_database = Chroma.from_documents(
            self.chunks, self.embeddings, persist_directory=vector_db_path
        )
        print("The file has been recorded to vec db")

        # set up extractor from this vec database
        self.retriever = self.vec_database.as_retriever(
            search_type="similarity", search_kwargs={"k": 4}
        )

        template = """Use this information in order to answer the question. 
                Context: {context}
                Question: {question}
                Your answer must be complete and consistent.
              Your answer must contain at least 100 words"""

        QA_PROMPT = PromptTemplate.from_template(template)

        self.qa_chain = RetrievalQA.from_chain_type(
            self.llm,
            retriever=self.retriever,
            chain_type_kwargs={"prompt": QA_PROMPT},
            verbose=False,
        )

    def ask_question(self, question_text):
        reply = self.qa_chain({"query": question_text})
        return reply


class Dialog:
    def __init__(self, name_of_doc):
        # initialize chat
        self.chat = ChatWithPDF(name_of_doc, api_key=OPENAI_API_KEY)
        self.chat.memorize_content()

    def ask(self, query):
        reply = self.chat.ask_question(query)

        return reply["result"]
