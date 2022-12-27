import logging
import speech_recognition as sr

def stt(file_path):
    data = {}
    data["text"] = ""
    data["error"] = ""
    recog= sr.Recognizer()
    #recognize the wav file as bangla
    with sr.AudioFile(file_path) as source:
        audiofile=recog.listen(source)
        try:
            text=recog.recognize_google(audiofile, language='bn-BD')
            data["text"] =  text

        except sr.UnknownValueError:
            data["error"] = "unknown_value"

        except sr.RequestError as e:
            logging.error(f"Could not request results from Google Speech Recognition service; {0}".format(e))
            data["error"] = "connection_error"
        
        return data