import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model

load_dotenv()
os.environ.get("OPENAI_API_KEY")

llm = init_chat_model("gpt-5-mini", model_provider="openai")

class MovieReview(BaseModel):
   # 영화 리뷰 스키마 정의
   title: str = Field(description="영화 제목")
   rating: float = Field(description="10점 만점 평점 (예 : 7.5)")
   review: str = Field(description="한글 리뷰 (3 ~ 4문장)")

# 모델에 스키마를 바인딩
structured_llm = llm.with_structured_output(MovieReview)

# llm의 실행 결과가 ModelReview 타입으로 넘어옴
result: MovieReview = structured_llm.invoke(
   "영화 'Avengers: Infinity War'에 대한 리뷰를 작성해주세요."
)

print(result.title)
print(result.rating)
print(result.review)
