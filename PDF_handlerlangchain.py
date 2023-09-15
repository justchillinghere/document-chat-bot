import os
import warnings
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.document_loaders import PDFMinerLoader
from langchain.chains import RetrievalQA
from langchain.indexes import VectorstoreIndexCreator

load_dotenv()

warnings.filterwarnings("ignore")
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # TO SURPRESS Tensorflow warnings
warnings.filterwarnings("default")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


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
        self.chunks = PyPDFLoader(self.filename).load_and_split()
        print(f"The file <{self.filename}> has been read")

        # write embeddings of chunks to vecDb
        self.vec_database = DocArrayInMemorySearch.from_documents(
            self.chunks, self.embeddings
        )
        print("The file has been recorded to vec db")

        # set up extractor from this vec database
        self.retriever = self.vec_database.as_retriever()

        self.memory = ConversationBufferMemory(
            return_messages=True,
            memory_key="chat_history",
        )

        self.conversation = ConversationalRetrievalChain.from_llm(
            llm=self.llm, memory=self.memory, retriever=self.retriever
        )

    def ask_question(self, question_text):
        promt = f"""You need to answer the question related to the text you have just read
                            here's some notes you should follow:
                            Before saying that you don't know, do your best to come up with an answer.
                            People hate AI that cant answer their questions!

                            If the question is not related to our text then don't use that text in your answers
                            
                            1) be honest, if you don't know just truthfully say so
                            2) Your reply is limited by 200 words
                            3) Your text should be well structered and has some reasoning points
                            
                            So, here's the question you need to answer:
                            {question_text}
                            """

        reply = self.conversation({"question": promt})["answer"]

        return reply


class Dialog:
    def __init__(self, name_of_doc):
        # initialize chat
        self.chat = ChatWithPDF(name_of_doc, api_key=OPENAI_API_KEY)
        self.chat.memorize_content()

    def ask(self, query):
        reply = self.chat.ask_question(query)

        return reply
