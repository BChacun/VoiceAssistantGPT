import pyttsx3
import speech_recognition as sr
import torch

from gpt4all import GPT4All

gptj = GPT4All("ggml-gpt4all-j-v1.3-groovy")



# Set up text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def process_input(input_text):

    '''   
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    model = GPT2LMHeadModel.from_pretrained('gpt2')

    input_ids = tokenizer.encode(input_text, return_tensors='pt')
    output = model.generate(input_ids, max_length=50, num_return_sequences=1)
    response_text = tokenizer.decode(output[0], skip_special_tokens=True)
    '''
    
    messages = [{"role": "user", "content": input_text}]
    response_dict = gptj.chat_completion(messages)

    response_text = response_dict["choices"][0]["message"]["content"]

    print(response_text)



    return response_text

def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio)
        print("You said:", query)
        return query
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        print("Sorry, I'm currently unavailable. Please try again later.")
        return ""

speak("Hello! How can I assist you today?")

while True:
    input_text = listen()

    if input_text:
        response_text = process_input(input_text)
        speak(response_text)

    # Exit condition
    if 'goodbye' in input_text.lower():
        speak("Goodbye!")
        break

