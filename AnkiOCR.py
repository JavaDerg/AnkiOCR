################
#    IMPORT
################
try:
    from PIL import Image, ImageDraw
    print('[SUCCESS] Imported Pillow')
except ImportError:
    import Image
    print('[ERROR] Importing Pillow failed!\nWill use Image lib')
import pytesseract
from os import listdir
import time
import csv
import re
import pandas as pd
import configparser
from pathlib import Path

################
#    VARIABLES
################

config_file_path = './config.ini'
configPath = Path(config_file_path)
config = configparser.ConfigParser(allow_no_value=True)
config.optionxform = str # disable lowercase writing

def writeConfig():
    print('[INFO] writing config file...')
    config['DEBUG'] = {'enable_debug' : 'False'}
    config['BASIC'] = {'output_file' : './output.csv',
                       'src_config_file' : './config.txt',
                       'src_image_path' : './img/',
                       'src_keywords_path' : './keywords/',
                       '; Do not forget to install you Pytesseract-Lang-Package!':None, 'ocr_extract_lang' : 'deu'}
    config['CARD STRATEGY'] = {'; "OneByOne" or "FlipFlop"':None, 'card_Side_Strategy' : 'FlipFlop', 
                               'is_First_Card_Front' : 'True'}
    config['CROPPING FRONT'] = {'front_margin_top' : '0',
                                'front_margin_bottom' : '0',
                                'front_margin_left' : '0',
                                'front_margin_right' : '0'}
    config['CROPPING BACK'] = {'back_margin_top' : '0',
                               'back_margin_bottom' : '0',
                               'back_margin_left' : '0',
                               'back_margin_right' : '0'}
    config['CARD STYLING'] = {'; keep the installed fonts in mind!':None, 'card_font_family' : 'Arial',
                              '; xx-small x-small small medium large x-large xx-large':None, 'card_font_size' : 'medium'}
    config['KEYWORD STYLING'] = {'; keep the installed fonts in mind!':None, 'keywords_font_family' : 'Arial',
                                 '; xx-small x-small small medium large x-large xx-large':None, 'keywords_font_size' : 'medium',
                                 '; valid css colors as name or hex value':None,'keywords_color' : 'orange',
                                 'enable_colored_keywords' : 'True',
                                 'enable_italic_keywords' : 'False',
                                 'enable_bold_keywords' : 'True',
                                 'enable_underlined_keywords' : 'False'}
    
    with open(config_file_path, 'w') as configfile:
        config.write(configfile)
    print('[SUCCESS] config file written!')
        
def readConfig():
    print('[INFO] reading in config file...')
    config.read(config_file_path)
    
    #    DEBUG
    global enable_debug
    enable_debug = config['DEBUG'].getboolean('enable_debug')

    #    BASIC
    global output_file
    output_file = config['BASIC']['output_file']
    global src_config_file
    src_config_file = config['BASIC']['src_config_file']
    global src_image_path
    src_image_path = config['BASIC']['src_image_path']
    global src_keywords_path
    src_keywords_path = config['BASIC']['src_keywords_path']
    global ocr_extract_lang
    ocr_extract_lang = config['BASIC']['ocr_extract_lang']

    #    CARD STRATEGY
    global card_Side_Strategy
    card_Side_Strategy = config['CARD STRATEGY']['card_Side_Strategy']
    global is_First_Card_Front
    is_First_Card_Front = config['CARD STRATEGY'].getboolean('is_First_Card_Front')

    #    CROPPING FRONT
    global front_margin_top
    front_margin_top = int(config['CROPPING FRONT']['front_margin_top'])
    global front_margin_bottom
    front_margin_bottom = int(config['CROPPING FRONT']['front_margin_bottom'])
    global front_margin_left
    front_margin_left = int(config['CROPPING FRONT']['front_margin_left'])
    global front_margin_right
    front_margin_right = int(config['CROPPING FRONT']['front_margin_right'])

    #    CROPPING BACK
    global back_margin_top
    back_margin_top = int(config['CROPPING BACK']['back_margin_top'])
    global back_margin_bottom
    back_margin_bottom = int(config['CROPPING BACK']['back_margin_bottom'])
    global back_margin_left
    back_margin_left = int(config['CROPPING BACK']['back_margin_left'])
    global back_margin_right
    back_margin_right = int(config['CROPPING BACK']['back_margin_right'])

    #    CARD STYLING
    global card_font_family
    card_font_family = config['CARD STYLING']['card_font_family']
    global card_font_size
    card_font_size = config['CARD STYLING']['card_font_size']

    #    KEYWORD STYLING
    global keywords_font_family
    keywords_font_family = config['KEYWORD STYLING']['keywords_font_family']
    global keywords_font_size
    keywords_font_size = config['KEYWORD STYLING']['keywords_font_size']
    global keywords_color
    keywords_color = config['KEYWORD STYLING']['keywords_color']
    global enable_colored_keywords
    enable_colored_keywords = config['KEYWORD STYLING'].getboolean('enable_colored_keywords')
    global enable_italic_keywords
    enable_italic_keywords = config['KEYWORD STYLING'].getboolean('enable_italic_keywords')
    global enable_bold_keywords
    enable_bold_keywords = config['KEYWORD STYLING'].getboolean('enable_bold_keywords')
    global enable_underlined_keywords
    enable_underlined_keywords = config['KEYWORD STYLING'].getboolean('enable_underlined_keywords')
    
    print('[SUCCESS] config file read finished!')
    
def loadKeywords():
    temp = []
    with open(f'{src_keywords_path}{ocr_extract_lang}.csv',encoding='utf16') as csvfile:
        wordslist = csv.reader(csvfile)
        for key in wordslist:
            temp.append(key[0]) # no double array problem
    if enable_debug: print(f'[DEBUG] Keywords: \n{temp}')
    return temp

def getCardSide(cardid):
    if card_Side_Strategy == "FlipFlop":
        if is_First_Card_Front:
            if cardid%2 == 0:
                if enable_debug: print(f'[INFO] {cardid} is front with "{card_Side_Strategy}" strategy')
                return "front"
            else:
                if enable_debug: print(f'[INFO] {cardid} is back with "{card_Side_Strategy}" strategy')
                return "back"
        else:
            if cardid%2 != 0:
                if enable_debug: print(f'[INFO] {cardid} is front with "{card_Side_Strategy}" strategy')
                return "front"
            else:
                if enable_debug: print(f'[INFO] {cardid} is back with "{card_Side_Strategy}" strategy')
                return "back"
        
    elif card_Side_Strategy == "OneByOne":
        half = totalNumOfImages*0.5
        
        if is_First_Card_Front:
            if cardid < half:
                if enable_debug: print(f'[INFO] {cardid} is front with "{card_Side_Strategy}" strategy')
                return "front"
            else:
                if enable_debug: print(f'[INFO] {cardid} is back with "{card_Side_Strategy}" strategy')
                return "back"
        else:
            if cardid >= half:
                if enable_debug: print(f'[INFO] {cardid} is front with "{card_Side_Strategy}" strategy')
                return "front"
            else:
                if enable_debug: print(f'[INFO] {cardid} is back with "{card_Side_Strategy}" strategy')
                return "back"

def cropImage(img, side):
    card = Image.open(img)
    width, height = card.size
    
    if side == "front":
        cropped = card.crop((front_margin_left, front_margin_top, width-front_margin_right, height-front_margin_bottom))
    elif side == "back":
        cropped = card.crop((back_margin_left, back_margin_top, width-back_margin_right, height-back_margin_bottom))
    else:
        print('[ERROR] No Side')
    return cropped

def extractOCR(img):
    data = pytesseract.image_to_string(img, ocr_extract_lang)
    if enable_debug: print(f'[DEBUG] Extracted data: {data}')
    return data[:-1] # crop away the note sign at the end

def styleData(data):
    data = data.replace('\n', '<br>')
    data = f'<span style="font-size:{card_font_size};font-family:{card_font_family}">' + data + '</span>'
    if enable_debug: print(f'[DEBUG] Styled data: {data}')
    return data

def highlightKeywords(data):
    for key in keywords:
        searchPhrase = re.search(key, data, re.IGNORECASE)
        
        if searchPhrase: # check if keyword is present in data
            origKey = searchPhrase.group() # save the original key for later
            
            if enable_debug:
                print('[DEBUG] Found keyword!')
                print(f'[DEBUG] Original Keyword Position: {searchPhrase.span()}')
                print(f'[DEBUG] Original Keyword: "{origKey}"')
                
            if enable_colored_keywords: data = re.sub(key, f'<span style="color:{keywords_color}"{key}</span>', data, flags=re.IGNORECASE)
            if enable_italic_keywords: data = re.sub(key, f'<em>{key}</em>', data, flags=re.IGNORECASE)
            if enable_bold_keywords: data = re.sub(key, f'<b>{key}</b>', data, flags=re.IGNORECASE)
            if enable_underlined_keywords: data = re.sub(key, f'<u>{key}</u>', data, flags=re.IGNORECASE)
            
            data = re.sub(key, origKey, data, flags=re.IGNORECASE) # insert the original keyword back again
            
    if enable_debug: print(f'[DEBUG] Highlighted keywords: {data}')
    
    return data

def addToDataFrame(data, cardid, cardSide, row):
    if enable_debug: print(f'[DEBUG] data: \n{data}\nfrom card index : {cardid}    with: {cardSide} at row: {row}') 
    
    if card_Side_Strategy == "FlipFlop":
        if cardid%2 == 0:
            output.at[row, cardSide] = data
            return row
        else:
            output.at[row, cardSide] = data
            return row + 1
        
    if card_Side_Strategy == "OneByOne":
        half = totalNumOfImages*0.5
        if cardid <= half:
            output.at[row, cardSide] = data
            return row + 1
        else:
            index = rowCounter-half
            output.at[index, cardSide] = data
            return row + 1

def numericalSort(value):
    """
        extracts values to sort on a numerical basis

        in: string 'file-name' of the image
        
        out: list of tokens
    """
    
    if enable_debug: print(f'[DEBUG] regex: {value}')
    parts = numbers.split(value)
    
    if enable_debug: print(f'[DEBUG] parts: {parts}')
    parts[1::2] = map(int, parts[1::2])
    
    if enable_debug: print(f'[DEBUG] mapped parts: {parts}')
    return parts


################
#    SETUP
################

# create config file if not already present
if not configPath.exists():
    print("No config found")
    writeConfig()
readConfig()

# pytesseract version
print('[INFO] currently using tesseract: ' + str(pytesseract.get_tesseract_version()))

# other languages can be installed by
# sudo apt install tesseract-ocr-[language code]
langs = pytesseract.get_languages(config='')
print(f'[INFO] following languages are availible:\n   {langs}')

# get a numerical sorted list of all files and the total count
numbers = re.compile(r'(\d+)') # matches numerical token with multiple digits
files = sorted(listdir(path=src_image_path), key=numericalSort)
totalNumOfImages = len(files)
if enable_debug:
    print(f'[INFO] {totalNumOfImages} image files are present in "{src_image_path}"')
    print(f'[INFO] Following files are present:\n    {files}')
        
################
#    LOOP
################ 

# CHECK IF OCR CODE IS INCLUDED IN INSTALLED LANG's. NEEDS TO BE PRESENT FOR OCR!
if ocr_extract_lang in langs:
    if totalNumOfImages%2 != 0:
        print('[ERROR] One Front or Back Card is missing!\nPlease check you Input Folder!')
    else:
        keywords = loadKeywords()
    
        cardID = 0 # Zero based counting!
        
        rowCounter = 0
        
        # pre-allocate memory for all images
        pattern = ["",""]
        preAlloc = [pattern] * int(totalNumOfImages*0.5)
        output = pd.DataFrame(preAlloc, columns=["front", "back"])
        
        while cardID < totalNumOfImages:
            # main working cycle
            if enable_debug: begin = time.time()
    
            cardSide = getCardSide(cardID)
            rowCounter = addToDataFrame(styleData(highlightKeywords(extractOCR(cropImage(src_image_path+files[cardID], cardSide)))), cardID, cardSide, rowCounter)
    
            if enable_debug:
                end = time.time()
                print(f'[INFO] Execution of one image cycle: {end-begin:.2f}s')
            
            print(f'[INFO] Card {cardID} has been processed!')
            cardID += 1
        
        # write output to file
        if enable_debug: print(output)
        output.to_csv(output_file, sep='\t', header=False, index=False, encoding='utf16', quoting=csv.QUOTE_NONE)
        
        print('[SUCCESS] Jobs are done')
    
else:
    print(f'[WARNING] Please install following Tesseract OCR Language: {ocr_extract_lang}')