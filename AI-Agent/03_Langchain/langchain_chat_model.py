import os
import random
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()
os.environ.get("OPENAI_API_KEY")
os.environ.get("ANTHROPIC_API_KEY")

if random.random() < 0.5: # 50%의 확률로 gpt-5-mini를 선택
    print("gpt-5-mini selected")
    model = init_chat_model("gpt-5-mini", model_provider="openai")
else: 
    print("claude-sonnet-4-20250514 selected")
    model = init_chat_model("claude-sonnet-4-20250514", model_provider="anthropic") # 모델 생성

result = model.invoke("RAG가 뭔가요?")
print(result.content)