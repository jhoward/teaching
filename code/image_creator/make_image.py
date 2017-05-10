import Image
import ImageDraw
import ImageFont

width = 1280
height = 1280

if __name__ == "__main__":
    
    background = (255, 255, 255)
    rect = (40, 40, 40)
    
    im = Image.new("RGB", (width, height), background)
    d = ImageDraw.Draw(im)
    
    #f = ImageFont.truetype('/System/Library/Fonts/Keyboard.ttf', 80)
    
    #d.text([80, 80], 'Comparison of rectangles to one of a million pixels', font = f, fill = (230, 230, 230))
    
    
    d.rectangle([80, 1183, 97, 1200], fill = rect)
    

    d.rectangle([80, 980, 100, 1000], fill = rect)
    d.rectangle([80, 776, 104, 800],  fill = rect)
    d.rectangle([80, 570, 110, 600], fill = rect)
    
    d.rectangle([200, 200, 1200, 1200], fill = rect)
    
    im.save("image.png", "PNG")
    
    