import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI

load_dotenv()
os.environ.get("OPENAI_API_KEY")

# 채팅 모델 초기화
chat_model = ChatOpenAI(model="gpt-4.1-mini")

# 프롬프트 템플릿 정의
chat_prompt_template = ChatPromptTemplate.from_messages([
    ("system", "당신은 띠꺼운 AI 도우미입니다. 사용자의 질문을 3줄 요약 식으로 답하시오."),
    ("human", "{question}")
])

# 출력 파서 정의
string_output_parser = StrOutputParser()

# 프롬프트 템플릿을 사용하여 모델을 실행
result: AIMessage = chat_model.invoke(
    chat_prompt_template.format_messages(
        question="파이썬에서 리스트를 정렬하는 방법은?"
    )
)

# 결과를 str 형식으로 변환
parsed_result: str = string_output_parser.parse(result)
print(parsed_result.content)

print("-------------------------------------------------------------")

# 체인 생성 (LCEL)
chain = chat_prompt_template | chat_model | string_output_parser
print(type(chain))

# 체인 실행
result = chain.invoke({"question": "파이썬에서 리스트를 정렬하는 방법은?"})

# 결과 출력
print(type(result))
print(result)