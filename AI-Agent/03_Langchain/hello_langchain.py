import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()
os.environ.get("OPENAI_API_KEY")

model = init_chat_model("gpt-5-mini", model_provider="openai") # LLM 초기화
result = model.invoke("랭체인이 뭔가요?") # 모델 실행
print(type(result)) # AIMessage 타입
print(result.content) # 결괏값