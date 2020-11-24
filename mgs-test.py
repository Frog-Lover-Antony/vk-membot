from lib import memegenerator
from random import randint

img = memegenerator.make_meme("fuck it", "deocumentation watching moment", "lib/successkid.jpg")
img.save(str(randint(0, 255)) + ".png")
