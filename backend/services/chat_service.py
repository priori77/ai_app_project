import os
from config.chat_config import ChatConfig
from config.openai_config import DesignerConfigs
from openai import OpenAI

class ChatService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def create_chat_completion(self, messages, designer_type="범용", conversation_id=None):
        try:
            # 디자이너 타입 로깅
            print(f"Received designer_type: {designer_type}")
            
            # 시스템 프롬프트와 GPT 설정 가져오기
            system_prompt = ChatConfig.get_system_prompt(designer_type)
            gpt_config = DesignerConfigs.get_config(designer_type)
            
            # 시스템 프롬프트(개발자 역할) + 유저 메시지
            full_messages = [{"role": "developer", "content": system_prompt}] + messages

            response = self.client.chat.completions.create(
                model=gpt_config["model"],
                messages=full_messages,
                reasoning_effort=gpt_config["reasoning_effort"],
                max_completion_tokens=gpt_config["max_completion_tokens"]
            )

            # --- 후처리(마크다운/markpage) ---
            raw_answer = response.choices[0].message.content
            formatted_answer = self._format_markdown_response(raw_answer)

            response_data = {
                "success": True,
                "message": formatted_answer,
                "designer_type": designer_type
            }
            print(f"Sending response with designer_type: {response_data['designer_type']}")
            return response_data

        except Exception as e:
            print(f"Chat completion error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "designer_type": designer_type
            }

    def _format_markdown_response(self, text):
        """
        GPT의 응답에 포함된 <markpage> 태그를 제거하고,
        최종적으로는 사용자 화면에 불필요한 태그가 표시되지 않도록 합니다.
        """
        if not text:
            return "답변이 없습니다."

        # 혹시 GPT가 이미 <markpage> 태그를 감싸서 응답했다면 제거
        cleaned = text.replace("<markpage>", "").replace("</markpage>", "").strip()
        # 최종 반환: markpage 태그 없이 그대로 전달
        return cleaned