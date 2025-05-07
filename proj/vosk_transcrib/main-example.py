import time
from transcrib import Transcrib

tc = Transcrib()
msg = ""
while True:    
    calling = False
    init_voice_time = time.time()

    while True: 
        # Read voice
        tc.listen_bigbrain()
        pvd = tc.partial
        print(pvd["partial"]['list'][1])
        
        #if not calling:
        if (
            "segunda" in pvd["partial"]['list'][1] and
            "feira" in pvd["partial"]['list'][1]
        ):
            print(pvd["partial"]['str'])
            calling = True
            tc.reset()

        if calling:
            if (
                "faça" in pvd["partial"]['list'][1] or
                "faz" in pvd["partial"]['list'][1]
            ):
                if (
                    "clipe" in pvd["partial"]['list'][1]
                ):
                    print(pvd["partial"]['str'])

                    msg = "Make a clip" 
                    tc.reset()    
                    break

    if msg == "Make a clip":
        break    
    

# Vosky
# Coqui