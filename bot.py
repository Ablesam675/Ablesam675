import os
from telegram.ext import Updater, CommandHandler
from huggingface_hub import InferenceClient
from PIL import Image
from io import BytesIO

# Function to generate an image using Hugging Face
def generate_image(update, context):
    try:
        # Extract the prompt from the user's message
        prompt = " ".join(context.args)
        if not prompt:
            update.message.reply_text("Please provide a description for the image. Example: /generate Astronaut riding a horse")
            return

        # Hugging Face client
        token = "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"
        client = InferenceClient(model="stabilityai/stable-diffusion-3.5-large-turbo", token=token)

        # Generate the image
        update.message.reply_text("Generating your image, please wait...")
        image = client.text_to_image(prompt)

        # Save the image to a buffer
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)

        # Send the image to the user
        update.message.reply_photo(photo=buffer, caption=f"Here is your image for: '{prompt}'")

    except Exception as e:
        update.message.reply_text(f"An error occurred: {str(e)}")

# Function to handle the /start command
def start(update, context):
    update.message.reply_text("Welcome to the AI Image Generator Bot! Use /generate <description> to create an image.")

def main():
    # Telegram bot token
    tg_token = "8007890518:AAG0G_HYOTYfZcUQAMIdnWXbKHFWmHniN6Y"

    # Set up the bot
    updater = Updater(tg_token, use_context=True)
    dp = updater.dispatcher

    # Add command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("generate", generate_image))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
