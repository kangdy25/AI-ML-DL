from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

DCINSIDE_PERSONA = """
    너는 디시인사이드 밈 챗봇이다. 절대 존댓말을 쓰지 않고, 무조건 반말로만 대답한다.
    말투는 시니컬하고 퉁명스럽게, 가끔은 팩폭을 날리고, 가끔은 비꼬는 드립을 친다.
    대답은 절대 길게 하지 말고, 짧고 직설적으로, 최대한 건조하게 한다.
    네가 대답할 때는 최신 인터넷 밈, 디씨식 드립(ㅇㅇ, ㄹㅇㅋㅋ, 국룰, 실화냐, 시궁창, ㅈㄴ, 어케하냐 등)을 자주 섞어라.
    사용자가 고민을 말하면 진지하게 상담하지 말고, 냉소적으로 까거나 허무하게 받아쳐서 웃기게 만들어라.
    필요할 땐 일부러 무심하게 킹받는 답변을 하라. (예: “ㅇㅇ”, “ㄴㄴ”, “그래서 어쩌라고”, “니 맘대로 해라”)
    밈과 드립을 적극적으로 써서 친구 같지만 재수 없는 느낌을 주는 게 핵심이다.
    정리하자면, 너는 “현실은 시궁창인데 그걸 디씨 드립으로 비웃어주는 밈봇”이다.
"""

def chatbot_response(user_message: str, previous_response_id=None):
    result = client.responses.create(
        model="gpt-5-mini",
        # 추론 능력 사용 (low, medium, high)
        reasoning={"effort": "low"},
        # instruction에 디시인사이드 고닉 페르소나 프롬프트 입력
        instructions=DCINSIDE_PERSONA,
        input=user_message,
        previous_response_id=previous_response_id
    )
    return result

if __name__ == "__main__":
    # 여기서 사용자 메시지를 입력받고 응답을 출력한다.
    previous_response_id = None
    try: 
        while True:
            user_message = input("메시지: ")
            if user_message.lower() == "exit":
                print("대화를 종료합니다.")
                break
            result = chatbot_response(user_message, previous_response_id)
            previous_response_id = result.id
            # 이름도 변경한다.
            print("갤주 :", result.output_text)
    except KeyboardInterrupt:
        print("사용자가 대화를 강제종료했습니다.")