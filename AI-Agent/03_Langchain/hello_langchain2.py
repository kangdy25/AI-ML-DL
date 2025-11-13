import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()
os.environ.get("ANTHROPIC_API_KEY")

model = init_chat_model("claude-sonnet-4-20250514", model_provider="anthropic") # LLM 초기화
result = model.invoke("랭체인이 뭔가요?") # 모델 실행
print(result.content) # 결괏값