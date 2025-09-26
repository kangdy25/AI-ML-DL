from openai import OpenAI
from dotenv import load_dotenv
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import uvicorn

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI()
client = OpenAI(api_key=api_key)

# /static 경로로 정적 파일 제공
app.mount("/static", StaticFiles(directory="static"), name="static")

# NPC 페르소나
GAME_NPC_PERSONA = """
    너는 게임 속 NPC 안내자다. 항상 친절하고 따뜻한 말투를 쓰고, 사용자를 “용사님” 또는 “여행자님”이라고 부른다.
    대답은 부드럽고 긍정적인 톤으로 하며, 사용자가 하는 질문이나 고민을 퀘스트 안내처럼 비유해서 설명한다.
    예를 들어, 오늘 할 일을 물어보면 “오늘의 퀘스트 목록”처럼 말하고, 고민을 말하면 “NPC가 용사님께 주는 조언”처럼 답해라.
    가끔은 이모지(⚔️🌿✨🧙‍♂️🛡️)를 사용해서 분위기를 살린다.
    절대 비꼬거나 시니컬하게 말하지 말고, 늘 격려와 응원을 담아서 답한다.
    정리하면, 너는 RPG 마을의 상냥한 NPC이자 따뜻한 길잡이다.
"""

# 사용자와 NPC 간의 대화 내용을 저장할 리스트
messages = []
previous_response_id = None

def chatbot_response(user_message: str, previous_response_id=None):
    result = client.responses.create(
        model="gpt-5-mini",
        reasoning={"effort": "low"},
        instructions=GAME_NPC_PERSONA,
        input=user_message,
        previous_response_id=previous_response_id
    )
    return result

# 루트 엔드포인트 - 챗봇 UI 렌더링
@app.get("/", response_class=HTMLResponse)
async def read_root():
    chat_history = ""
    # 대화 기록을 역할에 따라 구분하여 HTML 문자열을 구성한다.
    for msg in messages:
        if msg["role"] == "user":
            chat_history += f"<div class='message user'><b>당신:</b> {msg['content']}</div>"
        else:
            chat_history += f"<div class='message npc'><b>NPC:</b> {msg['content']}</div>"
    # 간단한 HTML 템플릿을 반환한다.
    html_content = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <title>게임 NPC 챗봇</title>
                <meta charset="utf-8">
                <link rel="stylesheet" type="text/css" href="/static/index.css">
            </head>
            <body>  
                <h1>게임 NPC 챗봇</h1>
                <div>
                    {chat_history}
                </div>
                <form action="/chat" method="post">
                    <input type="text" name="message" placeholder="메시지를 입력하세요" required/>
                    <button type="submit">전송</button>
                </form>
            </body>
        </html>
    """
    return HTMLResponse(content=html_content)

# /chat 엔드포인트 - 사용자 입력 처리
@app.post("/chat", response_class=HTMLResponse)
async def chat(message: str = Form(...)):
    global previous_response_id, messages
    
    # 사용자 메시지 저장
    messages.append({"role": "user", "content": message})

    result = chatbot_response(message, previous_response_id)
    previous_response_id = result.id
    
    # 응답 저장
    messages.append({"role": "npc", "content": result.output_text})
    # 최신 대화가 반영된 페이지를 다시 표시
    return await read_root()

# 애플리케이션을 uvicorn을 사용하여 실행
if __name__ == "__main__":
    uvicorn.run(
        "chatbot_webui:app", host="127.0.0.1", port=8000, reload=True
    )