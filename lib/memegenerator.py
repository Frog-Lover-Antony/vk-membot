# -*- coding: utf-8 -*-

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw


def make_meme(topString, bottomString, filename, font_file="arial.ttf"):
    img = Image.open(filename)
    imageSize = img.size

    # find biggest font size that works
    fontSize = int(imageSize[1] / 5)
    fontPath = "fonts/" + font_file
    font = ImageFont.truetype(fontPath, fontSize)
    topTextSize = font.getsize(topString)
    bottomTextSize = font.getsize(bottomString)
    while topTextSize[0] > imageSize[0] - 20 or bottomTextSize[0] > imageSize[0] - 20:
        fontSize = fontSize - 1
        font = ImageFont.truetype(fontPath, fontSize)
        topTextSize = font.getsize(topString)
        bottomTextSize = font.getsize(bottomString)

    # find top centered position for top text
    topTextPositionX = (imageSize[0] / 2) - (topTextSize[0] / 2)
    topTextPositionY = 0
    topTextPosition = (topTextPositionX, topTextPositionY)

    # find bottom centered position for bottom text
    bottomTextPositionX = (imageSize[0] / 2) - (bottomTextSize[0] / 2)
    bottomTextPositionY = imageSize[1] - bottomTextSize[1]
    bottomTextPosition = (bottomTextPositionX, bottomTextPositionY)

    draw = ImageDraw.Draw(img)

    # draw outlines
    # there may be a better way
    outlineRange = int(fontSize / 15)
    for x in range(-outlineRange, outlineRange + 1):
        for y in range(-outlineRange, outlineRange + 1):
            draw.text((topTextPosition[0] + x, topTextPosition[1] + y), topString, (0, 0, 0), font=font)
            draw.text((bottomTextPosition[0] + x, bottomTextPosition[1] + y), bottomString, (0, 0, 0), font=font)

    draw.text(topTextPosition, topString, (255, 255, 255), font=font)
    draw.text(bottomTextPosition, bottomString, (255, 255, 255), font=font)

    return img


def get_upper(somedata):
    result = ''
    try:
        result = somedata.decode("utf-8").upper()
    except:
        result = somedata.upper()
    return result


def get_lower(somedata):
    result = ''
    try:
        result = somedata.decode("utf-8").lower()
    except:
        result = somedata.lower()
    return result
