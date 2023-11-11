import random
 
file = open('11.txt', encoding='utf-8')
data = file.read()
lines = data.split('\n')
line = random.randrange(len(lines))
print(lines[line])
