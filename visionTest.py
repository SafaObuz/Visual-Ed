import cv2
from vision.visionController import VisionController
from classroomAssistant import ClassroomAssistant

from elevenlabs import play
from elevenlabs.client import ElevenLabs

from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

visionController = VisionController()


client = ElevenLabs(
  api_key="c0589b977890a8d9eaff24e6619c5037", # Defaults to ELEVEN_API_KEY
)

api_key = openai_api_key
template = """
You are an AI assistant designed to help disabled students communicate by asking multiple-choice questions. Your goal is to understand what the student wants to say or needs assistance with. As the student cannot speak, you will communicate solely through multiple-choice questions. Each question should be concise and have five short options.

Since the student is in a classroom environment, conversations will revolve around school topics and potential needs, such as restroom breaks, requesting help from the teacher, or understanding academic material. Remember, the student may have difficulty expressing themselves, so your questions should be clear and easy to understand.

Here are some guidelines for crafting effective questions:

1. Start by asking what type of assistance the student needs.

2. Avoid complex or lengthy questions, as the student may find them difficult to answer.

3. Always include an "Other" option in each question to allow the student to provide additional information if none of the provided options fit their needs.

4. If the student selects "Other," ask follow-up questions to understand their needs better. You can try asking different multiple-choice questions to narrow down the student's needs.

5. Always provide an option to end the conversation if the student is finished or cannot continue.

6. Never ask yes or no questions. Always provide multiple options to choose from.

7. When you don't understand the student's question, repeat the question in your response. This shows that you are actively listening and trying to help.

8. Don't add questions in the options. Only add what the user might want to say. For example, "I want to go to the restroom," "I want to ask a question," etc.

9. Please don't give me empty options. Always provide me with 5 options. If the student selects "Other" and the options are empty, repeat the question: "What kind of assistance does the student need?"

Your primary objective is to understand the student's needs and provide appropriate assistance. Keep the conversation history in mind to maintain context and continuity. 

Previous conversation:
{chat_history}
New human question: {question}
Response:

"""
assistant = ClassroomAssistant(api_key, template)

def talk(text):
    audio = client.generate(
    text=text,
    voice="Stalberts",
    model="eleven_monolingual_v1"
    )
    play(audio)

while True:
    question, options = assistant.ask_question()
    print(question)
    print(options)

    string = question + " your are options are"
    for option in options:
        string += option + " "
    talk(string)

    option = input()
    assistant.give_response(option)
    """visionController.process()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    """
        
visionController.close()