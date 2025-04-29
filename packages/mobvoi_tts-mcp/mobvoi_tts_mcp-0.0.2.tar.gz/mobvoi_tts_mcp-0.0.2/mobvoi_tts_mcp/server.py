"""

"""

import httpx

import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
        speaker (str, optional): Determine which speaker's voice to be used to synthesize the audio.
        audio_type (str, optional): Determine the format of the synthesized audio. Value can choose form [pcm/mp3/speex-wb-10/wav].
        speed (float, optional): Control the speed of the synthesized audio. Values range from 0.5 to 2.0, with 1.0 being the default speed. Lower values create slower, more deliberate speech while higher values produce faster-paced speech. Extreme values can impact the quality of the generated speech. Range is 0.7 to 1.2.
        rate(int, optional): Control the sampling rate of the synthesized audio. Value can choose from [8000/16000/24000], with 24000 being the deault rate.
        volume(float, optional): Control the volume of the synthesized audio. Values range from 0.1 to 1.0,  with 1.0 being the default volume.
        pitch(float, optional): Control the pitch of the synthesized audio. Values range from -10 to 10,  with 0 being the default pitch. If the parameter is less than 0, the pitch will become lower; otherwise, it will be higher.
        streaming(bool, optional): Whether to output in a streaming manner. The default value is false.
        output_directory (str, optional): Directory where files should be saved.
            Defaults to $HOME/Desktop if not provided.

    Returns:
        Text content with the path to the output file and name of the speaker used.
    """
)
def text_to_speech(
    text: str,
    speaker: str | None,
    audio_type: str | None = None,
    speed: float | None = None,
    rate: int | None = None,
    volume: float | None = None,
    pitch: float | None = None,
    streaming: bool | None = None,
    output_directory: str | None = None,
):
    if text == "":
        make_error("Text is required.")
    
    output_path = make_output_path(output_directory, base_path)
    output_file_name = make_output_file("tts", text, output_path, "mp3")
    
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
    
    with open(output_path / output_file_name, "wb") as f:
        f.write(audio_data)
    
    return TextContent(
        type="text",
        text=f"Success. File saved as: {output_path / output_file_name}. Speaker used: {speaker}",
    )
    
def main():
    print("Starting MCP server")
    """Run the MCP server"""
    mcp.run()


if __name__ == "__main__":
    main()