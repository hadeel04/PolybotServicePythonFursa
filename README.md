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
git clone https://github.com/your-username/image-processing-telegram-bot.git

2.Navigate to the project directory:

