import requests
from html.parser import HTMLParser
import json

class HTMLFilter(HTMLParser):
    text = ""
    new_line = True
    def handle_data(self, data):
        if "." in data:
            self.text += data + "\n"
            self.new_line = True
        else:
            if self.new_line:
                self.text += "- " + data
                self.new_line = False
            else:
                self.text += data


def get_reference(url):
    r = requests.get(url)
    r.encoding = 'UTF-8'

    i = r.text.find('<div class="main">')

    r = r.text[i:]

    i = r.find('<h1 id="twitch-api-reference">Twitch API Reference</h1>')
    

    return r[i:]

def get_functions(html:str):
    f = []

    inicio = '<section class="left-docs">'
    final = '<section class="doc-content">'

    t = html

    while t.find(final) != -1:
        i = t.find(inicio) + len(inicio)
        t = t[i:]
        _i = t.find(final)

        f.append(t[:_i])

        t = t[_i+len(final):]

    i = t.find(inicio) + len(inicio)
    t = t[i:]
    _i = t.find(final)

    f.append(t[:_i])

    return f

def get_info(functions: list):
    out = {}
    
    for i_f, f in enumerate(functions):
        inicio = '<h2 id="'
        final = '">'

        i = f.find(inicio) + len(inicio)
        f = f[i:]
        _i = f.find(final)

        f_id = f[:_i]

        out[f_id] = {}

        f = f[_i:]

        inicio = '<h3>Response Codes</h3>'
        final = '</tbody></table>'

        i = f.find(inicio) + len(inicio)
        f = f[i:]
        _i = f.find(final)

        f_errors = f[:_i]

        inicio = '<tr>'
        final = '</tr>'
        e_inicio = '<td>'
        e_final = '</td>'

        out[f_id]['errors'] = {}

        if i == len('<h3>Response Codes</h3>') -1:
             out[f_id]['errors']["OK CODE"] = ""

        while f_errors.find(inicio) != -1:
            i = f_errors.find(inicio) + len(inicio)
            f_errors = f_errors[i:]
            _i = f_errors.find(final)

            e = f_errors[:_i]

            f_errors = f_errors[_i+len(final):]

            for __i in range(0, 2):
                i = e.find(e_inicio) + len(e_inicio)
                e = e[i:]
                _i = e.find(e_final)

                if __i == 0:

                    code = e[:_i]

                    e = e[_i+len(e_final):]
                if __i == 1:

                    descr = e[:_i]

                    e = e[_i+len(e_final):]

            if "OK" in code or "Accepted" in code:
                out[f_id]['errors']["OK CODE"] = code[:3]

            if code[:3].isdigit():
                h = HTMLFilter()
                h.feed(descr)

                out[f_id]['errors'][code[:3]] = [code, h.text] 

            f = f_errors

    return out

if __name__ == "__main__":
    page = get_reference("https://dev.twitch.tv/docs/api/reference/")
    
    l = get_functions(page)

    f = get_info(l)

    with open("./docs/errors docs/errors.json", "w", encoding="UTF-8") as file:
        json.dump(f, file, indent=4, ensure_ascii=False)
    file.close()

    

    
    
    