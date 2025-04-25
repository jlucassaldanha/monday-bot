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

    def listen(self, only_partial: bool = False, only_result: bool = False):
        """Faz a leitura dos dados"""
        data = self.stream.read(4096)

        if only_partial:
            # Real time
            if not self.recognizer.AcceptWaveform(data):
                json_data = json.loads(self.recognizer.PartialResult())
                words_list = str(json_data["partial"]).split()

                output = {
                    "partial": {
                        "list" : [len(words_list), words_list],
                        "str" : json_data["partial"]
                        }   
                    }
 
                return output
            else:
                self.recognizer.Reset()

        elif only_result:
            # post processing
            if self.recognizer.AcceptWaveform(data):
                json_data = json.loads(self.recognizer.Result())
                words_list = str(json_data["text"]).split()

                output = {
                    "text": {
                        "list" : [len(words_list), words_list],
                        "str" : json_data["text"]
                        }   
                    }
                return output
            
        else:
            # both
            if self.recognizer.AcceptWaveform(data):
                json_data = json.loads(self.recognizer.Result())
                words_list = str(json_data["text"]).split()

                output = {
                    "text": {
                        "list" : [len(words_list), words_list],
                        "str" : json_data["text"]
                        }   
                    }
                
                return output
            else:
                json_data = json.loads(self.recognizer.PartialResult())
                words_list = str(json_data["partial"]).split()

                output = {
                    "partial": {
                        "list" : [len(words_list), words_list],
                        "str" : json_data["partial"]
                        }   
                    }
                
                return output
            
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
        
    def reset(self):
        self.recognizer.Reset()


if __name__ == "__main__":
    tc = Transcrib()
    ok = False

    while True:
        tc.listen_bigbrain()
        pd = tc.partial
        pt = tc.text

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
        
