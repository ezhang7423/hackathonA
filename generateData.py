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

cT = [0, 0, 1, 0, 0, 7, 1, 0, 5, 5, 0, 4, 2, 10, 5, 6, 8, 3, 3]
bT = [0, 0, 0, 1, 3, 5, 6, 9, 4, 0, 0, 9, 7, 0, 0, 9, 2, 4, 10]


random.seed(42)
# with open("data.txt", 'w') as out:


def randomWeight(tmp):
    rand = (random.randint(0, 1000) - 500) / 1000
    tmp = round(tmp * (rand + 1), 2)
    if (tmp > 10):
        tmp = 10
    if (tmp < 0):
        tmp = 0
    return tmp


def generate10000(type):
    coders = []
    for x in range(10000):
        coders.append(type.copy())
        for y in range(15):
            # generate skills
            tmp = cT[y+4]
            tmp = tmp + .5
            coders[x][y+4] = randomWeight(tmp)
            # generate interests
            tmp = 10 - cT[y+4]
            coders[x].append(randomWeight(tmp))
    return coders


def makeString(liste):
    return '\n'.join(str(e) for e in liste)


with open("data.out", 'w') as out:
    coders = generate10000(cT)
    bizppl = generate10000(bT)
    out.write(makeString(coders))
    out.write(makeString(bizppl))
