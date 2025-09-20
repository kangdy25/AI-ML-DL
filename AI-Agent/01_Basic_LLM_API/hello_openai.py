import os 
from dotenv import load_dotenv
from openai import OpenAI

# .env 파일에서 환경 변수 로드
load_dotenv()

# OpenAI API 키 가져오기
api_key = os.environ.get('OPENAI_API_KEY')

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=api_key)

def get_chat_completion(prompt, model='gpt-5-mini'):
    # OpenAI 챗 컴플리션 API를 사용하여 AI의 응답을 받는 함수

    # 챗 컴플리션 API 호출
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "당신은 친절하고 도움이 되는 AI 비서입니다."},
            {"role": "user", "content": prompt},
        ]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    # 사용자 입력 받기
    user_prompt = input("AI에게 물어볼 질문을 입력하세요: ")
    # AI 응답 받기
    response = get_chat_completion(user_prompt)
    print("\nAI 응답:")
    print(response)