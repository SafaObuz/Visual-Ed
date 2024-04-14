# Visual-Ed

<img width="500" alt="hoyahacks" src="https://github.com/SafaObuz/Visual-Ed/assets/127442959/3b899692-363b-4159-b634-619f8980d6c1">







# Introduction
The Visual-Ed is an innovative project aimed at assisting individuals with mobility disability in classroom environments, particularly Locked-In syndrome. Locked-in syndrome is a condition in which a person is aware and awake but cannot move or communicate verbally due to complete paralysis of nearly all voluntary muscles except for the eyes. This project utilizes computer vision technology to provide these individuals with a means of communication and interaction within the classroom setting.

# Features
Eye Movement Detection: The system incorporates computer vision algorithms to detect the movement of the user's eyes, allowing them to interact with the assistant.
AI-Powered Assistance: Integrated with OpenAI's GPT-3 model, the assistant predicts and generates responses based on the user's input and context.
Multiple-Choice Interaction: The assistant engages users with multiple-choice questions, enabling them to respond using eye movements detected by the camera.
Raspberry Pi Integration: Built on a Raspberry Pi platform, the assistant is compact, affordable, and portable, making it suitable for use in various educational settings.
Graphical User Interface (GUI): The assistant features a user-friendly GUI for seamless interaction and accessibility.

# Requirements
To run the Locked-In Syndrome Classroom Assistant, ensure you have the following dependencies installed:
i) Python 3.7 or higher
ii) langchain==1.0.0 or higher
iii) python-dotenv==0.19.0 or higher
iv)  pygame
v) openai

Install the dependencies using the following command:
pip install -r requirements.txt

Usage
Connect the camera module to the Raspberry Pi and ensure it is properly configured.
Clone the repository to your Raspberry Pi.
Install the dependencies as described above.
Run the assistant script by executing python assistant.py in the terminal.
Follow the prompts on the GUI to interact with the assistant using eye movements.
Enjoy the enhanced communication and assistance provided by the Locked-In Syndrome Classroom Assistant!

# Contributing
Contributions to the project are welcome! If you'd like to contribute, please follow these steps:

Fork the repository.
Create a new branch for your feature or bug fix.
Make your changes and ensure the code passes all tests.
Commit your changes with clear and descriptive messages.
Push your changes to your fork.
Open a pull request to merge your changes into the main repository.

# License
This project is licensed under the MIT License. See the LICENSE file for more details.

# Acknowledgements
We would like to express our gratitude to the developers of OpenAI's GPT-3 model and the contributors to the langchain library for their invaluable contributions to this project.
