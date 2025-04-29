from vosk import Model, KaldiRecognizer
import pyaudio, json


class Transcrib():
    stream = None
    recognizer = None
    partial = {
        'partial': {
            'list': [0, []], 
            'str': ''
            }
        }
    text = {
        'text': {
            'list': [0, []], 
            'str': ''
            }
        }

    def __init__(self, model_path: str = r".\vosk_transcrib\vosk-model-small-pt-0.3"):
        """Inicia o modelo e o objeto de captura do microfone"""
        model = Model(model_path)
        self.recognizer = KaldiRecognizer(model, 16000)

        cap = pyaudio.PyAudio()
        self.stream = cap.open(
            input=True, 
            format=pyaudio.paInt16, 
            channels=1, 
            rate=16000, 
            frames_per_buffer=8192
            )
        self.stream.start_stream()

    def partial_listen(self) -> dict:
        data = self.stream.read(4096)

        if not self.recognizer.AcceptWaveform(data):
            json_data = json.loads(self.recognizer.PartialResult())
            words_list = str(json_data["partial"]).split()

            self.partial = {
                "partial": {
                    "list" : [len(words_list), words_list],
                    "str" : json_data["partial"]
                    }   
                }

            return self.partial
        else:
            self.recognizer.Reset()

    def result_listen(self) -> dict:
        data = self.stream.read(4096)

        if self.recognizer.AcceptWaveform(data):
            json_data = json.loads(self.recognizer.Result())
            words_list = str(json_data["text"]).split()

            self.text = {
                "text": {
                    "list" : [len(words_list), words_list],
                    "str" : json_data["text"]
                    }   
                }
            return self.text
            
    def listen(self):
        """Faz a leitura dos dados"""
        data = self.stream.read(4096)
        
        if self.recognizer.AcceptWaveform(data):
            json_data = json.loads(self.recognizer.Result())
            words_list = str(json_data["text"]).split()

            self.text = {
                "text": {
                    "list" : [len(words_list), words_list],
                    "str" : json_data["text"]
                    }   
                }
            
            return self.text
        else:
            json_data = json.loads(self.recognizer.PartialResult())
            words_list = str(json_data["partial"]).split()

            self.partial = {
                "partial": {
                    "list" : [len(words_list), words_list],
                    "str" : json_data["partial"]
                    }   
                }
            
            return self.partial
        
    def reset(self):
        self.recognizer.Reset()

    def partial_calling(self, name: str) -> bool:
        """verifica se foi chamado.
        name deve ser uma lista com as opções de nomes"""
        r = 0
        for n in name.split(" "):
            if n in self.partial:
                r += 1

        if r == len(name.split(" ")):
            return True
        else:
            return False
    
    def text_calling(self, name: str) -> bool:
        """verifica se foi chamado.
        name deve ser uma lista com as opções de nomes"""
        r = 0
        for n in name.split(" "):
            if n in self.text:
                r += 1

        if r == len(name.split(" ")):
            return True
        else:
            return False
        
    def partial_and_verify(self, words: list) -> bool:
        r = 0
        for w in words:
            if w in self.partial:
                r += 1

        if r == len(words):
            return True
        else:
            return False
        
    def result_and_verify(self, words: list) -> bool:
        r = 0
        for w in words:
            if w in self.text:
                r += 1

        if r == len(words):
            return True
        else:
            return False
        
    def partial_or_verify(self, words: list) -> bool:
        r = False
        for w in words:
            if w in self.partial:
                r = True
                break

        if r:
            return True
        else: 
            return False
        
    def result_or_verify(self, words: list) -> bool:
        r = False
        for w in words:
            if w in self.text:
                r = True
                break

        if r:
            return True
        else: 
            return False
    




if __name__ == "__main__":
    tc = Transcrib()
    ok = False

    while True:
        tc.listen_bigbrain()
        pd = tc.partial
        pt = tc.text
         
        print(pd)

        if not ok:
            if (
                "segunda" in pd["partial"]['list'][1] and
                "feira" in pd["partial"]['list'][1]
            ):
                print(pd["partial"]['str'])
                ok = True
                #break

        if ok:
            if (
                "faça" in pd["partial"]['list'][1] or
                "faz" in pd["partial"]['list'][1]
            ):
                if (
                    "clipe" in pd["partial"]['list'][1]
                ):
                    print(pd["partial"]['str'])
                    ok = True
                    break


                    
    #while True:
    #    tc.listen_bigbrain()
    #    pd = tc.partial
    #    pt = tc.text

    #    if (
    #        "segunda" in pd["partial"]['list'][1] and
    #        "feira" in pd["partial"]['list'][1]
    #    ):
    #        print(pd["partial"]['str'])
    #        ok = True
    #        break

    #print(ok)
    #while True:
    #    tc.listen_bigbrain()
    #    pd = tc.partial
    #    pt = tc.text

    #    if (
    #        "faça" in pd["partial"]['list'][1] or
    #        "faz" in pd["partial"]['list'][1]
    #    ):
    #        if (
    #            "clipe" in pd["partial"]['list'][1]
    #        ):
    #            print(pd["partial"]['str'])
    #            ok = True
    #            break



        #if (
        #    "segunda" in pt["text"]['list'][1] and
        #    "feira" in pt["text"]['list'][1]
        #):
        #    print(pt["text"]['str'])
        
