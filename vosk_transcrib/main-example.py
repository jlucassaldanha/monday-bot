import time
from transcrib import Transcrib

tc = Transcrib()

while True:
    print("::main while")
    
    calling = False
    init_voice_time = time.time()

    while True: 
        print("::voice while")
    
        # Read voice
        tc.listen_bigbrain()
        pvd = tc.partial
        
        print("::rec")

        if (
            "segunda" in pvd["partial"]['list'][1] and
            "feira" in pvd["partial"]['list'][1]
        ):
            print(pvd["partial"]['str'])
            calling = True

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
                    break
           
            print("::rec")
    

# Vosky
# Coqui