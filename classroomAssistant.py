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

    def ask_question(self):
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
            #print("Question: ")
            #print(self.currentQuestion["question"])
            # Print the options
            self.currentQuestion["options"] = options
            #print("Options:")
            #print(self.currentQuestion["options"])

            if len(self.currentQuestion["options"]) == 0:
                continue

            # Get the user's response for summary
            self.summary.append(response['chat_history'])

            if text == "end":
                break
            
            

            break #?

        return self.currentQuestion["question"], self.currentQuestion["options"]
    
    def give_response(self, response):
            self.summary.append(response)
            self.options = response

            self.currentQuestion = {
                "question": "",
                "options": []
            }


    def get_summary(self):
        llm = OpenAI(temperature=0.5, api_key=self.api_key)
        for i in range(len(self.summary)):
            self.summary_string = self.summary_string + self.summary[i] + ' '
        summarize = llm.invoke(self.summary_string)
        return(summarize)
    


