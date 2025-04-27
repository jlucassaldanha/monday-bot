import json

with open("infos.json", 'r', encoding="UTF-8") as j_info:
    INFOS = json.load(j_info)
j_info.close()

for func in INFOS.keys():
    function_info = INFOS[func]

    title = "\n\n" + func + "\n\n"

    info = "#### " + function_info['info'] + "\n\nParameters:\n"
    
    if info.find("/docs/authentication#app-access-tokens") != -1:
        info = str(info).replace("/docs/authentication#app-access-tokens", "https://dev.twitch.tv/docs/authentication/#app-access-tokens")

    if info.find("/docs/authentication#user-access-tokens") != -1:
        info = str(info).replace("/docs/authentication#user-access-tokens", "https://dev.twitch.tv/docs/authentication/#user-access-tokens")

    query_params = function_info['query']
    query = ""
    if not "None" in query_params.keys():
        for k in query_params.keys():
            query += f"\t{query_params[k][0]} ({query_params[k][1]}) : {query_params[k][3]}\n\n"

    body_params = function_info['body']
    body = ""
    if not "None" in body_params.keys():
        for k in body_params.keys():
            body += f"\t{body_params[k][0]} ({body_params[k][1]}) : {body_params[k][3]}\n\n"

    with open(path+"\\APIdocstrings.md", '+a', encoding="UTF-8") as docstrings_file:
        docstrings_file.write(title)
        docstrings_file.write(info)
        docstrings_file.write("\tclient_id (str): Client aplication id.\n\n\ttoken (str) : User oauth token.\n\n")
        docstrings_file.write(query)
        docstrings_file.write(body)
    docstrings_file.close()

print(info)
print(query)
print(body)

    