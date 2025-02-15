"""
OpenAI API configurations for different designer roles.
Each role has its own optimized parameters for the best possible responses.
"""

import os
from dotenv import load_dotenv

load_dotenv()

class BaseConfig:
    """기본 설정값을 제공하는 베이스 클래스"""
    API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL = "o3-mini"
    # o3-mini에서는 temperature, presence_penalty, frequency_penalty 대신 reasoning_effort를 사용합니다.
    REASONING_EFFORT = "high"
    MAX_COMPLETION_TOKENS = 4000

    @classmethod
    def validate(cls):
        """API 키가 설정되어 있는지 확인"""
        if not cls.API_KEY:
            raise ValueError("OpenAI API key is not set in environment variables")
        return True

class DesignerConfigs:
    """각 디자이너 역할별 최적화된 설정"""
    
    WORLD_DESIGNER = {  # 레벨 디자이너용
        "model": "o3-mini",
        "reasoning_effort": "medium",
        "max_completion_tokens": 4000
    }
    
    SYSTEM_DESIGNER = {
        "model": "o3-mini",
        "reasoning_effort": "medium",
        "max_completion_tokens": 4000
    }
    
    QUEST_DESIGNER = {
        "model": "o3-mini",
        "reasoning_effort": "medium",
        "max_completion_tokens": 4000
    }
    
    NARRATIVE_DESIGNER = {
        "model": "o3-mini",
        "reasoning_effort": "high",  # 내러티브 디자이너는 더 심도 있는 분석이 필요할 수 있음
        "max_completion_tokens": 4000
    }
    
    # 범용 디자이너 설정 (기존 ChatbotConfig 값 사용)
    GENERAL = {
        "model": "o3-mini",
        "reasoning_effort": "medium",
        "max_completion_tokens": 4000
    }

    @classmethod
    def get_config(cls, designer_type):
        """
        디자이너 타입에 따른 설정을 반환합니다.
        Args:
            designer_type (str): "레벨 디자이너", "시스템 디자이너" 등의 한글 타입명
        Returns:
            dict: 해당 디자이너 타입의 GPT 설정값
        """
        mapping = {
            "레벨 디자이너": cls.WORLD_DESIGNER,
            "시스템 디자이너": cls.SYSTEM_DESIGNER,
            "퀘스트 디자이너": cls.QUEST_DESIGNER,
            "내러티브 디자이너": cls.NARRATIVE_DESIGNER,
            "범용": cls.GENERAL
        }
        return mapping.get(designer_type, cls.GENERAL)

    @classmethod
    def validate(cls):
        """설정값들이 올바른지 확인"""
        if not BaseConfig.API_KEY:
            raise ValueError("OpenAI API key is not set in environment variables")
        return True

# 기존 ChatbotConfig는 범용 설정으로 사용 (하위 호환성 유지)
class ChatbotConfig(BaseConfig):
    """범용 챗봇 설정 (기존 코드와의 호환성을 위해 유지)"""
    MODEL = DesignerConfigs.GENERAL["model"]
    REASONING_EFFORT = DesignerConfigs.GENERAL["reasoning_effort"]
    MAX_COMPLETION_TOKENS = DesignerConfigs.GENERAL["max_completion_tokens"]

class ReviewAnalysisConfig(BaseConfig):
    """리뷰 분석을 위한 최적화된 설정"""
    MODEL = "o3-mini"
    REASONING_EFFORT = "high"
    MAX_COMPLETION_TOKENS = 2500  # 리뷰 분석에 충분한 토큰