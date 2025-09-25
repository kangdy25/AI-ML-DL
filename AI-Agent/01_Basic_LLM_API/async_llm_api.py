import asyncio
import os
import logging
import random

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from dotenv import load_dotenv
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic

load_dotenv()

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 비동기 클라이언트 생성
openai_client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
claude_client = AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# 테스트용 간헐적 실패 시뮬레이션 함수
async def simulate_random_failure():
    # 50% 확률로 실패 발생시키기
    if random.random() < 0.5:
        logger.warning("인위적으로 API 호출 실패 발생 (테스트용)")
        raise ConnectionError("인위적으로 발생시킨 연결 오류 (테스트용)")
    # 약간의 지연 시간 추가
    await asyncio.sleep(random.uniform(0.1, 0.5))

common_retry = retry( 
    stop=stop_after_attempt(3), # 최대 3번 시도
    wait=wait_exponential(multiplier=1, min=2, max=10), # 지수 백오프: 2초, 4초, 8초 ...
    retry=retry_if_exception_type(), # 모든 예외에 대해 재시도
    before_sleep=lambda retry_state: logger.warning(
        f"API 호출 실패: {retry_state.outcome.exception()}, {retry_state.attempt_number}번째 재시도 중..."
    )
)

@common_retry
async def call_async_openai(prompt: str, model: str = "gpt-5-mini") -> str:
    # 랜덤한 확률로 실패하는 call_async_openai 함수
    logger.info(f"OpenAI API 호출 시작: {model}")

    # 테스트를 위한 랜덤 실패 시뮬레이션
    await simulate_random_failure()

    # await을 사용하여 비동기적으로 API 응답을 기다린다
    response = await openai_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    logger.info("OpenAI API 호출 성공")
    return response.choices[0].message.content

@common_retry
async def call_async_claude(prompt: str, model: str = "claude-3-5-haiku-latest") -> str:
    logger.info(f"Claude API 호출 시작: {model}")

    # 테스트를 위한 랜덤 실패 시뮬레이션
    await simulate_random_failure()

    # await을 사용하여 비동기적으로 API 응답을 기다린다
    response = await claude_client.messages.create(
        model=model,
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    logger.info("Claude API 호출 성공")
    return response.content[0].text

async def main():
    print("동시에 API 호출하기 (재사용 로직 포함)")
    prompt = "비동기 프로그래밍에 대해서 두세 문장으로 설명해주세요."
    # 비동기 함수 호출 시 코루틴 객체 반환(실행은 아직 안됨)
    openai_task = call_async_openai(prompt)
    claude_task = call_async_claude(prompt)

    try:
        # 두 API 호출을 병렬로 실행하고 둘 다 완료될 때까지 대기
        # gather는 전체 작업 중 하나라도 실패하면 예외 발생
        openai_response, claude_response = await asyncio.gather(
            openai_task, claude_task, return_exceptions=False
        )
        print(f"OpenAI 응답: {openai_response}")
        print(f"Claude 응답: {claude_response}")
    except Exception as e:
        logger.error(f"API 호출 중 처리되지 않은 오류 발생: {e}")
        

if __name__ == "__main__":
    asyncio.run(main()) # 비동기 메인 함수를 이벤트 루프에서 실행