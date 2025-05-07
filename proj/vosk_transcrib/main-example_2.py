import time
from transcrib import Transcrib

tc = Transcrib(partial_result=True)
msg = ""
while True:    
    calling = False
    init_voice_time = time.time()

    while True: 
        # Read voice
        tc.listen_bigbrain()
        
        calling = tc.calling("segunda feira")
        print(tc.partial["partial"]["list"][1])

        if calling:
            if tc.or_verify(["faz", "faça"]):
                if tc.and_verify(["clip"]):
                    print(print(tc.partial["partial"]["list"][1]))

                    msg = "Make a clip" 
                    tc.reset()    
                    break

    if msg == "Make a clip":
        break    
    

# Vosky
# Coqui