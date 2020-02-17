import string,random
import time
import speech_recognition as sr

def recognize_from_mic(recognizer,microphone):
    if not isinstance(recognizer,sr.Recognizer):
        raise TypeError("`recognizer` must be an instance of `Recognizer`")
    if not isinstance(microphone,sr.Microphone):
        raise TypeError("`microphone` must be ab instance of `Microphone`")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio=recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }
    try:
        response["transcription"]=recognizer.recognize_google(audio)
    except sr.RequestError:
        response["success"]=False
        response["error"]="API not available"
    except sr.UnknownValueError:
        response["error"]="Unable to recognize Speech"
    return response
    
words = 'cuffs cuing culls cults cumin cupel cupid curbs curds cures panel pangs panic pansy pants papas papal papaw paper parch pards pared pares paris parks parka parry parse parts parte party pasha salaam salads salami salary saline saliva sallow salmon salons saloon salted saluki salute salved salver salves salvia salvos samara sambas samoan sampan sample sancta sanded sander sandal sanest sanity sansei santas  scabby scaled scales scalar scalds scalps scamps scampi scants scanty scared scares bigamy bigger bights bigots bigwig bijoux bikers biking bikini bilged bilges bilked billed billet billow binary binder binges bingos biomes biopsy biotic biotas biotin bipeds birdie births bisect bishop bisque melodies melodeon meltable meltdown membrane mementos memories memorial memoriam memorize menacing menhaden meninges meniscal meniscus mentally menthols mentions mephitic mephitis merchant merciful mercuric meridian tenanting tendering tenderize tenements tenebrous tennessee tenseness tensility tentacles tentative tentmaker tenuously teriyakis termagant terminals terminate terracing terrapins terrarium terrazzos redeposits redescribe redesigned redevelops redigested redirected rediscover redissolve redistrict'
wordList=words.split()
def choose_word(wordList):
    return random.choice(wordList)

def is_guessed(secret_word,word_guessed):
    for c in secret_word:
        if(c in word_guessed)==False:
            return False

    return True

def get_letters(secret_word,letters_guessed):
    correct_guesses=[]
    guessed_word=""
    for c in letters_guessed:
        if(c in secret_word)==True:
            correct_guesses.append(c)

    for c in secret_word:
        if( c in correct_guesses):
            guessed_word+=c
        else:
            guessed_word+='_'
    return guessed_word
def get_available_letters(letters_guessed):
    letters=string.ascii_lowercase
    unguessed=""
    for c in letters:
        if (c in letters_guessed)==False:
            unguessed+=c
    return unguessed

def check_guesses(guesses_remaining,user_guess,duplicate_guesses,display):
    guesses_remaining-=1
    if not user_guess.isalpha():
        print("Oops! That is not a valid letter. You have no warnings left so you lose one guess. " + display)
    elif user_guess in duplicate_guesses: 
        print('Oops! You\'ve already guessed that letter. You have no warnings left so you lose one guess: ' + display)
    else:
        print('Oops! That letter is not in my word: ' + display)
    print('-----------------')
    return guesses_remaining
def check_warnings(warnings_remaining,user_guess,duplicate_guesses,display):
    warnings_remaining -= 1
    if not user_guess.isalpha(): 
        print('Oops! That is not a valid letter. You have ' + str(warnings_remaining) + ' warnings left: ' + display)
    elif user_guess in duplicate_guesses:
        print('Oops! You\'ve already guessed that letter. You have ' + str(warnings_remaining) + ' warnings left. ' + display)
    print('-----------------')
    return warnings_remaining

def hangman(secret_word):
    letters_guessed=[]
    duplicate_guesses=[]
    guesses_remaining=6
    warnings_remaining=3
    display = '_ ' * len(secret_word)
    unique_letters=''
    for c in secret_word:
        if(c in unique_letters)==False:
            unique_letters+=c
    
    print('Welcome to the game Hangman!')
    print("I'm thinking of a word that is " + str(len(secret_word)) + " letters long.")
    print('You have ' + str(warnings_remaining) + ' warnings left.')
    print('-----------------')
  
    while True: 
        letters_left = get_available_letters(letters_guessed)
        print('You have ' + str(guesses_remaining) + ' guesses left.')
        print('Available letters: ' + letters_left)
        recognizer=sr.Recognizer()
        microphone=sr.Microphone()
        prompt_limit=5
        for i in range(prompt_limit):
            print('Please guess a letter:')
            guess = recognize_from_mic(recognizer, microphone)
            if guess["transcription"]:
                    break
            if not guess["success"]:
                    break
            print("I didn't catch that. What did you say?\n")
        user_guess=guess["transcription"].lower()
        print("you guessed {}".format( user_guess))
        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
            break
        if not user_guess.isalpha:
            if warnings_remaining > 0:
                warnings_remaining = check_warnings(warnings_remaining, user_guess, duplicate_guesses, display)
            elif guesses_remaining > 1: 
                guesses_remaining = check_guesses(guesses_remaining, user_guess, duplicate_guesses, display)
            else: 
                print('Sorry, you ran out of guesses. The word was ' + secret_word + '.')
                break
        else:
            if user_guess not in letters_guessed:
                letters_guessed.append(user_guess)
            
            game_over = is_guessed(secret_word, letters_guessed)

            if game_over:
                display = get_letters(secret_word, letters_guessed)
                print('Good guess: ' + display)
                print('-----------------')
                print('Congratulations, you won!')
                total_score = guesses_remaining*len(unique_letters)
                print('Your total score for this game is: ' + str(total_score))
                break
            elif user_guess in duplicate_guesses:
                if warnings_remaining > 0: 
                    warnings_remaining = check_warnings(warnings_remaining, user_guess, duplicate_guesses, display)
                elif guesses_remaining > 1:
                    guesses_remaining = check_guesses(guesses_remaining, user_guess, duplicate_guesses, display)

            elif (not user_guess in duplicate_guesses)and user_guess in secret_word:
                 display = get_letters(secret_word, letters_guessed)
                 print('Good guess: ' + display)
                 print('-----------------')

            elif user_guess not in secret_word:
                if user_guess in ['a', 'e', 'i', 'o', 'u'] and guesses_remaining > 1:
                    guesses_remaining = guesses_remaining - 1
                    guesses_remaining = check_guesses(guesses_remaining, user_guess, duplicate_guesses, display)
                elif guesses_remaining > 1:
                    guesses_remaining = check_guesses(guesses_remaining, user_guess, duplicate_guesses, display)
                else:
                    print('Oops! That letter is not in my word: ' + display)
                    print('-----------------')
                    print('Sorry, you ran out of guesses. The word was ' + secret_word + '.')
                    break
            duplicate_guesses.append(user_guess)

secret_word = choose_word(wordList)

hangman(secret_word)