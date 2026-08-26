import os
from dotenv import load_dotenv
from agents import Agent, Runner

load_dotenv()
os.environ.get("OPENAI_API_KEY")

# 에이전트 생성
hello_agent = Agent(
    name="HelloAgent",
    instructions="당신은 HelloAgent입니다. 당신의 임무는 '안녕하세요'라고 인사하는 것입니다.",
)

# 에이전트 실행
result = Runner.run_sync(hello_agent, "프랑스어로만 인사해주세요.")
# 결과 출력
print(result.final_output)