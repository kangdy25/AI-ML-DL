import os
from dotenv import load_dotenv
from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
os.environ.get("OPENAI_API_KEY")

prompt = ChatPromptTemplate.from_template(
    "주어진 '{word}'와 유사한 단어 3가지를 나열해주세요. 단어만 나열합니다."
)
model = ChatOpenAI(model="gpt-5-mini")
parser = StrOutputParser()

# 여러 분석을 동시에 수행
analysis_chain = RunnableParallel(
    synonyms = prompt | model | parser, # 유사어 분석
    word_count = RunnableLambda(lambda x : len(x["word"])), # 단어 수 계산
    uppercase = RunnableLambda(lambda x : x["word"].upper()) # 대문자로 변환
)

result = analysis_chain.invoke({"word": "peaceful"})
print(result)