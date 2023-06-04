import threading, queue, speech_recognition, pyttsx3, time, psutil,pygame, features
from os import path
from datetime import datetime

screen_title = 'Virtual Assistant'
screen_icon = 'icon.png'
screen_width = 800
screen_height = 600
screen_running = True


def speak(speak_text, engine, glow, text):
    def onWord(name, location, length):
        current_word = speak_text[location : location + length]
        prev_text = ""
        try:
            if (not text.empty()):
                new_text = text.get()
                if (new_text != prev_text):
                    prev_text = new_text
        except Exception as e:
            prev_text = ""

        if(not prev_text == current_word):
            text.put_nowait(current_word)

        if not screen_running:
            engine.stop()
            return
        
    if not screen_running:
        features.system_exit()

    glow.set()
    features.get_print_cyan("Virtual Assistant : " + speak_text)

    engine.connect('started-word', onWord)
    engine.say(speak_text)
    engine.runAndWait()

    text.put_nowait('')
    glow.clear()


def gui_program(glow, text):
    global screen_running

    pygame.init()
    pygame.display.init()
    
    pygame.display.set_caption(screen_title)
    pygame.display.set_icon(pygame.image.load(screen_icon))
    
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.WINDOWMAXIMIZED)
    screen.fill((5, 2, 23))

    handler = features.PygameImageHandler()
    font = pygame.font.Font('freesansbold.ttf', 24)

    for i in range(40):
        handler.loadFromFile(path.join(path.dirname(
            __file__), 'images\enabled\img ({}).jpg'.format(i + 1)), 'enabled-{}'.format(i + 1))
    for i in range(40):
        handler.loadFromFile(path.join(path.dirname(
            __file__), 'images\disabled\img ({}).jpg'.format(i + 1)), 'disabled-{}'.format(i + 1))

    i = 0
    current_text = ""
    while True:
        if (i == 40):i = 1
        else:i += 1

        time.sleep(0.035)
        if glow.is_set():
            handler.render(screen, 'enabled-{}'.format(i), (0, 0),
                           True, (screen_width, screen_height))
        else:
            handler.render(screen, 'disabled-{}'.format(i),
                           (0, 0), True, (screen_width, screen_height))

        try:
            if (not text.empty()):
                new_text = text.get()
                if (new_text != current_text):
                    current_text = new_text
        except Exception as e:
            current_text = ""

        # Top left Text
        left1_display = font.render(
            "Current Time  : " + datetime.now().strftime('%H:%M:%S').upper(), True, (217, 224, 255))
        screen.blit(left1_display, (screen_width // 16, screen_height // 14))

        left2_display = font.render(
            "Current Time  : " + datetime.today().strftime('%d-%m-%Y'), True, (217, 224, 255))
        screen.blit(left2_display, (screen_width // 16, screen_height // 8))

        # Top Right Text
        right_display = font.render(
            "Memory Usage : " + str(psutil.virtual_memory().percent) + "%", True, (217, 224, 255))
        screen.blit(right_display, right_display.get_rect(
            center=(screen_width - (screen_width // 4), screen_height // 11)))
        
        # Bottom Text
        if (current_text != ""):
            text_display = font.render(
                current_text.upper(), True, (217, 224, 255))
            screen.blit(text_display, text_display.get_rect(
                center=(screen_width // 2, screen_height - (screen_height // 10))))

        pygame.display.update(0, 0, screen_width, screen_height)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or not screen_running:
                screen_running = False
                pygame.quit()
                features.system_exit()


def recognizer_program(glow, text):
    global screen_running

    text.put_nowait('Wait a while, getting things ready')

    recognizer = speech_recognition.Recognizer()
    recognizer.pause_threshold = 0.8

    microphone = speech_recognition.Microphone()
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 200)

    first_speak = False
    while screen_running:
        
        with microphone as source:
            if(first_speak == False):
                speak(f"{features.get_wish()} sir, I am your virtual ai assistant. ready for command", engine,  glow, text)
                first_speak=True
            features.get_print_light_purple("Listening...")
            text.put_nowait('Listening...')
            audio = recognizer.listen(source)

        # Enter Command From Terminal 
        # listen_text = input("Enter Command : ").lower()

        try:
            listen_text = recognizer.recognize_google(audio).lower()
            
            if(listen_text):
                features.get_print_purple("You : " + listen_text)
                reply_text = "sorry sir i did not find any perfect response."

                if "hello" in listen_text:
                    reply_text = "hello sir, how may i help you"

                elif "hi" in listen_text:
                    reply_text = "Hi Sir, how are you ?"

                elif "help" in listen_text:
                    reply_text = "Sir please notics the command panel at the right side of this window"

                elif "your name" in listen_text:
                    reply_text = "You can call my anything sir, but i will like more if you call me only virtual assistant"

                elif "how are you" in listen_text:
                    reply_text = "i am fine sir, what about you"

                elif "who are you" in listen_text  or "what about you" in listen_text:
                    reply_text = "i am a virtual ai assistant developed with python programming language. I am made for making things easy for humans."

                elif "fine" == listen_text:
                    reply_text = "glad to hear that sir"

                elif "date" in listen_text:
                    reply_text = features.get_date()

                elif "time" in listen_text:
                    reply_text = features.get_time()

                elif "joke" in listen_text:
                    reply_text = features.get_joke()

                elif "screenshot" in listen_text or "capture the screen" in listen_text:
                    reply_text = features.take_screenshot()

                elif "where i am" in listen_text or "current location" in listen_text or "where am i" in listen_text:
                    city, state, country = features.get_my_location()
                    reply_text = f"You are currently in {city} city which is in {state} state and country {country}"

                elif "goodbye" in listen_text or "offline" in listen_text or "bye" in listen_text or "stop" in listen_text:
                    screen_running = False

                elif "ip address" in listen_text or "ip" in listen_text:
                    reply_text = features.get_my_ip()

                elif "system" in listen_text or "system_info" in listen_text:
                    reply_text = features.get_system_stats()

                elif 'search google for' in listen_text:
                    reply_text = features.get_google_search(listen_text)

                elif 'tell me about' in listen_text:
                    topic = listen_text.split('tell me about')[1]
                    if topic:
                        reply_text = features.get_wiki_response(topic)
                    else:
                        reply_text = "sorry sir. I couldn't load your query from my database."

                elif 'launch' in listen_text:
                    app_dictionary = {
                        'chrome': 'C:/Program Files/Google/Chrome/Application/chrome'
                    }
                    app = listen_text.split(' ', 1)[1]
                    path = app_dictionary.get(app)
                    if path is None:
                        reply_text = 'application path not found'
                    else:
                        features.launch_any_app(path_of_app=path)
                        reply_text = 'launching ' + app + 'for you sir!'

                elif 'weather' in listen_text:
                    reply_text = features.get_weather(city=listen_text.split(' ')[-1])

                elif "buzzing" in listen_text or "news" in listen_text or "headlines" in listen_text:
                    news_res = features.get_news()
                    res = 'Source: The Times Of India. Todays Headlines are. '
                    for index, articles in enumerate(news_res):
                        res = res + articles['title']
                        if index == len(news_res)-2:
                            break
                    reply_text = res

                elif "where is" in listen_text:
                    place = listen_text.split('where is ', 1)[1]
                    current_loc, target_loc, distance = features.get_location(place)
                    city = target_loc.get('city', '')
                    state = target_loc.get('state', '')
                    country = target_loc.get('country', '')
                    if city:
                        reply_text = f"{place} is in {state} state and country {country}. It is {distance} km away from your current location"
                    else:
                        reply_text = f"{state} is a state in {country}. It is {distance} km away from your current location"

                if (reply_text):
                    speak(reply_text, engine, glow, text)
        except:
            if(not screen_running):
                features.get_print_red("error : either could not recognize your speech or something went wrong")


def main_program():
    glow = threading.Event()
    text = queue.Queue()

    recognizer_thread = threading.Thread(target=recognizer_program, args=(glow, text))
    gui_thread = threading.Thread(target=gui_program,daemon=True, args=(glow, text))

    recognizer_thread.start()
    gui_thread.start()

    recognizer_thread.join()
    gui_thread.join()

    features.system_exit()


if __name__ == "__main__":
    main_program()
