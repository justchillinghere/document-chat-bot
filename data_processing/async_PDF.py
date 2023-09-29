import os
from typing import List
from uuid import uuid4
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
from langchain.docstore.document import Document
from langchain.prompts import ChatPromptTemplate
import logging


logger = logging.getLogger()
warnings.filterwarnings("ignore")
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # TO SURPRESS Tensorflow warnings
warnings.filterwarnings("default")

dotenv.load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
vector_db_path = os.getenv("VECTOR_DB_PATH")


class ChatWithPDF:
    def __init__(self, user_tg_id: int, api_key: str, message_limit=1200):
        self.message_limit = message_limit
        self.llm = OpenAI(temperature=0.2, openai_api_key=api_key, max_tokens=1000)
        self.embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        self.user_id = user_tg_id
        self.vec_database = None

    async def load_files(self, file_paths: List[str]):
        self.chunks = []
        for i in range(len(file_paths)):
            self.chunks.extend(PyPDFLoader(file_paths[i]).load())
        logger.info(f"Read files from user")

    def split_docs(self, chunk_size: int = 1000, chunk_overlap: int = 100):
        token_splitter = TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        self.chunks = token_splitter.split_documents(self.chunks)
        logger.info(f"Split {len(self.chunks)} chunks")

    async def create_db_collection(self):
        self.vec_database = Chroma.from_documents(
            self.chunks,
            self.embeddings,
            persist_directory=vector_db_path,
            collection_name=f'{self.user_id}_collection',
        )
        self.vec_database.persist()
        logger.info(f"The file has been recorded to vec db")

    async def get_qa_chain(self):
        if self.vec_database is None:
            self.vec_database = Chroma(
                embedding_function=self.embeddings,
                persist_directory=vector_db_path,
                collection_name=f'{self.user_id}_collection_{uuid4()}',
            )
        self.retriever = self.vec_database.as_retriever(
            search_type="mmr", search_kwargs={"k": 4}
        )
        template = """Use this information in order to answer the question. 
                Context: {context}
                Question: {question}

                Answer in the language used in question.
                Your answer must also be complete and consistent.
              """

        QA_PROMPT = PromptTemplate.from_template(template)

        self.qa_chain = RetrievalQA.from_chain_type(
            self.llm,
            retriever=self.retriever,
            chain_type_kwargs={"prompt": QA_PROMPT},
            verbose=False,
        )
        logger.info("QA chain created")

    async def ask_question(self, question_text):
        reply = self.qa_chain({"query": question_text})
        return reply


class Dialog:
    def __init__(self, user_id):
        # initialize chat
        self.chat = ChatWithPDF(user_id, api_key=OPENAI_API_KEY)

    async def load_documents_to_vec_db(self, file_paths: List[str]):
        await self.chat.load_files(file_paths)
        self.chat.split_docs()
        await self.chat.create_db_collection()

    async def ask(self, query):
        await self.chat.get_qa_chain()
        reply = await self.chat.ask_question(query)
        logger.info(f"Raw reply: {reply}")
        logger.info("Question answered")
        return reply["result"]