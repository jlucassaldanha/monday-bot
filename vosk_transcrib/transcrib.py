from vosk import Model, KaldiRecognizer
import pyaudio, json


class Transcrib():
    stream = None
    recognizer = None
    partial = {}
    text = {}
    result = []
    partial_result = False

    def __init__(self, model_path: str = r".\vosk_transcrib\vosk-model-small-pt-0.3", partial_result: bool = False):
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

        self.partial_result = partial_result
            
    def listen_bigbrain(self):
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
        
    def listen(self) -> dict:
        data = self.stream.read(4096)

        if self.partial_result:
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
        else:
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
        
    def and_verify(self, words: list) -> bool:
        if self.partial_result:
            self.result = self.partial["partial"]['list'][1]
        else:
            self.result = self.text["text"]['list'][1]

        r = 0
        for w in words:
            if w in self.result:
                r += 1

        self.recognizer.Reset()

        if r == len(words):
            return True
        else:
            return False
        
    def or_verify(self, words: list) -> bool:
        if self.partial_result:
            self.result = self.partial["partial"]['list'][1]
        else:
            self.result = self.text["text"]['list'][1]

        r = False
        for w in words:
            if w in self.result:
                r = True
                break

        self.recognizer.Reset()

        if r:
            return True
        else: 
            return False
        
    def calling(self, name: str) -> bool:
        """verifica se foi chamado.
        name deve ser uma lista com as opções de nomes"""
        words = name.split()

        return self.and_verify(words)
        
    def reset(self):
        self.recognizer.Reset()
    


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
        
