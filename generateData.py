# interests: [
#     { name: 'Creative Writing', emoji: '🖊️'},
#     { name: 'Math', emoji: '➕'},
#     { name: 'Teaching', emoji: '🏫'},
#     { name: 'Making Friends', emoji: '🎎'},
#     { name: 'Statistical Analysis', emoji: '📊'},
#     { name: 'ML/AI', emoji: '🤖'},
#     { name: 'Video Editing', emoji: '📹'},
#     { name: 'Scrum/Agile', emoji: '🔄'},
#     { name: 'Persuasion', emoji: '💬},
#     { name: 'Coding', emoji: '💻'},
#     { name: 'Database/SQL', emoji: '📋'},
#     { name: 'Listening', emoji: '👂'},
#     { name: 'Technical Writing', emoji: '📚'},
#     { name: 'Troubleshooting', emoji: '💡'},
#     { name: 'Negotiation', emoji: '🤝'},
# ]
import random
import numpy as np
import math

cT = [0, 0, 1, 0, 0, 7, 1, 0, 5, 5, 0, 4, 2, 10, 5, 6, 8, 3, 3]
bT = [0, 0, 0, 1, 3, 5, 6, 9, 4, 0, 0, 9, 7, 0, 0, 9, 2, 4, 10]


def randomWeight(tmp):
    rand = np.random.normal(0, 0.2)
    tmp = round(tmp * (rand + 1), 2)
    if (tmp > 10):
        tmp = 10
    if (tmp < 0):
        tmp = 0
    return tmp


def generate(typed, num):
    coders = []
    for x in range(num):
        coders.append(typed.copy())
        for y in range(15):
            # generate skills
            tmp = coders[x][y+4] + .5
            coders[x][y+4] = randomWeight(tmp)
            # generate interests
            tmp = 10 - coders[x][y+4]
            coders[x].append(randomWeight(tmp))
    return coders


def makeString(liste):
    return '\n'.join(str(e) for e in liste)


def matches(liste):
    labels = []
    matches = []
    for x in liste:
        for y in liste:
            if x != y:
                diff1 = 0
                diff2 = 0
                # for z in range(2):
                #     diff1 += 1 - math.sqrt((x[z+4] - y[z+6]) ** 2) / 10
                #     diff2 += 1 - math.sqrt((y[z+4] - x[z+6]) ** 2) / 10
                for z in range(15):
                    diff1 += 1 - math.sqrt((x[z+4] - y[z+19]) ** 2) / 10
                    diff2 += 1 - math.sqrt((y[z+4] - x[z+19]) ** 2) / 10
                diff = (diff1 + diff2) / 30
                matches.append(x + y)
                labels.append(round(diff, 2))
    return (matches, labels)


with open("matches.out", 'w') as out, open("labels.out", 'w') as out2:
    random.seed(42)
    coders = generate(cT, 80)
    bizppl = generate(bT, 80)
    allP = coders + bizppl
    finalD = matches(allP)
    out.write(makeString(finalD[0]))
    out2.write(makeString(finalD[1]))
