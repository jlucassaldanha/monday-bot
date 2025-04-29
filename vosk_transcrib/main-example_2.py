import time
from transcrib import Transcrib

tc = Transcrib(partial_result=True)
msg = ""
while True:    
    calling = False
    init_voice_time = time.time()

    while True: 
        # Read voice
        tc.listen()
        
        calling = tc.calling("segunda feira")

        if calling:
            if tc.or_verify(["faz", "faça"]):
                if tc.and_verify(["clip"]):
                    print(tc.result)

                    msg = "Make a clip" 
                    tc.reset()    
                    break

    if msg == "Make a clip":
        break    
    

# Vosky
# Coqui