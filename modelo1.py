from llama_cpp import Llama
import re
import os
import time
import pyfiglet
from colorama import Fore, Style, init

# Inicializa colorama (Windows compatibility)
init()

# Cargar el modelo
llm = Llama(
    model_path="C:/Users/USUARIO/Desktop/unrestrictedchat/Mawdistical_Mawdistic-NightLife-24b-Q4_K_M.gguf",
    chat_format=None,
    verbose=False
)

# Función para extraer usernames, correos y teléfonos
def extraer_datos(texto):
    usernames = re.findall(r'@\w+', texto)
    correos = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', texto)
    telefonos = re.findall(r'\b(?:\+?\d{1,4})?[\s\-\.]?(?:\(?\d{2,4}\)?[\s\-\.]?){2,4}\d{2,4}\b', texto)

    return {
        "usernames": usernames,
        "correos": correos,
        "telefonos": telefonos
    } 

# Limpia la pantalla
os.system('cls' if os.name == 'nt' else 'clear')

# Crea y muestra el banner
banner = pyfiglet.figlet_format("SimulatorChat", font="slant")
banner_lines = banner.split("\n")
if len(banner_lines) > 5:
    banner_lines[5] += f"   {Style.DIM}uses AI{Style.RESET_ALL}"
print(Fore.RED + "\n".join(banner_lines) + Style.RESET_ALL)

# Mensaje de bienvenida
print("\nSimulatorChat initiated, at your own risk and responsibility of misuse.\n") 
time.sleep(1)

# Elegir rol del asistente
tokennumber= 30
rol = input("🧠 Define AI's rol (example: a women you just met on the club)\n> ")
system_prompt = f"Instructions for assistant, act like: {rol}. Be coherent with your rol at all times. Answers must have maximum {3*tokennumber} number of characters(letters)\n"

# Historial de conversación
chat_history = system_prompt

# Bucle de conversación
while True:
    user_input = input("👤 Client: ")

    # Construir el prompt completo
    prompt = chat_history + f"\nUsuario: {user_input}\nAsistente:"

    # Llamar al modelo
    response = llm(
        prompt,
        max_tokens=tokennumber,
        stop=["\nUsuario:", "\nAsistente:"]
    )

    reply = response["choices"][0]["text"].strip()
    
    # Extraer información del texto generado
    victim_info = extraer_datos(user_input) 

    # Mostrar respuesta e info extraída
    print(f"\n🤖 Character: {reply}")
    
    print("\n📥 Client info detectada:\n")
    print(f"   📧 Correos:   {victim_info['correos']}")
    print(f"   ☎️  Teléfonos: {victim_info['telefonos']}")
    print(f"   🧑 Usernames: {victim_info['usernames']}\n") 

    # Actualizar historial
    chat_history += f"\nUsuario: {user_input}\nAsistente: {reply}"
