import speech_recognition as sr
#from gtts import gTTS
from random import randint
#from playsound import playsound
import os

class pySimpleVoiceRecognition():
    audio_data = ""

    @classmethod
    def rec(self) -> str:
        """
        Read and recognize audio from mic
        """
        # Init recognizer
        recognizer = sr.Recognizer()
        listened = False
        # Open mic

        print("Listening...")
        with sr.Microphone() as mic:
            # Listen mic audio
            while not listened:
                try:
                    rec = recognizer.listen(mic, 10, 10)
                    listened = True
                
                except sr.WaitTimeoutError:
                    listened = False
            print("Processing...")

            # Try to recognize the audio, in case of error, 
            # reset variable value and pass
            try:
                audio_data = recognizer.recognize_google(rec, language='pt')

            except sr.UnknownValueError:
                audio_data = ""
                print(">> Can't understand\n")
                pass

            except sr.RequestError:
                audio_data = ""
                print(">> Server down\n")

            self.audio_data = audio_data.lower()

            print(">>", self.audio_data)

            return self.audio_data # return value
    
    @classmethod
    def response(self, msg: str) -> None: #### SEM USO ####
        """
        Create a audio with the message and reproduces it
        """
        # Save path till working directory
        abspath = os.path.abspath(os.getcwd())
        num = randint(1, 20000) # Get random number
        # Create a name to the audio file
        audio_file_name = ".\\10 - logica final\\client\\audio\\" + str(num) + ".mp3"
        
        # Create audio file
        #text_to_speech = gTTS(msg, lang='en')
       # text_to_speech.save(audio_file_name)

        # Reproduces audio file
        # playsound(audio_file_name)
        # Remove audio file
        os.remove(audio_file_name)

        print("<<", msg)

    @classmethod
    def exist(self, terms:list) -> bool:
        """
        Verify the existence of a term in the list
        """
        for term in terms:
            if term in self.audio_data:
                return True

    @classmethod
    def only_exist(self, term:str) -> bool:
        """
        Verify the existence of a term in the list
        """   
        if term.lower() == self.audio_data.lower():
            return True
            
    @classmethod
    def assitent_call(self) -> bool:
        """
        Verify for assistent call.
        """
        if self.only_exist("lucas"):
            print("::Call Accepted")
            return True
        
        else:
            return False

    @classmethod      
    def action(self) -> bool:
        """
        Verify the audio recognized and return true in case of understand
        """
        if self.exist(terms=["clipe", "clip"]):# and self.exist(terms=["lucas"]):
            print(">> Ok, making clip\n")
            #self.response("Ok, making a clip")

            return True
        
        if self.exist(terms=["clipe", "clip"]):# and not self.exist(terms=["lucas"]):
            print(">> Sorry, I don't understand what you said\n")
            #self.response("Sorry, I don't understand what you said")

            return False
        
        if not self.exist(["clipe", "clip"]):# and self.exist(["lucas"]):
            print(">> Sorry, I don't understand what you said\n")
            #self.response("Sorry, I don't understand what you said")
            
            return False

if __name__ == "__main__":      
    while True:
        # Read voice
        rec = pySimpleVoiceRecognition.rec()

        # Get response
        result = pySimpleVoiceRecognition.action()

        print(result)
        # Break loop
        if result == True:
            break        
    