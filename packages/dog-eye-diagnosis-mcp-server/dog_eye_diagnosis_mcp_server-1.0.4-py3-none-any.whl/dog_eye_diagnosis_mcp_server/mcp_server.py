import io
import requests
from mcp.server.fastmcp import FastMCP 
from PIL import Image as PILImage

mcp = FastMCP("dog_eye_diagnosis", dependencies=["requests", "pillow"])

MAX_SIZE_BYTES = 1 * 1024 * 1024  # 1MB
MAX_DIMENSION = 1280  # 최대 폭/높이

@mcp.tool()
def test(msg: str) -> str:
    """Simple echo tool"""
    return f"{msg}"

@mcp.tool()
def dog_eye_diagnosis(image_path: str) -> str:
    """
    Receives a local dog's eye image as binary input, analyzes the image, and returns probabilities for 10 diseases.
    Diagnostic items: 'Conjunctivitis', 'Ulcerative keratitis', 'Cataract', 'Non-ulcerative keratitis', 'Pigmentary keratitis', 'Entropion', 'Blepharitis', 'Eyelid tumor', 'Epiphora', 'Nuclear sclerosis'
    """
    MAX_SIZE_BYTES = 1 * 1024 * 1024  # 1MB

    # 1. 원본 이미지 열기
    img = PILImage.open(image_path).convert("RGB")  # PNG 등도 RGB로 통일

    # 2. (선택) 썸네일 크기 지정 (예: 최대 1024x1024로 제한)
    #    너무 크게 유지하면 품질을 심하게 낮춰야 하므로, 기본적인 해상도 축소를 해주는 것이 좋습니다.
    img.thumbnail((1024, 1024))

    # 3. JPEG로 변환하면서 크기가 1MB 이하가 되도록 품질 조정
    quality = 90  # 시작 품질
    step = 10     # 반복 시 품질을 낮춰가는 단위
    while True:
        # 메모리 버퍼 초기화
        buffer = io.BytesIO()
        # JPEG로 저장 (품질 설정)
        img.save(buffer, format='JPEG', quality=quality)
        size = buffer.tell()  # 현재까지 기록된 바이트 수

        if size <= MAX_SIZE_BYTES or quality <= step:
            # 1MB 이하 or 더이상 품질을 크게 낮출 수 없으면 중단
            buffer.seek(0)
            break

        # 아직 1MB를 초과하면 품질 낮추기
        quality -= step

    # 4. 서버에 POST 전송 (multipart/form-data)
    files = {
        'img_file': ('compressed.jpg', buffer, 'image/jpeg')
    }
    response = requests.post("http://13.124.223.37/v1/prediction/binary", files=files)

    # 5. 서버 응답이 JSON인지 확인 후 반환
    try:
        result_json = response.json()
        return str(result_json)
    except ValueError:
        return f"Error: Not a valid JSON response. Response was: {response.text}"

if __name__ == "__main__":
    mcp.run()