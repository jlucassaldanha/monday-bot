name = "segunda feira"


falado = "testando segunda teste"

r = 0
for i, n in enumerate(name.split(" ")):
    if n in falado.split(" "):
        r += 1
    print(r)

if r == len(name.split(" ")):
    print("True")