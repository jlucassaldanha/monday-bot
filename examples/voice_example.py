from voice_reader import pySimpleVoiceRecognition

while True:
    print("::main while")
    while True:
        print("::voice while")
        # Read voice
        rec = pySimpleVoiceRecognition.rec()
        print("::rec")
        # Get response
        result = pySimpleVoiceRecognition.action()
    
        # Break loop
        if result == True:
            msg = "Make a clip"     
            break
