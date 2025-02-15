from dotenv import load_dotenv
load_dotenv()  # .env 파일 로드

import os
import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

class VectorService:
    def __init__(self, collection_name: str = "my_collection", persist_path: str = None):
        # persist_path가 지정되지 않으면 .env에서 설정된 값을 사용 (없으면 기본 "../vector_store")
        if persist_path is None:
            persist_path = os.getenv("CHROMA_PERSIST_DIRECTORY", "../vector_store")
        os.environ.setdefault("CHROMA_PERSIST_DIRECTORY", persist_path)
        
        # 최신 방식의 클라이언트 생성 (환경변수에 설정된 CHROMA_PERSIST_DIRECTORY 사용)
        self.client = chromadb.Client(settings=Settings(persist_directory=persist_path))

        
        # OpenAI 임베딩 함수 설정 (API 키 및 모델명 필요)
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if openai_api_key is None:
            raise RuntimeError("OPENAI_API_KEY is not set in environment variables")
        self.embedding_fn = OpenAIEmbeddingFunction(
            api_key=openai_api_key,
            model_name="text-embedding-ada-002"
        )
        
        # 컬렉션 가져오기 또는 생성하기 (임베딩 함수 연결)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_fn
        )
    
    def add_documents(self, documents: list[str], metadatas: list[dict] = None, ids: list[str] = None):
        if metadatas is None:
            metadatas = [{}] * len(documents)
        if ids is None:
            ids = [f"id_{i}" for i in range(len(documents))]
        self.collection.add(documents=documents, metadatas=metadatas, ids=ids)
    
    def add_document(self, doc_id: str, content: str, metadata: dict):
        try:
            self.add_documents([content], [metadata], [doc_id])
            return True
        except Exception as e:
            print(f"Error adding document {doc_id}: {e}")
            return False
    
    def query(self, query_text: str, top_k: int = 5):
        results = self.collection.query(query_texts=[query_text], n_results=top_k)
        return results
    
    def reset(self):
        self.client.reset()

# 싱글톤 인스턴스 생성 (persist_path는 .env에 설정된 값 "../vector_store"가 사용됨)
vector_service = VectorService()
