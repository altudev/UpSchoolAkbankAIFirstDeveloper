from openai import OpenAI
from ..config import Config
from ..models.chat import ChatMessage

class ChatService:
    def __init__(self, db_session):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.db_session = db_session

    def generate_response(self, messages, model):
        try:
            stream = self.client.chat.completions.create(
                model=model,
                messages=[{"role": m.role, "content": m.content} for m in messages],
                stream=True,
            )
            full_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
            return full_response
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")

    def save_message(self, role, content, model):
        message = ChatMessage(role=role, content=content, model=model)
        self.db_session.add(message)
        self.db_session.commit()
        return message

    def get_chat_history(self):
        return self.db_session.query(ChatMessage).order_by(ChatMessage.timestamp).all()