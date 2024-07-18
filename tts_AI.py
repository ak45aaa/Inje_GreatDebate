from openai import OpenAI
import pyglet

def tts(user_input, file_name='speech.mp3'):
  audio_bot = OpenAI(api_key='')

  speech_file_path = file_name
  response = audio_bot.audio.speech.create(
    model="tts-1-hd",
    voice="nova",
    speed = 1.2,
    input=user_input
  )

  response.stream_to_file(speech_file_path)
  song = pyglet.media.load(speech_file_path)
  song.play()