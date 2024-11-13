from flask import Flask
import random
from flask_cors import CORS
import time

app = Flask(__name__)

wordset = set()
f = open('./data/large_wc.txt')
count = 0
for word in f:
    word = word.split()[0]
    if len(word) > 3:
        wordset.add(word)
        count += 1
    if count == 10000:
        break

app = Flask(__name__)
CORS(app)

@app.route("/")
def get_words():
    possible_words = set()
    current_time = time.gmtime()
    ct = current_time.tm_year * 10000 + current_time.tm_mon * 100 + current_time.tm_mday
    honey_c = None
    while len(possible_words) < 20:
        letters = list("qwrtypsdfghjklzxcvbnm")
        aeiou = list("aeiou")
        possible_words = set()
        random.seed(ct)
        random.shuffle(letters)
        random.shuffle(aeiou)
        chosen = letters[:5]
        chosen.extend(aeiou[:2])
        honey_c = aeiou[0]
        chosen_set = set(chosen)
        empty = set()
        for word in wordset:
            if set(list(word)).difference(chosen_set) == empty:
                if honey_c in word:
                    possible_words.add(word)
        ct *= 2
    
    sorted_chosen = letters[:3] + aeiou[:2] + letters[3:5]
    possible_words = [x.upper() for x in possible_words]
    json = {"chosen": sorted_chosen, "possible_words": possible_words, "honey_char": honey_c}
    return json

if __name__ == "__main__":
    json = get_words()
    possible_words = json['possible_words']
    chosen = json['chosen']
    honey_c = json['honey_char']
    possible_words = sorted(list(possible_words), key=lambda x: len(x), reverse=True)
    print(possible_words, chosen, honey_c)

@app.route("/api")
def api():
    return get_words()
    # with open("data.json", mode="r") as my_file:
    #     text = my_file.read()
    #     return text
