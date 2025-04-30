"""
dog_eye_diagnosis_mcp_server 패키지

이 패키지는 강아지의 눈 이미지를 분석하여 10가지 안과 질환의 확률을 반환하는 MCP 서버를 제공합니다.
"""

from .mcp_server import puppy_eye_diagnosis, test

__all__ = ["puppy_eye_diagnosis", "test"]
