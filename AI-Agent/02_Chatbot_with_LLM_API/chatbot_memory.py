from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key=os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# previous_response_id 파라미터 추가
def chatbot_response(user_message: str, previous_response_id=None):
    result = client.responses.create(
        # previous_response_id 파라미터에 이전 대화의 ID 값을 넣는다.
        model="gpt-5-mini", input=user_message, previous_response_id=previous_response_id
    )
    return result

if __name__ == "__main__":
    previous_response_id = None
    try: 
        while True:
            user_message = input("메시지: ")
            if user_message.lower() == "exit":
                print("대화를 종료합니다.")
                break
            # 이전 대화의 ID 값을 추가로 넘겨준다.
            result = chatbot_response(user_message, previous_response_id)
            # 이전 대화의 ID를 response_id에 할당한다.
            previous_response_id = result.id
            print(result.output_text)
    except KeyboardInterrupt:
        print("\n사용자가 대화를 강제종료했습니다.")