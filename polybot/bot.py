import telebot
from loguru import logger
import os
import time
from telebot.types import InputFile
from polybot.img_proc import Img


class Bot:

    def __init__(self, token, telegram_chat_url):
        # create a new instance of the TeleBot class.
        # all communication with Telegram servers are done using self.telegram_bot_client
        self.telegram_bot_client = telebot.TeleBot(token)

        # remove any existing webhooks configured in Telegram servers
        self.telegram_bot_client.remove_webhook()
        time.sleep(0.5)

        # set the webhook URL
        self.telegram_bot_client.set_webhook(url=f'{telegram_chat_url}/{token}/', timeout=60)

        logger.info(f'Telegram Bot information\n\n{self.telegram_bot_client.get_me()}')

    def send_text(self, chat_id, text):
        self.telegram_bot_client.send_message(chat_id, text)

    def send_text_with_quote(self, chat_id, text, quoted_msg_id):
        self.telegram_bot_client.send_message(chat_id, text, reply_to_message_id=quoted_msg_id)

    def is_current_msg_photo(self, msg):
        return 'photo' in msg

    def download_user_photo(self, msg):
        """
        Downloads the photos that sent to the Bot to `photos` directory (should be existed)
        :return:
        """
        if not self.is_current_msg_photo(msg):
            raise RuntimeError(f'Message content of type \'photo\' expected')

        file_info = self.telegram_bot_client.get_file(msg['photo'][-1]['file_id'])
        data = self.telegram_bot_client.download_file(file_info.file_path)
        folder_name = file_info.file_path.split('/')[0]

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        with open(file_info.file_path, 'wb') as photo:
            photo.write(data)

        return file_info.file_path

    def send_photo(self, chat_id, img_path):
        if not os.path.exists(img_path):
            raise RuntimeError("Image path doesn't exist")

        self.telegram_bot_client.send_photo(
            chat_id,
            InputFile(img_path)
        )

    def handle_message(self, msg):
        """Bot Main message handler"""
        logger.info(f'Incoming message: {msg}')
        self.send_text(msg['chat']['id'], f'Your original message: {msg["text"]}')


class QuoteBot(Bot):
    def handle_message(self, msg):
        logger.info(f'Incoming message: {msg}')

        if msg["text"] != 'Please don\'t quote me':
            self.send_text_with_quote(msg['chat']['id'], msg["text"], quoted_msg_id=msg["message_id"])


class ImageProcessingBot(Bot):

    #the function check the name of the filter and the arguments
    # and process the image according to the filter
    def process_image(self, img_path, caption):
        caption_parts = caption.split()
        caption = caption_parts[0]
        filter_args = caption_parts[1:]
        my_img = Img(img_path)
        if (caption == 'Contour'):
            my_img.contour()
        if (caption == 'Blur'):
            blur_level = int(filter_args[0]) if filter_args else 16
            my_img.blur(blur_level)
        if (caption == 'Rotate'):
            my_img.rotate()
        if (caption == 'Segment'):
            my_img.segment()
        if (caption == 'Salt and pepper'):
            my_img.salt_n_pepper()

        #it wasnt obvoiuse how we will get the two photos also ownload_user_photo fun can
        #handle only one photo if i get it wright
        if (caption == 'Concat'):
            direction = filter_args[0] if filter_args else 'horizontal'
            my_img.concat(my_img, direction)

        if (caption == 'Sepia'):
            my_img.sepia()

        return my_img.save_img()

    #sending a welcome message for the user
    def greet_user(self, chat_id, first_name):
        self.send_text(chat_id, f"Welcome {first_name}! I'm ready to process your images.")

    #check if the user privide an image and caption and implement the filter on the picture
    def handle_message(self, msg):
        logger.info(f'Incoming message: {msg}')
        chat_id = msg['chat']['id']
        first_name = msg['chat']['first_name']

        if 'text' in msg:
            self.greet_user(chat_id, first_name)

        if self.is_current_msg_photo(msg):
            try:
                img_path = self.download_user_photo(msg)
                caption = msg['caption'] if 'caption' in msg else None

                if not caption:
                    self.send_text(chat_id,
                                   "Please provide a caption with one of the following filters: 'Blur', 'Contour', 'Rotate', 'Segment', 'Salt and pepper', 'Concat', 'Sepia'")
                    return
                processed_img_path = self.process_image(img_path, caption)
                self.send_photo(chat_id, processed_img_path)
            except Exception as e:
                logger.error(f"Error processing image: {e}")
                self.send_text(chat_id, "Something went wrong while processing the image. Please try again later.")
        else:
            self.send_text(chat_id, "Please send a photo to process.")
