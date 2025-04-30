import os, sys
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import httpx
from dotenv import load_dotenv

from mobvoi_tts_sdk import MobvoiTTS

load_dotenv()

# print("APP_KEY", os.getenv("APP_KEY"))

def main():
    custom_client = httpx.Client(
        timeout=10
    )
    
    client = MobvoiTTS(
        app_key = os.getenv("APP_KEY"),
        app_secret = os.getenv("APP_SECRET"),
        httpx_client = custom_client
    )
    
    text = '出门问问成立于2012年，是一家以语音交互和软硬结合为核心的人工智能公司，为全球40多个国家和地区的消费者、企业提供人工智能产品和服务。'
    output_dir = os.path.dirname(os.path.abspath("__file__"))
    
    content = client.generate(
        text=text,
    )
    
    output_file_path = os.path.dirname(os.path.abspath("__file__")) + f"/tests/test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    print(f"output_file_path: {output_file_path}")
    with open(output_file_path, "wb") as f:
        f.write(content)
        
if __name__ == "__main__":
    main()