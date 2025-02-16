from dotenv import load_dotenv
import os
from openai import OpenAI

# .env 파일 로드
load_dotenv()

def test_openai_api():
    try:
        # API 키 확인
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Error: OPENAI_API_KEY not found in environment variables")
            return

        # OpenAI 클라이언트 초기화 (v1.x 방식)
        client = OpenAI(api_key=api_key)
        
        # 간단한 임베딩 테스트
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input="Hello, world!"
        )
        
        # 결과 확인
        print("API 호출 성공!")
        print("임베딩 차원:", len(response.data[0].embedding))
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    test_openai_api()