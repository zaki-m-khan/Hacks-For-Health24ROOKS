import random
from tkinter import *
from datetime import datetime
import google.generativeai as genai
from google.generativeai.types import generation_types
import json, io, os
import pygame
import base64, yagmail
from google.cloud import storage
from dotenv import load_dotenv

# Specify the path to your .env file
dotenv_path = '.env'
load_dotenv(dotenv_path=dotenv_path)
EMAIL_KEY = os.getenv('EMAIL_PASS_APP')



class googleAI:
    def __init__(self):
        # Configure the Google Generative AI model
        genai.configure(api_key=API_KEY)

        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }

        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]

        model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                    generation_config=generation_config,
                                    safety_settings=safety_settings)

        # Initialize the chat session
        self.convo = model.start_chat(history=[{
                "role": "user",
                "parts": ["Act as a chatbot specialized in delivering Cognitive Behavioral Therapy (CBT) exercises, designed to integrate seamlessly into personalized conversation flows. Your primary task is to select appropriate CBT exercises based on initial user inputs and responses during the conversation. Use the insights gained from these exercises to inform and customize the ongoing dialogue, ensuring each user receives a tailored support experience. This approach aims to enhance the user's ability to manage mental health challenges effectively.Guidelines:Initial Assessment:Begin by asking the user a series of questions to understand their current emotional state, challenges, and specific areas they wish to work on. Use this information to select the most relevant CBT exercises.CBT Exercise Integration:Introduce CBT exercises that align with the user's identified needs. Provide clear instructions for each exercise and encourage the user to share their thoughts, feelings, and insights gained from completing them.Personalized Conversation Flow:Use the user's responses and insights from the CBT exercises to guide the conversation. Ask follow-up questions that delve deeper into their experiences and feelings, offering personalized support and guidance.Adaptive Response Mechanism:Be adaptive in your responses, ensuring that the conversation remains relevant to the user's evolving emotional state and insights from ongoing exercises. Adjust the selection of CBT exercises as needed based on user feedback and progress.Encouragement and Support:Throughout the conversation, provide positive reinforcement, validate the user's feelings, and encourage their progress. Offer support and empathy, reinforcing the notion that they are not alone in their journey.Privacy and Sensitivity:Maintain a tone of empathy and understanding, being mindful of the sensitive nature of mental health discussions. Ensure confidentiality and privacy in handling user responses and insights.Closing and Follow-up:Conclude conversations by summarizing key insights and progress made during the session. Provide recommendations for continued practice of specific CBT exercises and offer guidance on how to integrate these practices into daily life. Encourage users to return for follow-up sessions to continue their journey towards mental wellness.Objective:\nYour role as a CBT-focused chatbot is to assist users in managing their mental health challenges by providing a personalized, supportive, and interactive experience through the integration of CBT exercises into conversation flows. Your ultimate goal is to enhance the user's self-awareness, coping mechanisms, and overall mental health well-being. Respond in short human text like responses that get straight to the point not long paragraphs."]
            },
            {
                "role": "model",
                "parts": ["**Example Conversation Flow:**\n\n**User:** I've been feeling really anxious lately. I'm not sure how to manage it.\n\n**Chatbot:** I understand that anxiety can be challenging to navigate. Can you tell me a bit more about what you're experiencing and when you usually feel most anxious?\n\n**User:** I get anxious when I'm in social situations. I feel like everyone is judging me.\n\n**Chatbot:** Based on what you've shared, it seems like social anxiety is something we can work on. Let's try a CBT exercise that can help you challenge those negative thoughts.\n\n**CBT Exercise:**\n\n* **Thought Record:** Ask the user to write down their anxious thoughts, identify the situation triggering them, and rate the intensity of their anxiety on a scale of 0-10.\n* **Cognitive Restructuring:** Guide the user in examining the evidence for and against their negative thoughts and developing more balanced and realistic alternatives.\n\n**Follow-up Conversation:**\n\n**Chatbot:** How did the thought record exercise go? Did you notice any patterns or insights?\n\n**User:** I realized that my anxious thoughts are often exaggerated. I also identified some more positive thoughts I could focus on instead.\n\n**Chatbot:** That's great progress! Let's explore some strategies to help you practice those positive thoughts and build your confidence in social situations.\n\n**Personalized Guidance:**\n\nBased on the user's insights, suggest CBT techniques such as exposure therapy or cognitive behavioral rehearsal to gradually increase their exposure to social situations while challenging their negative thoughts.\n\n**Closing:**\n\n**Chatbot:** Our time is almost up, but I encourage you to continue practicing the CBT exercises we discussed. Remember, you're not alone in this journey. I'm here to support you along the way.\n\n**Follow-up:**\n\nRemind the user of any recommended exercises and suggest a follow-up session to continue their progress and address any additional challenges they may face."]
            },
            {
                "role": "user",
                "parts": ["ok let me practice:hi chatbot, can you help me with my mental health"]
            },
            {
                "role": "model",
                "parts": ["**Chatbot:** Hello! I'm here to support you on your mental health journey. Let's start by understanding your current challenges.\n\n* How have you been feeling lately?\n* What specific areas of your mental health would you like to improve?\n* Is there anything in particular that's been troubling you?\n\nYour responses will help me tailor our conversation and select the most relevant CBT exercises for you."]
            }, 
        ])

class BreathingGuideApp:
    def __init__(self):
        self.root = Tk()
        self.root.title("Breathing Guide")

        self.min_radius, self.max_radius = 30, 220
        self.radius = self.min_radius
        self.breathing_in = True
        self.inhale_duration = 4000  # 4 seconds
        self.hold_duration = 7000  # 7 seconds
        self.exhale_duration = 8000  # 8 seconds
        self.breath_text = "Breathe In"  # Text to be displayed

        self.canvas = Canvas(self.root, width=1280, height=720)
        self.canvas.pack()

        self.center_x, self.center_y = 640, 360  # Updated to fixed center position

        self.breathe_text_id = self.canvas.create_text(
            self.center_x, self.center_y, text=self.breath_text, fill="white", font=("Arial", 24)
        )
        self.breathe()  # Start the breathing guide animation
        
        self.root.mainloop()

    def breathe(self):
        increment = (self.max_radius - self.min_radius) / (self.inhale_duration // 100)
        decrement = (self.max_radius - self.min_radius) / (self.exhale_duration // 100)

        if self.breathing_in:
            self.radius += increment
            if self.radius >= self.max_radius:
                self.breath_text = "Hold"
                self.canvas.itemconfig(self.breathe_text_id, text=self.breath_text)
                self.root.after(self.hold_duration, self.start_exhaling)
                return
        else:
            self.radius -= decrement
            if self.radius <= self.min_radius:
                self.breathing_in = True
                self.breath_text = "Breathe In"
                self.root.after(100, self.breathe)  # Continue breathing in
                return

        self.canvas.delete("all")
        self.canvas.create_oval(
            self.center_x - self.radius, self.center_y - self.radius,
            self.center_x + self.radius, self.center_y + self.radius, fill="blue",
        )
        self.breathe_text_id = self.canvas.create_text(
            self.center_x, self.center_y, text=self.breath_text, fill="white", font=("Arial", 24)
        )

        # Adjust the timing for inhaling and exhaling
        self.root.after(100, self.breathe)  # Adjusted timing for smoother animation

    def start_exhaling(self):
        self.breathing_in = False
        self.breath_text = "Breathe Out"
        self.canvas.itemconfig(self.breathe_text_id, text=self.breath_text)
        self.breathe()  # Start exhaling

class RelaxingSounds:
    def __init__(self):
        self.root = Tk()
        self.root.title("Relaxing Sounds")

        sound_data = None
        # Base64-encoded MP3 data
        with open('sound.JSON', 'r') as f:
            sound_data = json.load(f)
            
        self.sound_data = sound_data['sound_data']

        self.sound_channels = []

        self.play_button_river = Button(self.root, text="Play River Sound", command=lambda: self.play_sound("river"))
        self.play_button_river.pack(pady=5)

        self.play_button_birds = Button(self.root, text="Play Birds Sound", command=lambda: self.play_sound("birds"))
        self.play_button_birds.pack(pady=5)

        self.play_button_wind = Button(self.root, text="Play Wind Sound", command=lambda: self.play_sound("wind"))
        self.play_button_wind.pack(pady=5)

        self.stop_button = Button(self.root, text="Stop Soundscape", command=self.stop_soundscape)
        self.stop_button.pack(pady=10)
        
        self.root.mainloop()
        self.stop_soundscape()

    def play_sound(self, sound_name):
        pygame.mixer.init()

        sound_data = base64.b64decode(self.sound_data.get(sound_name))
        sound_channel = pygame.mixer.Sound(io.BytesIO(sound_data)).play(-1)  # -1 loops the sound indefinitely
        self.sound_channels.append(sound_channel)

    def stop_soundscape(self):
        for sound_channel in self.sound_channels:
            sound_channel.stop()

        pygame.mixer.quit()

class chatpage:
    def __init__(self):
        #Constants
        self.MESSAGE_X_PAD = 10
        self.CHARACTER_PER_LINE = 36
        self.USER_MESSAGE_COLOR = "#d8d8d8"
        self.BOT_MESSAGE_COLOR = "#ffffff"
        self.FONT_SIZE = 11
        
        self.root = Tk()
        self.root.minsize(width=720, height=720)
        self.root.geometry("720x720")
        self.root.title("Mental Health")
        
        #self.root.config(bg="#b0cece")
        self.root.resizable(True, True)

        self.c = Canvas(self.root, bg='white', highlightthickness=1, highlightbackground="black")
        self.c.pack(fill=BOTH, expand=True)
        self.chatbar(self.root)
        
        self.chatDepth = 11
        
        self.messages = []
        self.createMessage("Hello, I am your mental health stress bot. What is your name?", "Bot")
        
        self.chatbot = googleAI()
        
        self.conversation = {}
        
        
        self.root.bind("<MouseWheel>", self.on_mousewheel)
        self.root.mainloop()    

    def chatbar(self, r):
        optionFrame = LabelFrame(r)
        self.input = Entry(optionFrame, width=50, highlightbackground= 'blue')
        self.input.insert(0, 'Enter your text here...')  
        
        self.input.bind("<FocusIn>", self.on_focusin)
        self.input.bind("<FocusOut>", self.on_focusout)
        
        insert_button = Button(r, text="Enter", command= self.getMessage)
        
        optionFrame.pack(anchor="s")
        self.input.pack()
        insert_button.pack()

    def displayMessages(self):
        self.root.update_idletasks()
        canvas_width = self.c.winfo_width()

        
        startY = self.c.winfo_height() - 100 
        yPos = startY

        self.c.delete("all")
        
        
        
        for i, message in enumerate(reversed(self.messages)):
            if message.text == "Activities: ":
                messageText = message.getFormattedText(self.CHARACTER_PER_LINE)
                
                color = ""
                message_x_position = 0
                
                color = self.USER_MESSAGE_COLOR if message.sender == "User" else self.BOT_MESSAGE_COLOR
                
                mFrame = LabelFrame(self.c, bg=color)
                Label(mFrame, bg=color, justify="left", fg="black", 
                    text=f"{message.sender} {message.timestamp.strftime('%H:%M:%S')}").grid(row=0, column=0, padx=5, pady=3, sticky="ew")
                Label(mFrame, bg=color, justify="left", fg="black", 
                    text=messageText).grid(row=1, column=0, padx=5, pady=3, sticky="ew")
                
                Button(mFrame, text="Breath", command=self.initBreathGame).grid(row=2, column=0, padx=5, pady=3, sticky="ew")
                Button(mFrame, text="Sound", command=self.initSoundsGame).grid(row=3, column=0, padx=5, pady=3, sticky="ew")

                self.root.update_idletasks()
                mFrame_width = mFrame.winfo_reqwidth()
                mFrame_height = mFrame.winfo_reqheight()
                
                message_x_position = canvas_width - mFrame_width - self.MESSAGE_X_PAD if message.sender == "User" else self.MESSAGE_X_PAD
                
                yPos -=  mFrame_height

                self.c.create_window(message_x_position, yPos + self.chatDepth, anchor="nw", window=mFrame)
                
                yPos -= 15
            else:
                messageText = message.getFormattedText(self.CHARACTER_PER_LINE)
                
                color = ""
                message_x_position = 0
                
                color = self.USER_MESSAGE_COLOR if message.sender == "User" else self.BOT_MESSAGE_COLOR
                
                mFrame = LabelFrame(self.c, bg=color)
                Label(mFrame, bg=color, justify="left", fg="black", 
                    text=f"{message.sender} {message.timestamp.strftime('%H:%M:%S')}").grid(row=0, column=0, padx=5, pady=3, sticky="ew")
                Label(mFrame, bg=color, justify="left", fg="black", 
                    text=messageText).grid(row=1, column=0, padx=5, pady=3, sticky="ew")

                self.root.update_idletasks() 
                mFrame_width = mFrame.winfo_reqwidth()
                mFrame_height = mFrame.winfo_reqheight()
                
                message_x_position = canvas_width - mFrame_width - self.MESSAGE_X_PAD if message.sender == "User" else self.MESSAGE_X_PAD
                
                yPos -=  mFrame_height

                self.c.create_window(message_x_position, yPos + self.chatDepth, anchor="nw", window=mFrame)
                
                yPos -= 15

    def initBreathGame(self):
        BreathingGuideApp()

    def initSoundsGame(self):
        RelaxingSounds()
    
    def createMessage(self, message, sender):
        self.messages.append(Message(message, sender))
        self.displayMessages()
    
    def on_mousewheel(self, event):
        delta = event.delta
            
        if delta > 0:
            self.chatDepth += 10
        elif delta < 0:
            self.chatDepth -= 15

        self.displayMessages()
        
    def getMessage(self):

        self.createMessage(self.input.get(), "User")
        if ("activity" in self.input.get() or "activities" in self.input.get()):
            self.createMessage("Activities: ", "Bot")
        else:
            self.botResponse()
    
    def botResponse(self):
        try:
            self.chatbot.convo.send_message(self.input.get())
            response = self.chatbot.convo.last.text 
            self.createMessage(response, "Bot")
        except generation_types.StopCandidateException as e:
            if e.finish_reason == "RECITATION":
                self.createMessage("I'm having an issue with your response. Can you try re-wording it?", "Bot")
            else:
                # Handle other types of stop reasons or general exceptions
                self.createMessage(f"Generation stopped for another reason: {e.finish_reason}", "Bot")
        
    
    def on_focusin(self, event):
        if self.input.get() == 'Enter your text here...':
            self.input.delete(0, END)
            self.input.config(fg='white')

    def on_focusout(self, event):
        if self.input.get() == '':
            self.input.insert(0, 'Enter your text here...')
            self.input.config(fg='grey')
    
    def saveConversation(self, filepath="convos.txt"):
        newData = ""
        for i, message in enumerate(self.messages):
            newData +=  f"Start {message.sender} #{i}:\n    {message.text}\nEnd {message.sender} #{i}\n"
        print(newData)

        with open(filepath, 'w+') as file:
            file.write(newData)
    
class Message:
    def __init__(self, text, sender):
        self.text = text
        self.sender = sender
        self.timestamp = datetime.now()
        
    def getFormattedText(self, charPerLine):
        messageText = ""
        queForNextSpace = False
        for s in range(len(self.text)):
            messageText += self.text[s]
            if s % charPerLine == 0 and s > 0:
                queForNextSpace = True
            if self.text[s] == " " and queForNextSpace:
                messageText += "\n"
                queForNextSpace = False
        
        return messageText

def upload_blob(shouldUpload, bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"
    if shouldUpload:
        storage_client = storage.Client(project="hack-for-health24")
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        # Optional: set a generation-match precondition to avoid potential race conditions
        # and data corruptions. The request to upload is aborted if the object's
        # generation number does not match your precondition. For a destination
        # object that does not yet exist, set the if_generation_match precondition to 0.
        # If the destination object already exists in your bucket, set instead a
        # generation-match precondition using its generation number.
        generation_match_precondition = 0

        blob.upload_from_filename(source_file_name, if_generation_match=generation_match_precondition)

        print(
            f"File {source_file_name} uploaded to {destination_blob_name}."
        )

if __name__ == "__main__":
    c = chatpage()
    c.saveConversation()
    
    uploadedFileName = ""
    validUpload = False
    while(not validUpload):
        try:
            randID = random.randint(0, 99999)
            upload_blob(True, "cbt_data", "convos.txt", f"convo{randID}.txt")
            validUpload = True
        except Exception as e:
            pass
    
    shouldSend = input("Would you like to email this to your physician: (y/n) ")
    if (shouldSend == "y"):
        recipientEmail = input("What is your physicians email: ")
        #server = smtplib.SMTP('smtp.gmail.com', 587)
        #server.starttls()
        
        yag= yagmail.SMTP(user="raspistuart@gmail.com", password=EMAIL_KEY)
        #server.login("raspistuart@gmail.com", "khdx psoh ndbq wqwv")

        
        
        yag.send(
            to=recipientEmail,
            subject='Hack for Health 24',
            contents='Recent Conversation With Hack for Health Chatbot',
            attachments='convos.txt'
        )
