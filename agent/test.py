from main import Main
from test_input import query, voice_path, image_path
object = Main(0)
answer = object(query, voice_path, image_path)
with open("test_output.txt", "w") as f:
    f.write(answer)