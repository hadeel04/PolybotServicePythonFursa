# Image Processing Telegram Bot

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

This Telegram bot written in Python allows users to process images by applying various filters. It utilizes the `pyTelegramBotAPI` library for interacting with the Telegram Bot API and the `matplotlib` library for image processing.

## Features

- Welcome message for new users
- Supported filters:
  - Blur (with optional blur level)
  - Contour
  - Rotate
  - Segment
  - Salt and Pepper
  - Sepia
  - Concat (horizontally or vertically concatenate two images)
- Users can send an image along with a caption specifying the desired filter
- The processed image is sent back to the user

## Prerequisites

- Python 3.x
- flask
- maplotlib
- telebot
- loguru

## Installation

1. Clone the repository:

```bash
git clone https://github.com/hadeel04/PolybotServicePythonFursa
```

2.Navigate to the project directory:

```bash
cd PolybotServicePythonFursa
```

3.Install the required dependencies:

```bash
pip install -r requirements.txt
```
## Configuration

1. <a href="https://desktop.telegram.org/" target="_blank">Download</a> and install Telegram Desktop (you can use your phone app as well).
2.  Once installed, create your own Telegram Bot by following <a href="https://core.telegram.org/bots/features#botfather">this section</a> to create a bot. Once you have your telegram token you can move to the next step.
3.  Set the environment variable `TELEGRAM_TOKEN` with your telegram bot token
   
```bash
export TELEGRAM_TOKEN=your_telegram_bot_token_here
```
4. Sign-up for the Ngrok service
5. then install the `ngrok` agent as [described here](https://ngrok.com/docs/getting-started/#step-2-install-the-ngrok-agent)
6. Authenticate your ngrok agent:

```bash
ngrok config add-authtoken <your-authtoken>
```
7. start ngrok by running the following command:

```bash
ngrok http 8443
```
8. set the `TELEGRAM_APP_URL` env var to your URL ,Your bot public URL is the URL specified in the `Forwarding` line (e.g. `https://16ae-2a06-c701-4501-3a00-ecce-30e9-3e61-3069.ngrok-free.app`):
   
```bash
export TELEGRAM_APP_URL=your_telegram_url_here
```
## Usage

1. Run the app.py file to start the Flask server and the Telegram bot:
     
```bash
python app.py
```
2. Send an image to the Telegram bot, along with a caption specifying the desired filter.
3. The bot will process the image and send back the filtered image.
