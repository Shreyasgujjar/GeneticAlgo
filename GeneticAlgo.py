import random
from PIL import Image, ImageDraw
from operator import itemgetter

def mutated_genes():
    x1 = random.randint(0, 21)
    y1 = random.randint(0, 21)
    size = random.randint(1,5)
    shape = [(x1,y1),(x1 + size,y1+ size)] 
    return shape

def create_gnome():
  return [mutated_genes() for _ in range(100)]

def fitness(gnome):
  w, h = 32, 32
  newImg = Image.new("RGB", (w, h),"white")
  image = ImageDraw.Draw(newImg,'RGBA') 
  for ordinates in gnome:
    image.rectangle(ordinates, (105,105,105,125))
  pix = newImg.load()
  loss = 0
  pixels = Image.open('star.jpg').load()
  for i in range(0,32):
    for j in range(0,32):
      try:
        diffRed   = abs(pixels[i,j]   - pix[i,j][0]) 
        diffGreen  = abs(pixels[i,j]   - pix[i,j][1])
        diffBlue  = abs(pixels[i,j]   - pix[i,j][2])

        pctDiffRed   = diffRed / 255 
        pctDiffGreen = diffGreen / 255
        pctDiffBlue   = diffBlue  / 255
        loss = loss + (((pctDiffRed + pctDiffGreen + pctDiffBlue) / 3) * 100) 
      except:
        diffRed   = abs(pixels[i,j][0]   - pix[i,j][0]) 
        diffGreen  = abs(pixels[i,j][1]   - pix[i,j][1])
        diffBlue  = abs(pixels[i,j][2]   - pix[i,j][2])

        pctDiffRed   = diffRed / 255 
        pctDiffGreen = diffGreen / 255
        pctDiffBlue   = diffBlue  / 255
        loss = loss + (((pctDiffRed + pctDiffGreen + pctDiffBlue) / 3) * 100)
  return loss

def mating(gnome1, gnome2):
  childGnome = []
  for p1, p2 in zip(gnome1, gnome2):
    probablity = random.random()
    if probablity < 0.45:
      childGnome.append(p1)
    elif probablity < 0.9:
      childGnome.append(p2)
    else:
      childGnome.append(mutated_genes())
  return childGnome

from operator import itemgetter

size = 100

gen = 1
match = 0

gnomes = [create_gnome() for i in range(size)]

population = []

for gnome in gnomes:
  sample = {}
  sample["gnome"] = gnome
  sample["fitness"] = fitness(gnome)
  population.append(sample)

while not match:
  population = sorted(population, key= itemgetter('fitness'))
  print("Least loss for gen " + str(gen) + " - " + str(population[0]['fitness']))
  if population[0]['fitness'] <= 15000:
    newImg = Image.new("RGB", (32, 32), "white")
    image = ImageDraw.Draw(newImg, 'RGBA')
    for ordinates in population[0]['gnome']:
      image.rectangle(ordinates, (105,105,105,125))
    newImg.show()
    match = 1
  newGen = [gnome for gnome in population[:10]]
  for i in range(90):
    firstParent = random.choice(population[:50])
    secondParent = random.choice(population[:50])
    count = 0
    while firstParent["gnome"] == secondParent["gnome"] and count != len(population):
      secondParent = random.choice(population[:50])
      count += 1
    child = mating(firstParent["gnome"], secondParent["gnome"])
    newGen.append({
        "gnome": child,
        "fitness": fitness(child)
    })
  population = newGen

  gen += 1