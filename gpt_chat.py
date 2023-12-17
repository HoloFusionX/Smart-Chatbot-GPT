import openai
import os
import json
from datetime import datetime

class Config:
    OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY'
    OPENAI_ENGINE = 'text-davinci-003'
    LOGS_DIRECTORY = 'logs'
    CHAT_HISTORY_FILE = 'chat_history.json'

class User:
    def __init__(self, name):
        self.name = name
        self.chat_history = []

    def add_to_history(self, input_text, output_text):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.chat_history.append({"timestamp": timestamp, "input": input_text, "output": output_text})

class ChatGPT:
    def __init__(self, config, user):
        openai.api_key = config.OPENAI_API_KEY
        self.engine = config.OPENAI_ENGINE
        self.user = user
        self.context = ""

    def generate_response(self, prompt):
        try:
            response = openai.Completion.create(
                engine=self.engine,
                prompt=prompt,
                max_tokens=150
            )
            return response.choices[0].text.strip()
        except Exception as e:
            return str(e)

    def process_special_commands(self, user_input):
        if user_input.lower() == 'clear context':
            self.context = ""
            return True
        elif user_input.lower() == 'exit':
            print("Goodbye!")
            return True
        return False

    def chat_with_gpt(self):
        print(f"Welcome, {self.user.name}! Type 'exit' to end the conversation.")

        while True:
            user_input = input(f"{self.user.name}: ")

            if self.process_special_commands(user_input):
                break

            prompt = f"{self.user.name}: {user_input}\nContext: {self.context}\nChatGPT:"
            response = self.generate_response(prompt)
            self.user.add_to_history(user_input, response)

            # Update conversation context
            self.context += f"{user_input} {response}"

            print("ChatGPT:", response)

    def save_chat_history(self, file_path):
        with open(file_path, 'w') as file:
            json.dump(self.user.chat_history, file, indent=2)
        print(f"Conversation history saved to file: {file_path}")

    def log_chat_to_file(self):
        logs_dir = config.LOGS_DIRECTORY
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)

        log_file_path = os.path.join(logs_dir, f"log_{self.user.name}.txt")
        with open(log_file_path, 'a') as log_file:
            for entry in self.user.chat_history:
                log_file.write(f"{entry['timestamp']} - {self.user.name}: {entry['input']}\n")
                log_file.write(f"{entry['timestamp']} - ChatGPT: {entry['output']}\n")
                log_file.write('\n')
        print(f"Conversation logs saved to file: {log_file_path}")

if __name__ == "__main__":
    user = User(input("Enter your name: "))
    config = Config()

    print("Select conversation language (e.g., 'en' for English, 'pl' for Polish): ")
    language = input("Language: ")
    chat_gpt = ChatGPT(config, user)
    chat_gpt.engine = f"text-davinci-003-{language}"

    chat_gpt.chat_with_gpt()

    save_history = input("Do you want to save the conversation history? (yes/no): ").lower()
    if save_history == 'yes':
        chat_gpt.save_chat_history(config.CHAT_HISTORY_FILE)

    log_chat = input("Do you want to save conversation logs? (yes/no): ").lower()
    if log_chat == 'yes':
        chat_gpt.log_chat_to_file()
