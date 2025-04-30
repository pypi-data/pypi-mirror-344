from .interfaces import Injestion, Retrieval
import yaml
from ollama import ChatResponse,chat
import psycopg2
from sentence_transformers import SentenceTransformer
from haystack import Document
from haystack.components.preprocessors import DocumentCleaner

class PGVectorInjestion(Injestion):
    def __init__(
        self,
        pg_config: dict = None ,
        config_path: str = None 
    ):
        """
        Contextual Memory Engine.
        :param pg_config: PostgreSQL connection string
        :param config_path: PostgresSQL connection configuration path.
        """

        #         pg_config = {
        #     'host': 'localhost',
        #     'port': 5432,
        #     'dbname': 'your_database',
        #     'user': 'your_username',
        #     'password': 'your_password'
        # }
        if pg_config:
            self.pg_config = pg_config
        elif config_path:
            with open(config_path, 'r') as f:
                self.pg_config = yaml.safe_load(f)
        self.conn=psycopg2.connect(**self.pg_config)
        self.cur=self.conn.cursor()
        self.embedding_model = None
        self.context_model=None
        self.table_name = None
        self.text_col = None
        self.embedding_dimension=None
        self.embedding_column=None
    
    def configure(
        self,
        embedding_model: str,
        context_model: str,
        table_name: str,
        embedding_dim: int,
        text_column: str,
        embedding_column: str
    ):
        """
        Configure semantic model, situate model, table schema, etc.
        Should be called immediately after initialization.
        """
        self.embedding_model = SentenceTransformer(embedding_model)
        self.context_model = context_model
        self.table_name = table_name
        self.embedding_dim = embedding_dim
        self.text_column = text_column
        self.embedding_column = embedding_column

    def postgres_storage(self,combined_text,encoded_input):
        """
        Store the embeddings in the database.
        :param contextual_chunk: The contextual chunk of text.
        :param contextual_chunk_embedding: The embedding of the contextual chunk.
        return : Print statement after successfull into db
        """

        self.cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        self.cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id SERIAL PRIMARY KEY,
            {self.text_column} TEXT,
            {self.embedding_column} vector({self.embedding_dim})
        );
        """)
        self.cur.execute(f"""
        INSERT INTO {self.table_name} (
            {self.text_column},
            {self.embedding_column})
        VALUES (%s,%s::vector);""",
        (combined_text,encoded_input))

        self.conn.commit()

        return print("Data inserted successfully into the database.")

    def encode_input(self, text: str):

        """
        Encodes input text into embeddings using the pre-configured model.
        :param text: The input text to encode.
        :return: The embedding vector for the input text.
        """

        if self.embedding_model is None:
            raise ValueError("Model is not configured. Please call `configure` to set up the embedding model.")
        
        # Encode the text into embeddings
        embedding = self.embedding_model.encode(text)
        return embedding.tolist()
    
    def situate_content(self,document,chunk):

        """
        Situate the content of a chunk within the context of a document.
        :param document: The document in which the chunk is situated.
        :param chunk: The chunk of text to be situated.
        :return: The situated content.
        """

        # Load the model
        try:
            response: ChatResponse = chat(model=self.context_model, messages=[{'role': 'system', 'content': 'test'}])
        except:
            print(f"Pulling {self.context_model} model... This may take a few minutes...")
            print("Model pulled successfully!")

        # Define the prompt for the document context

        DOCUMENT_CONTEXT_PROMPT = """
        <document>
        {doc_content}
        </document>
        """

        CHUNK_CONTEXT_PROMPT = """
        Here is the chunk we want to situate within the whole document
        <chunk>
        {chunk_content}
        </chunk>

        Please give a short succinct context to situate this chunk within the overall document for the purposes of improving search retrieval of the chunk.
        Answer only with the succinct context and nothing else.
        """
        prompt = DOCUMENT_CONTEXT_PROMPT.format(doc_content=document) + CHUNK_CONTEXT_PROMPT.format(chunk_content=chunk)
        response: ChatResponse = chat(model='llama3.2', messages=[
            {
                'role': 'user',
                'content': prompt,
            },
        ])
        combined_text= f"{chunk}{response['message']['content']}"
        return combined_text
    def doc_cleaner(self,text: str):

        doc=Document(content=text)
        cleaner=DocumentCleaner(remove_empty_lines=True,remove_extra_whitespaces=True)
        result = cleaner.run(documents=[doc])
        return result["documents"][0].content
        

    def inject(self, document,data):

        print(f"Injecting into Postgres PG Vector: {data}")
        cleaned_doc=self.doc_cleaner(document)
        cleaned_chunk=self.doc_cleaner(data)
        combined_text=self.situate_content(cleaned_doc,cleaned_chunk)
        encoded_input=self.encode_input(data)
        store=self.postgres_storage(combined_text,encoded_input)
        return print("stored successfully")

class PGVectorRetrieval(Retrieval):

    def __init__(self,
        pg_config: dict = None ,
        config_path: str = None ):

        """
        Contextual Memory Engine.
        :param pg_config: PostgreSQL connection string
        :param config_path: PostgresSQL connection configuration path.
        """
        if pg_config:
            self.pg_config = pg_config
        elif config_path:
            with open(config_path, 'r') as f:
                self.pg_config = yaml.safe_load(f)
        self.conn=psycopg2.connect(**self.pg_config)
        self.cur=self.conn.cursor()
        self.embedding_model = None
        self.table_name = None
        self.text_col = None
        self.embedding_dimension=None
        self.embedding_column=None

    
    def configure(
        self,
        embedding_model: str,
        table_name: str,
        text_column: str,
        embedding_column: str
    ):
        """
        Configure semantic model, situate model, table schema, etc.
        Should be called immediately after initialization.
        """
        self.embedding_model = SentenceTransformer(embedding_model)
        self.table_name = table_name
        self.text_column = text_column
        self.embedding_column = embedding_column

    def retrieve_results(self,embedding_list: list,k: int):

        """
        Retrive results from PgVector database
        :param emedding_list: The query embedding
        :return: A list of top k results
        """

        try:
            self.cur.execute(f"""SELECT id,{self.text_column} FROM {self.table_name} ORDER BY {self.embedding_column} <=> %s :: vector LIMIT {k}""", (embedding_list,))
            results=self.cur.fetchall()
            results_list = [row[1] for row in results]
            return results_list
        except Exception as e:
            print(f"Search failed: {e}")
            return []


    def encode_input(self, text: str):
        """
        Encodes input text into embeddings using the pre-configured model.
        :param text: The input text to encode.
        :return: The embedding vector for the input text.
        """
        if self.embedding_model is None:
            raise ValueError("Model is not configured. Please call `configure` to set up the embedding model.")
        
        # Encode the text into embeddings
        embedding = self.embedding_model.encode(text)
        return embedding.tolist()

    def doc_cleaner(self,text: str):

        doc=Document(content=text)
        cleaner=DocumentCleaner(remove_empty_lines=True,remove_extra_whitespaces=True)
        result = cleaner.run(documents=[doc])
        return result["documents"][0].content
    
    def retrieve(self, query : str , k : int):

        print(f"Retrieving from Postgres PG Vector with query: {query}")
        cleaned_query=self.doc_cleaner(query)
        encoded_input=self.encode_input(cleaned_query)
        result=self.retrieve_results(encoded_input,k)
        return result
