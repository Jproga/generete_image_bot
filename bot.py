import telebot
from config import TOKEN
from logic import Text2ImageAPI
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот генерирующий картинки. Последовательность написания сообщения боту: текст, размер x y через пробел")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Создайте экземпляр Text2ImageAPI
        api = Text2ImageAPI('https://api-key.fusionbrain.ai/', 'Api_token', 'secret_token')


        text = message.text.split()
        width = int(text[-2])
        height = int(text[-1])
        
        # Сгенерируйте изображение
        api.text_to_image(message.text, api.get_model(), 'landscape.png', width=width, height=height)

        # Отправьте изображение пользователю
        with open('landscape.png', 'rb') as image_file:
            bot.send_photo(message.chat.id, image_file)

    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "Произошла ошибка. Пожалуйста, попробуйте снова.")
      
if __name__ == "__main__":
    bot.polling(none_stop=True)
