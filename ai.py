from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
'''
#instantiate the language model
llm = OpenAI(temperature=0.1, api_key='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')

# Look how "chat_history" is an input variable to the prompt template
template = """

You are AI assistant which asks questions with 5 short multiple choice style 
answers to a human to try to understand what this person wants to say or need. 
This person is the classsrom environment right now, so the conversions would 
be about school topics and possible needs in school such as needing to restroom.
You should ask questions to get answer from, the user from the multiple choices
to narrow down to predict what user wants to say or learn in curren situtation.
You will only ask multiple choice question. Each question will only have at max 5 options


Previous conversation:
{chat_history}

New human question: {question}
Response:
"""

prompt = PromptTemplate.from_template(template)

# Notice that we need to align the `memory_key`

memory = ConversationBufferMemory(memory_key="chat_history")

conversation = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True,
    memory=memory
)

text = "Ask the first question"
response = conversation({"question":text})
print(response['text'])
'''


text = ""
def chat(api_key, text):
    template = """
    You are AI assistant which asks questions with 5 short multiple choice style 
    answers to a human to try to understand what this person wants to say or need. 
    This person is the classsrom environment right now, so the conversions would 
    be about school topics and possible needs in school such as needing to restroom.
    You should ask questions to get answer from, the user from the multiple choices
    to narrow down to predict what user wants to say or learn in curren situtation.
    You will only ask multiple choice question. Each question will only have at max 5 options


    Previous conversation:
    {chat_history}

    New human question: {question}
    Response:

    """

    prompt = PromptTemplate.from_template(template)

    while True:
        if text == "":
            text = "Ask the first question"
            continue
        else:
            llm = OpenAI(temperature=0.1, api_key=api_key)
            memory = ConversationBufferMemory(memory_key="chat_history")
            conversation = LLMChain(
                llm=llm,
                prompt=prompt,
                verbose=True,
                memory=memory
            )
            text = input("Enter your response: ")
            response = conversation({"question":text})
            print(response['text'])

if __name__ == "__main__":
    print(chat("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", text))



        