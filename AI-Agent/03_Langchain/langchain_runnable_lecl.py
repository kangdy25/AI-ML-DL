import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
os.environ.get("OPENAI_API_KEY")

prompt = ChatPromptTemplate.from_template(
    "주어지는 문구에 대하여 50자 이내의 짧은 시를 작성해주세요: {word}"
)

model = ChatOpenAI(model="gpt-5-mini")
parser = StrOutputParser()

# LECL로 체인 구성하기
chain = prompt | model | parser

# 실행하기 
result = chain.invoke({"word": "평범한 일상"})
print(result)