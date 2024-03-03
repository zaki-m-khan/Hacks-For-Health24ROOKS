# Personal Mental Health Assistant

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Contributors](#contributors)

## Introduction
The Personal Mental Health Assistant is an innovative chatbot developed during the "Hacks for Health" hackathon at Lehigh University, sponsored by Google Cloud. Created by Morgan Stuart, Jared Cooper, Mithat Eroglu, and Zaki Khan, this chatbot is designed to support individuals in managing their mental health. It uses a combination of Cognitive Behavioral Therapy (CBT) exercises and personalized conversation flows to provide a tailored support experience. The chatbot offers various functionalities, including breathing exercises, calming sounds, and a game, to help users based on their feelings and needs.

## Installation
To set up the Personal Mental Health Assistant, follow these steps:
1. Clone the project repository from GitHub.
2. Ensure you have Python installed on your system.
3. Install the required dependencies using pip:
4. Set up Google Cloud Services, including Google Cloud Storage and Google's Gemini, as per the project's dependency requirements.

## Usage
To use the chatbot:
1. Run the chatbot script from your terminal or command prompt.
2. Follow the on-screen prompts to interact with the chatbot.
3. Optionally, at the end of the conversation, you can choose to send the conversation transcript to a therapist by providing their email address.

## Features
- **Personalized Conversation Flow:** Tailors the chat experience based on user inputs and selected CBT exercises.
- **Breathing Exercises:** Guides users through breathing exercises to help manage acute stress or anxiety.
- **Calming Sounds:** Offers a selection of calming sounds to aid in relaxation.
- **Therapist Email Integration:** Allows users to send a transcript of their conversation to their therapist for further discussion.

## Dependencies
- Google Cloud Storage
- Google's Gemini for intelligent conversation flow
- Other Python libraries as specified in the `requirements.txt` file

## Configuration
To configure the chatbot for use:
1. Create an Application Default Credential (ADC) for Google Cloud Services.
2. Connect the ADC to a Google Cloud Storage bucket created for storing conversation transcripts.
3. Configure the email functionality to enable sending conversations to therapists.

## Contributors
- Morgan Stuart
- Jared Cooper
- Mithat Eroglu
- Zaki Khan

