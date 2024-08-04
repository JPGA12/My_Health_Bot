# My Health Bot

**My Health Bot** es un asistente personal para todo lo relacionado con la salud y la nutrición. Este chatbot está diseñado para proporcionar información precisa y útil sobre una variedad de temas de salud y nutrición, ayudándote a tomar decisiones informadas para mejorar tu bienestar general.

## Características

- **Información Nutricional:** Obtén detalles sobre el valor nutricional de diferentes alimentos.
- **Planes de Dieta Personalizados:** Recibe recomendaciones de dietas basadas en tus necesidades y objetivos personales.
- **Registro de Comidas:** Lleva un registro de tus comidas diarias para un seguimiento más fácil de tu nutrición.
- **Consejos de Salud:** Accede a consejos útiles y prácticas saludables para mejorar tu estilo de vida.
- **Ejercicios y Rutinas:** Descubre ejercicios efectivos para mantenerte en forma y saludable.

## Cómo empezar

1. **Salud General:** Selecciona esta opción para obtener información y consejos sobre temas de salud en general.
2. **Nutrición:** Elige esta opción para recibir información sobre nutrición y dietas.
3. **Pregunta Abierta:** Si tienes alguna pregunta específica, selecciona esta opción y escribe tu consulta.

Para reiniciar la conversación en cualquier momento, simplemente escribe "reiniciar" o "salir". Nuestro chatbot está aquí para ayudarte a alcanzar tus objetivos de salud y nutrición con respuestas personalizadas y relevantes.

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/JPGA12/My_Health_Bot.git
   cd My_Health_Bot
2. Crea y activa un entorno virtual:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  
    # En Windows usa 
    .venv\Scripts\activate
3. Instala las dependencias:
    ```bash
    Copiar código
    pip install -r requirements.txt
4. Crea un archivo .env en el directorio raíz del proyecto con el siguiente contenido, asegurándote de reemplazar las variables con tus propias claves:
    ```bash 
    TELEGRAM_TOKEN=tu-telegram-token
    OPENAI_API_KEY=tu-openai-apikey
5. Ejecuta el Bot
    ```bash
    python bot.py
## Uso
- /start: Inicia la conversación con el bot y muestra el menú principal.
- /help: Muestra una lista de comandos disponibles y su descripción.
- /nutritional_info [alimento]: Proporciona la información nutricional del alimento especificado.
- /log_meal [comida]: Registra una comida.
- /diet_plan: Proporciona un plan de dieta personalizado.
- /tips: Proporciona consejos de salud y nutrición.
- salir o reiniciar: Reinicia la conversación.
## Contribuir
Si deseas contribuir a este proyecto, por favor sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (git checkout -b feature/nueva-funcionalidad).
3. Realiza tus cambios y haz commit (git commit -m 'Añadir nueva funcionalidad').
4. Sube tus cambios a la rama (git push origin feature/nueva-funcionalidad).
5. Abre un Pull Request.
## Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.
## Contacto
Si tienes alguna pregunta o sugerencia, no dudes en abrir un issue o contactar al autor del proyecto.