
import logging
import httpx
import typing
import os, sys
import mobvoi_tts_mcp
from mobvoi_tts_mcp import __version__

# print(f"mobvoi_tts-mcp version: {mobvoi_tts_mcp.__version__}")
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

print(f"mobvoi_tts-mcp version: {__version__}")
logger.info("Running LOCAL version of mobvoi_tts_mcp server.py")  # 添加标记
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
from mobvoi_tts_sdk import MobvoiTTS
from mobvoi_tts_mcp.utils import (
    make_error,
    make_output_path,
    make_output_file,
)

load_dotenv()
app_key = os.getenv("APP_KEY")
app_secret = os.getenv("APP_SECRET")
base_path = os.getenv("MOBVOI_TTS_MCP_BASE_PATH")
print("base_path", base_path)
if not app_key:
    raise ValueError("Mobvoi_TTS_APP_KEY environment variable is required")
if not app_secret:
    raise ValueError("Mobvoi_TTS_app_secret environment variable is required")

custom_client = httpx.Client(
    timeout=10
)

client = MobvoiTTS(
    app_key = app_key,
    app_secret = app_secret,
    httpx_client = custom_client
)

mcp = FastMCP("MobvoiTTS")

@mcp.tool(
    description="""Convert text to speech with a given speaker and save the output audio file to a given directory.
    Directory is optional, if not provided, the output file will be saved to $HOME/Desktop.
    You can choose speaker by providing speaker parameter. If speaker is not provided, the default speaker(xiaoyi_meet) will be used.
    
    ⚠️ COST WARNING: This tool makes an API call to Mobvoi TTS service which may incur costs. Only use when explicitly requested by the user.
    
    Args:
        text (str): The text to convert to speech.
        speaker (str): Determine which speaker's voice to be used to synthesize the audio.
        audio_type (str): Determine the format of the synthesized audio. Value can choose form [pcm/mp3/speex-wb-10/wav].
        speed (float): Control the speed of the synthesized audio. Values range from 0.5 to 2.0, with 1.0 being the default speed. Lower values create slower, more deliberate speech while higher values produce faster-paced speech. Extreme values can impact the quality of the generated speech. Range is 0.7 to 1.2.
        rate(int): Control the sampling rate of the synthesized audio. Value can choose from [8000/16000/24000], with 24000 being the deault rate.
        volume(float): Control the volume of the synthesized audio. Values range from 0.1 to 1.0,  with 1.0 being the default volume.
        pitch(float): Control the pitch of the synthesized audio. Values range from -10 to 10,  with 0 being the default pitch. If the parameter is less than 0, the pitch will become lower; otherwise, it will be higher.
        streaming(bool): Whether to output in a streaming manner. The default value is false.
        output_directory (str): Directory where files should be saved.
            Defaults to $HOME/Desktop if not provided.

    Returns:
        Text content with the path to the output file and name of the speaker used.
    """
)
def text_to_speech(
    text: str,
    speaker:  typing.Optional[str] = "xiaoyi_meet",
    audio_type: typing.Optional[str] = "mp3",
    speed: typing.Optional[float] = 1.0,
    rate: typing.Optional[int] = 24000,
    volume: typing.Optional[float] = 1.0,
    pitch: typing.Optional[float] = 0.0,
    streaming: typing.Optional[bool] = False,
    output_directory: typing.Optional[str] = None,
):
    print("text_to_speech start.")
    
    logger.debug(f"Received text_to_speech call: text={text}, speaker={speaker}, audio_type={audio_type}")
    
    if text == "":
        make_error("Text is required.")
    
    output_path = make_output_path(output_directory, base_path)
    output_file_name = make_output_file("tts", text, output_path, "mp3")
    
    logger.debug(f"Output path: {output_path / output_file_name}")
    
    try:
        logger.debug("Calling Mobvoi TTS API")
        audio_data = client.generate(
            text=text,
            speaker=speaker,
            audio_type=audio_type,
            speed=speed,
            rate=rate,
            volume=volume,
            pitch=pitch,
            streaming=streaming
        )
        logger.debug(f"Received audio_data: {len(audio_data)} bytes")
        if len(audio_data) < 100:
            logger.error(f"Invalid audio data: {audio_data}")
            raise RuntimeError(f"Mobvoi TTS returned invalid data: {len(audio_data)} bytes")
        
    
        with open(output_path / output_file_name, "wb") as f:
            f.write(audio_data)
            logger.debug(f"Audio file written: {output_path / output_file_name}")
    
        return TextContent(
            type="text",
            text=f"Success. File saved as: {output_path / output_file_name}. Speaker used: {speaker}",
        )
    except httpx.HTTPStatusError as e:
        logger.error(f"Mobvoi API error: {e.response.text}")
        raise RuntimeError(f"Mobvoi API failed: {e.response.text}")
    except httpx.RequestError as e:
        logger.error(f"Network error: {str(e)}")
        raise RuntimeError(f"Network error: {str(e)}")
    except Exception as e:
        logger.exception(f"Error in text_to_speech: {str(e)}")
        raise
    
def main():
    logger.info("Starting MCP server")
    mcp.run()


if __name__ == "__main__":
    main()