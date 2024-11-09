from dotenv import load_dotenv

load_dotenv()
from main import AgentMain
from test_input import query, voice_path, image_path
object = AgentMain(0)
answer = object(query, voice_path, image_path)
with open("test_output.txt", "w") as f:
    f.write(answer)