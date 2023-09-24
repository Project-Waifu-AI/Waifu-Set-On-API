from numpy.random import choice

items = "common","uncommon","rare","super rare"
probabilities = [0.5,0.35,0.1,0.05]
N_TESTS = 10
daftar=[]

for i in range(N_TESTS):
    hasil = choice(items,p=probabilities)
    daftar.append(hasil)
    
print (daftar)