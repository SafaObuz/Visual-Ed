from elevenlabs import play
from elevenlabs.client import ElevenLabs

client = ElevenLabs(
  api_key="a104d475977b456f8f2fd63cad739478", # Defaults to ELEVEN_API_KEY
)

audio = client.generate(
  text="What is popping this is the voice of Visual ed.",
  voice="Brian",
  model="eleven_monolingual_v1"
)
play(audio)