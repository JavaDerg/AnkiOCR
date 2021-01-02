try:
    from PIL import Image, ImageDraw
    print("successfully imported Pillow")
except ImportError:
    import Image
    print("error while importing Pillow\nWill use Image lib")
import pytesseract
from os import listdir
import time
import csv
import re

enable_debug = False

src_config_file = './config.txt'
src_image_path = './img/'
src_keywords_path = './keywords/'
orig_debug_path = './debug/orig/'
edit_debug_path = './debug/edit/'
name_debug_image = 'anki03'
image_file_extension = '.JPG'
ocr_extract_lang = 'deu'

front_margin_top = 140
front_margin_bottom = 15
front_margin_left = 180
front_margin_right = 40

back_margin_top = 140
back_margin_bottom = 15
back_margin_left = 180
back_margin_right = 40

card_font_family = 'Courier'
card_font_size = 'medium'

keywords_font_family = 'Courier'
keywords_font_size = 'medium'
keywords_color = 'orange'
enable_colored_keywords = True
enable_italic_keywords = True
enable_bold_keywords = True
enable_underlined_keywords = True


print("currently using tesseract: " + str(pytesseract.get_tesseract_version()))

# other languages can be installed by
# sudo apt install tesseract-ocr-[language code]
langs = pytesseract.get_languages(config='')
print(f"following languages are availible:\n   {langs}" )

files = listdir(path=src_image_path)
print(f"following files are present:\n    {files}")

def loadKeywords():
    temp = []
    with open(f'{src_keywords_path}{ocr_extract_lang}.csv',encoding='utf16') as csvfile:
        wordslist = csv.reader(csvfile)
        for key in wordslist:
            temp.append(key[0]) # no double array problem
    if enable_debug: print(temp)
    return temp

def getCardSide():
    # TODO FlipFlop, OneSide than the Other  
    return "front"

def cropImage(img, side):
    card = Image.open(img)
    width, height = card.size
    
    if side == "front":
        cropped = card.crop((front_margin_left, front_margin_top, width-front_margin_right, height-front_margin_bottom))
    elif side == "back":
        cropped = card.crop((back_margin_left, back_margin_top, width-back_margin_right, height-back_margin_bottom))
    else:
        print("[ERROR] No Side")
    return cropped

def extractOCR(img):
    data = pytesseract.image_to_string(img, ocr_extract_lang)
    return data[:-1] # crop away the note sign at the end

def styleData(data):
    data = data.replace('\n', "<br>")
    data = f'<span style="font-size:{card_font_size};font-family:{card_font_family}">' + data + '</span>'
    if enable_debug: print(data)
    return data

def highlightKeywords(data):
    for key in keywords:
        searchPhrase = re.search(key, data, re.IGNORECASE)
        
        if searchPhrase: # check if keyword is present in data
            origKey = searchPhrase.group() # save the original key for later
            
            if enable_debug:
                print("Found keyword")
                print(f"Original Keyword Position: {searchPhrase.span()}")
                print(f"Original Keyword: {origKey}")
                
            if enable_colored_keywords: data = re.sub(key, f'<span style="font-color:{keywords_color}"{key}</span>', data, flags=re.IGNORECASE)
            if enable_italic_keywords: data = re.sub(key, f'<em>{key}</em>', data, flags=re.IGNORECASE)
            if enable_bold_keywords: data = re.sub(key, f'<b>{key}</b>', data, flags=re.IGNORECASE)
            if enable_underlined_keywords: data = re.sub(key, f'<u>{key}</u>', data, flags=re.IGNORECASE)
            
            data = re.sub(key, origKey, data, flags=re.IGNORECASE) # insert the original keyword back again
            
    if enable_debug: print(data)
    
    return data

def writeTSVFile(data, cardID, cardSideStrategy):
    #with open('./output.csv', 'w') as file:
    #    file.write(data)
    pass

# CHECK IF OCR CODE IS INCLUDED IN INSTALLED LANG's. NEEDS TO BE PRESENT FOR OCR!
if ocr_extract_lang in langs:
    
    keywords = loadKeywords()
    
    cardID = 1
    cardSideStrategy = "FlipFlop"
    
    if enable_debug: begin = time.time()
    
    writeTSVFile(styleData(highlightKeywords(extractOCR(cropImage(src_image_path+files[cardID], getCardSide())))), cardID, cardSideStrategy)
    
    if enable_debug:
        end = time.time()
        print(f"Execution of one image cycle: {end-begin:.2f}s")

    print("Jobs are done")
    
else:
    print(f'Please install following Tesseract OCR Language: {ocr_extract_lang}')