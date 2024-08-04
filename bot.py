from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
import logging
import pandas as pd
import openai
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Verificar que las variables de entorno se hayan cargado correctamente
if TELEGRAM_TOKEN is None:
    raise ValueError("El token de Telegram no se ha encontrado. Asegúrate de que TELEGRAM_TOKEN está definido en el archivo .env.")
if OPENAI_API_KEY is None:
    raise ValueError("La clave de API de OpenAI no se ha encontrado. Asegúrate de que OPENAI_API_KEY está definido en el archivo .env.")

# Configura el logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Inicializa el Updater
updater = Updater(token=TELEGRAM_TOKEN, use_context=True)

# Obtén el dispatcher para registrar los manejadores
dispatcher = updater.dispatcher

# Configura la API de OpenAI
openai.api_key = OPENAI_API_KEY

# Función para obtener respuesta de GPT-3.5 con limitación a salud y nutrición
def get_gpt3_response(prompt, context):
    topic = context.user_data.get('topic', 'general')
    if topic == 'salud':
        system_content = "You are an assistant focused solely on health topics. Please respond only to questions related to health."
    elif topic == 'nutricion':
        system_content = "You are an assistant focused solely on nutrition topics. Please respond only to questions related to nutrition."
    else:
        system_content = "You are an assistant focused solely on health and nutrition. Please respond only to questions related to these topics."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300  # Aumentado para permitir respuestas más largas
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        logging.error(f"Error al llamar a la API de OpenAI: {e}")
        return "Lo siento, no puedo procesar tu solicitud en este momento."

# Función para generar una imagen con DALL-E
def generate_image(prompt):
    try:
        if len(prompt) > 1000:
            prompt = prompt[:997] + '...'  # Asegurar que el prompt no exceda los 1000 caracteres
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )
        return response['data'][0]['url']
    except Exception as e:
        logging.error(f"Error al generar la imagen con OpenAI: {e}")
        return None

# Función para manejar todos los mensajes y procesarlos
def handle_message(update, context):
    user = update.message.from_user
    text = update.message.text.lower()  # Convertir el texto a minúsculas para la comparación
    user_id = user.id
    logging.info(f"Mensaje recibido de {user.username} ({user_id}): {text}")

    if text in ['salir', 'reiniciar']:
        return restart(update, context)
    
    response = get_gpt3_response(text, context)
    context.bot.send_message(chat_id=update.effective_chat.id, text=response, parse_mode='HTML', reply_markup=reply_markup_with_restart())

    # Generar y enviar una imagen relacionada con la respuesta
    image_prompt = response[:1000]  # Truncar el prompt para la generación de la imagen si es necesario
    image_url = generate_image(image_prompt)
    if image_url:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_url, reply_markup=reply_markup_with_restart())

# Función para reiniciar la conversación
def restart(update, context):
    update.message.reply_text("El chat ha sido reiniciado.", reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()
    start(update, context)

def reply_markup_with_restart():
    return ReplyKeyboardMarkup([['Reiniciar']], resize_keyboard=True)

# Función para manejar las opciones iniciales de bienvenida
def handle_welcome_choice(update, context):
    query = update.callback_query
    query.answer()
    choice = query.data

    if choice == 'salud':
        context.user_data['topic'] = 'salud'
        query.edit_message_text(text="Has seleccionado Salud General. ¿Cuál es tu pregunta?")
    elif choice == 'nutricion':
        context.user_data['topic'] = 'nutricion'
        query.edit_message_text(text="Has seleccionado Nutrición. ¿Cuál es tu pregunta?")
    elif choice == 'pregunta_abierta':
        context.user_data['topic'] = 'general'
        query.edit_message_text(text="Has seleccionado Pregunta Abierta. ¿Cuál es tu pregunta?")

# Comando /start
def start(update, context):
    response = "Soy un chatbot de salud y nutrición. Selecciona un tema para comenzar."
    keyboard = [
        [InlineKeyboardButton("Salud General", callback_data='salud')],
        [InlineKeyboardButton("Nutrición", callback_data='nutricion')],
        [InlineKeyboardButton("Pregunta Abierta", callback_data='pregunta_abierta')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Enviar el logo
    logo_path = 'LogoChatBot.png'  # Asegúrate de que el archivo está en el mismo directorio que este script
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(logo_path, 'rb'))
    
    # Enviar el mensaje de bienvenida
    context.bot.send_message(chat_id=update.effective_chat.id, text=response, reply_markup=reply_markup_with_restart())
    context.bot.send_message(chat_id=update.effective_chat.id, text=response, reply_markup=reply_markup)

# Comando /help
def help(update, context):
    response = "Puedes hacer preguntas sobre salud general, nutrición o cualquier otro tema relacionado. Usa /start para comenzar de nuevo."
    context.bot.send_message(chat_id=update.effective_chat.id, text=response, reply_markup=reply_markup_with_restart())

# Comando /nutritional_info
def nutritional_info(update, context):
    food = ' '.join(context.args)
    if food:
        response = get_gpt3_response(f"Proporciona la información nutricional de {food}.", context)
        context.bot.send_message(chat_id=update.effective_chat.id, text=response, reply_markup=reply_markup_with_restart())
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Por favor, proporciona el nombre del alimento.", reply_markup=reply_markup_with_restart())

# Comando /log_meal
def log_meal(update, context):
    global users_data
    user_id = update.message.from_user.id
    meal = ' '.join(context.args)
    if meal:
        if user_id in users_data['user_id'].values:
            users_data.loc[users_data['user_id'] == user_id, 'meals'] += f', {meal}'
        else:
            users_data = users_data.append({'user_id': user_id, 'meals': meal}, ignore_index=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Comida registrada con éxito.", reply_markup=reply_markup_with_restart())
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Por favor, proporciona la comida que deseas registrar.", reply_markup=reply_markup_with_restart())

# Comando /diet_plan
def diet_plan(update, context):
    response = get_gpt3_response("Proporciona un plan de dieta personalizado basado en la información del usuario.", context)
    context.bot.send_message(chat_id=update.effective_chat.id, text=response, reply_markup=reply_markup_with_restart())

# Comando /tips
def tips(update, context):
    response = get_gpt3_response("Proporciona algunos consejos de salud y nutrición.", context)
    context.bot.send_message(chat_id=update.effective_chat.id, text=response, reply_markup=reply_markup_with_restart())

# Manejador de mensajes para registrar todas las peticiones
def log_message(update, context):
    user = update.message.from_user
    logging.info(f"Mensaje recibido de {user.username} ({user.id}): {update.message.text}")

# Registra los manejadores de comandos
start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help)
nutritional_info_handler = CommandHandler('nutritional_info', nutritional_info)
log_meal_handler = CommandHandler('log_meal', log_meal)
diet_plan_handler = CommandHandler('diet_plan', diet_plan)
tips_handler = CommandHandler('tips', tips)
restart_handler = CommandHandler('restart', restart)

# Manejador de respuestas y reinicio
dispatcher.add_handler(CallbackQueryHandler(handle_welcome_choice, pattern='^(salud|nutricion|pregunta_abierta)$'))
dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(nutritional_info_handler)
dispatcher.add_handler(log_meal_handler)
dispatcher.add_handler(diet_plan_handler)
dispatcher.add_handler(tips_handler)
dispatcher.add_handler(restart_handler)
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), handle_message))

# Inicia el bot
updater.start_polling()
updater.idle()
