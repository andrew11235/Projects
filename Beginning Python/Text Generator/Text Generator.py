from random import choice, choices
from nltk import FreqDist, ngrams

while True:
    try:
        with open(input("Input corpus file location: "), "r", encoding="utf-8") as f:
            bdict = dict(FreqDist(list(ngrams(f.read().split(), 3))))  # Dictionary of trigram frequencies
            break
    except FileNotFoundError:
        print("Invalid file location. ", end="")

# Generates 10 sentences
for _ in range(10):
    while True:
        # Ensures starting word is capital and not the end of a sentence
        trigm = choice(list(bdict.keys()))
        while trigm[0][-1] in [".", "!", "?"] or not trigm[0][0].isupper():
            trigm = choice(list(bdict.keys()))

        slist = list(trigm)

        while len(slist) < 15 or slist[-1][-1] not in [".", "!", "?"]:  # Minimum word length and ending punctuation
            lis = {k[-1]: bdict[k] for k in bdict if k[0] == slist[-2] and k[1] == slist[-1]}
            if len(lis) == 0:  # Restarts at trigram dead end
                continue
            slist.append(choices(list(lis.keys()), list(lis.values()))[0])
        print(*slist)
        break
