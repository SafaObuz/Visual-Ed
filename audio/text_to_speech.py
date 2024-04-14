from elevenlabs import play
from elevenlabs.client import ElevenLabs

client = ElevenLabs(
  api_key="c0589b977890a8d9eaff24e6619c5037", # Defaults to ELEVEN_API_KEY
)

audio = client.generate(
  text="I want to talk with teacher about leave of absence to do my past homework.",
  voice="Stalberts",
  model="eleven_monolingual_v1"
)
play(audio)