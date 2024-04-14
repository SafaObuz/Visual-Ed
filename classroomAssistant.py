from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

class ClassroomAssistant:
    def __init__(self, api_key, template):
        self.api_key = api_key
        self.template = template
        self.summary = self.summary = ["Summerize the following texts by figuring out what the user needs help with. It should be in first person as if the user is asking for the help. "]
        self.summary_string = ''
        self.options = ''
        self.currentQuestion = {
            "question": "",
            "options": []
        }

    def start_conversation(self):
        prompt = PromptTemplate.from_template(self.template)
        text = "Ask the first question"
        while text != "end":
            llm = OpenAI(temperature=0.5, api_key=self.api_key)
            memory = ConversationBufferMemory(memory_key="chat_history")
            conversation = LLMChain(
                llm=llm,
                prompt=prompt,
                #verbose=True,
                memory=memory
            )

            response = conversation({"question": text})

            self.options = response['text']
            question = self.options.split('\n')[0]
            options = [option[2:] for option in self.options.split('\n')[1:]]

            self.currentQuestion["question"] = question
            print("Question: ")
            print(self.currentQuestion["question"])

            

            # Print the options
            self.currentQuestion["options"] = options
            print("Options:")
            print(self.currentQuestion["options"])

            if len(self.currentQuestion["options"]) == 0:
                continue

            # Get the user's response for summary
            self.summary.append(response['chat_history'])

            if text == "end":
                break
            
            self.currentQuestion = {
                "question": "",
                "options": []
            }
            text = input("Enter your response: ")

            self.summary.append(text)
            
            self.options = response['text']

    def get_summary(self):
        llm = OpenAI(temperature=0.5, api_key=self.api_key)
        for i in range(len(self.summary)):
            self.summary_string = self.summary_string + self.summary[i] + ' '
        summarize = llm.invoke(self.summary_string)
        return(summarize)
    

if __name__ == "__main__":
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
    assistant.start_conversation()

    summary = assistant.get_summary()
    print("Conversation Summary:")
    print(summary)

