import random

n = random.randint(1, 100)
m = random.randint(1, 100)

connections = []
for i in range(m):
    connections.append([random.randint(1, n), random.randint(1,n)])
output = str()
output+=str(n)+" "+str(m)+"\n"
for c in connections:
    output+=str(c[0])+" "+str(c[1])+"\n"

open("testgraph.txt", 'w').write(output)
