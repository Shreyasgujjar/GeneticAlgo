import random
from PIL import Image, ImageDraw
from operator import itemgetter

# Function to create random genes
def mutated_genes():
    x1 = random.randint(0, 21)
    y1 = random.randint(0, 21)
    size = random.randint(1,5)
    shape = [(x1,y1),(x1 + size,y1+ size)] 
    return shape

# Function to create a complete gnome
def create_gnome():
  return [mutated_genes() for _ in range(100)]

# Evaluation function
# Checks how close the image generated is to the 
# final image
def fitness(gnome):
  w, h = 32, 32
  newImg = Image.new("RGB", (w, h),"white")
  image = ImageDraw.Draw(newImg,'RGBA') 
  # Draw rectangles
  for ordinates in gnome:
    image.rectangle(ordinates, (105,105,105,125))
  pix = newImg.load()
  loss = 0
  pixels = Image.open('star.jpg').load()
  # Find out the difference / loss value
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

# Get a child gnome based on the logic
# random number is less than 0.45 -> assumes 1st parent gene
# random number is less than 0.9 and more than 0.45 -> assumes 2nd parent gene
# random number is more than 0.9 -> mutate the gene in this case
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

size = 100

gen = 1
match = 0

# Create gnomes with a size equal to the population size
gnomes = [create_gnome() for i in range(size)]

population = []

# Calculate and create a dict of gnomes with there fitness
for gnome in gnomes:
  sample = {}
  sample["gnome"] = gnome
  sample["fitness"] = fitness(gnome)
  population.append(sample)

# Checks if a aproximate match is found
while not match:
  # Sort the population based on their fitness
  population = sorted(population, key= itemgetter('fitness'))
  print("Least loss for gen " + str(gen) + " - " + str(population[0]['fitness']))
  # Stop once the fitness below 15000 is found
  if population[0]['fitness'] <= 15000:
    newImg = Image.new("RGB", (32, 32), "white")
    image = ImageDraw.Draw(newImg, 'RGBA')
    for ordinates in population[0]['gnome']:
      image.rectangle(ordinates, (105,105,105,125))
    newImg.show()
    match = 1
  # Assumes the highest fit people for the next generation
  newGen = [gnome for gnome in population[:10]]
  # Randomly mates the population to form children
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