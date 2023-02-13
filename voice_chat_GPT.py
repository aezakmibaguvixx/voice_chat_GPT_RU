import dotenv
import speech_recognition as sr
import time
import threading
import pyttsx3
import os
import openai
from dotenv import load_dotenv
dotenv.load_dotenv('.env')
openai.api_key = os.getenv('API_KEY')

# Две глобальные переменные ,Ireply используется для
# отслеживания состояния ответа от AI, а final_msg содержит итоговое сообщение,
# которое будет выдано AI. В данном случае, они инициализируются как
# False и пустая строка соответственно.
global AIreply, final_msg
AIreply = False
final_msg = ''

# 3
engine = pyttsx3.init() # Инициализирует модуль pyttsx3 для синтеза речи
voices = engine.getProperty('voices')      # Получает список доступных голосов
engine.setProperty('voice', 'ru')  # Устанавливает голос из списка голосов
rate = engine.getProperty('rate')          # Получает текущую скорость речи
engine.setProperty('rate', 200)             # Устанавливает скорость речи на 160


# 2- set the aikey and sending request to chat gpt
def generate_response(prompt):                # Функция используетсяч для оздания ответа AI
                                              # на полученный запрос (prompt).
    global AIreply, final_msg                 # объявляются две глобальные переменные
    comletions = openai.Completion.create(    # метод для создания ответа AI на основе полученного
                                              # запроса (prompt). Параметры, которые передаются
                                              # в этот метод:
        engine = 'text-davinci-003',          # модель AI, которая будет использоваться для создания ответа.
        prompt = prompt,                      # текст запроса
        max_tokens = 1024,                    # максимальное количество токенов в ответе.
        n = 1,                                # количество ответов, которые нужно создать.
        stop = None,                          # список токенов, которые означают конец ответа
        temperature = 0.5,                    # параметр, который определяет степень случайности в ответе AI

    )
    message = comletions.choices[0].text      # выбираем ответ AI с индексом 0  и сохраняем в переменную
    final_msg = message.strip()               # стрип для удаления лишних пробелов или символов
    AIreply = True                            # true  означает что был получет ответ от AI

def chatprinter(chat):                        # Функция печатает посимвольно с задеркой
    for word in chat:                         # цикл по каждому символу
        time.sleep(0.055)                     # задержка
        print(word, end = '', flush = True)   # end= для того чтобы не начиналась новая строкка после каждого символа
                                              # флуш чтобы вывод был немедленный
    print()



    #Этот код создает систему распознавания голоса используя библиотеку
    # SpeechRecognition (sr). Он использует микрофон для записи звуковых данных,
    # а затем пытается распознать речь с помощью Google Speech Recognition.
    # Когда текст был успешно распознан, он передается функции generate_response()
    # для генерации ответа. Функция chatprinter() используется для вывода ответа,
    # а затем он произносится с помощью библиотеки pyttsx3 (engine).
    # Если не удается распознать речь, выводится сообщение "Sorry, your voice-error".
    # Если слово "стоп" встречается в распознанном тексте, выполнение цикла прекращается и программа завершается.

r = sr.Recognizer()
with sr.Microphone() as source:
    print('---------------GPT ГОТОВ УСЛЫШАТЬ ТЕБЯ---------------')
    while True:
        print('Me:', end = ' ', flush = True)
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language='ru-RU', show_all=True)
            Textresult = text['alternative'][0]['transcript']
            if 'стоп' in Textresult:
                print('Ending GPT communication')
                break
            t1 = threading.Thread(target = generate_response,args = (Textresult,))
            t1.start()

            chatprinter(Textresult)

            while AIreply == False:
                pass
            AIreply = False

            print('Chat GPT: ', end = '')
            t2 = threading.Thread(target = chatprinter,args = (final_msg,))
            t2.start()

            #start reading the text recived from GPT
            engine.setProperty('voice', 'ru')
            engine.say(final_msg)
            engine.runAndWait()
            print('---------------------')
        except:
            print('Sorry, your voice-error')