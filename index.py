from flask import Flask

app = Flask(__name__)
import random
import ollama
from flask import Flask
from flask_cors import CORS

wordset = set()
f = open('./data/large_wc.txt')

count = 0

for word in f:
    word = word.split()[0]
    if len(word) > 3:
        wordset.add(word)
        count += 1
    if count == 2000:
        break
print(len(wordset))

app = Flask(__name__)
CORS(app)

@app.route("/")
def get_words():
    possible_words = set()
    aeiou = list("aeiou")
    letters = list("qwrtypsdfghjklzxcvbnm")
    while len(possible_words) < 20:
        possible_words = set()
        random.seed()
        random.shuffle(letters)
        random.shuffle(aeiou)
        chosen = letters[:5]
        chosen.extend(aeiou[:2])
        chosen_set = set(chosen)
        empty = set()
        for word in wordset:
            if set(list(word)).difference(chosen_set) == empty:
                possible_words.add(word)
        print(len(possible_words))
    # html_to_ret = "<p>{0}</p><p>{1}</p>".format(chosen, possible_words
    json = {"chosen":list(chosen), "possible_words":list(possible_words)}
    return json


def get_hint(word):
    response = ollama.chat(
        model="llama3.1",
        messages=[
            {
                "role": "system",
                "content": "Reply with the word and a 1 sentence clue about the word, nothing else.",
            },
            {"role": "user", "content": word},
        ],
    )
    return response


if __name__ == "__main__":
    json = get_words()
    possible_words = json['possible_words']
    chosen = json['chosen']
    print(possible_words)
    print(chosen)
    possible_words = sorted(list(possible_words), key=lambda x: len(x), reverse=True)

@app.route("/api")
def api():
    return get_words()
    # with open("data.json", mode="r") as my_file:
    #     text = my_file.read()
    #     return text
