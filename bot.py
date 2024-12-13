import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, CallbackContext
from huggingface_hub import InferenceClient

# Set up Flask
app = Flask(__name__)

# Telegram Bot token and Hugging Face token
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')  # Set this in your environment variables
HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACE_TOKEN')  # Set this in your environment variables

# Hugging Face client
hf_client = InferenceClient("stabilityai/stable-diffusion-3.5-large-turbo", token=HUGGINGFACE_TOKEN)

# Telegram bot setup
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dispatcher = Dispatcher(bot, update_queue=None, workers=0)

# Start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello! Send me a prompt, and I'll generate an image for you using AI.")

# Generate image command
def generate_image(update: Update, context: CallbackContext) -> None:
    if not context.args:
        update.message.reply_text("Please provide a prompt. For example: /generate A sunset over a mountain.")
        return

    prompt = " ".join(context.args)
    update.message.reply_text(f"Generating image for: {prompt}...")

    try:
        # Call Hugging Face API to generate an image
        image = hf_client.text_to_image(prompt)
        # Save image to a temporary file
        temp_file = "output.png"
        image.save(temp_file)

        # Send image back to the user
        with open(temp_file, "rb") as img:
            update.message.reply_photo(photo=img, caption=f"Here is your AI-generated image for: {prompt}")
    except Exception as e:
        update.message.reply_text(f"Failed to generate image: {e}")

# Add handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("generate", generate_image))

# Webhook route
@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

if __name__ == "__main__":
    app.run(debug=True)