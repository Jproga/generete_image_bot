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


        # Разделите сообщение по запятой
        parts = message.text.split(',')
        prompt = parts[0].strip()  # Текст запроса до первой запятой
        size = parts[1].strip().split()  # Размер изображения (x, y)
        width = int(size[0])
        height = int(size[1])

        # Проверка длины запроса
        if len(prompt.split()) > 10:
            bot.reply_to(message, "Запрос слишком длинный. Используйте не более 10 слов.")
            return

        generating_message = bot.send_message(message.chat.id, "Генерирую изображение...")
        
        # Сгенерируйте изображение
        api.text_to_image(message.text, api.get_model(), 'landscape.png', width=width, height=height)

        # Удалите сообщение о генерации
        bot.delete_message(message.chat.id, generating_message.message_id)

        # Отправьте изображение пользователю
        with open('landscape.png', 'rb') as image_file:
            bot.send_photo(message.chat.id, image_file)

    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "Произошла ошибка. Пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    bot.polling(none_stop=True)
