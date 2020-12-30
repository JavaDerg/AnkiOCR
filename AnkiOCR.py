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

enable_debug = False

src_config_file = './config.txt'
src_image_path = './img/'
src_keywords_path = './keywords/'
orig_debug_path = './debug/orig/'
edit_debug_path = './debug/edit/'
name_debug_image = 'anki03'
image_file_extension = '.JPG'
ocr_extract_lang = 'deu'

card_font_family = 'Courier'
card_font_size = 'medium'

keywords_font_family = 'Courier'
keywords_font_size = 'medium'
keywords_color = 'orange'
enable_colored_keywords = True
enable_kursiv_keywords = True
enable_bold_keywords = True
enable_underlined_keywords = True


print("currently using tesseract: " + str(pytesseract.get_tesseract_version()))

# other languages can be installed by
# sudo apt-get install tesseract-ocr-[language code]
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
    # TODO
    return "front"

def cropImage(img, side):
    card = Image.open(img)
    width, height = card.size
    
    if side == "front":
        cropped = card.crop((180, 140,width-40, height-15)) #TODO adjust values for crop
    elif side == "back":
        cropped = card.crop((180, 140,width-40, height-15)) # TODO adjust values for crop
    else:
        print("[ERROR] No Side")
    return cropped

def extractOCR(img):
    data = pytesseract.image_to_string(img, ocr_extract_lang)
    return data[:-1] # crop away the note sign at the end

def styleData(data):
    data = data.replace('\n', "<br>")
    data = f'<span style="font-size:{card_font_size};font-family:{card_font_family}">' + data + '</span>'
    return data

def highlightKeywords(data):
    # kursiv <em></em>
    #for keys in keywords:
        
        #for key in range (0,len(keys)):
            #if key in data.to_lowercase():
                #print("success")
            #else:
                #print("Nothing found")
    if enable_colored_keywords: pass
    if enable_kursiv_keywords: pass
    if enable_bold_keywords: pass
    if enable_underlined_keywords: pass
    return data

def writeTSVFile(data):
    pass

# CHECK IF OCR CODE IS INCLUDED IN INSTALLED LANG's. NEEDS TO BE PRESENT FOR OCR!
if ocr_extract_lang in langs:
    keywords = loadKeywords()

    if enable_debug: begin = time.time()
    ##data.append(styleData(extractOCR(cropImage(src_image_path+files[1], getCardSide()))))
    #data = styleData(extractOCR(cropImage(src_image_path+files[1], getCardSide())))
    data = highlightKeywords(extractOCR(cropImage(src_image_path+files[1], getCardSide())))
    #with open('./output.csv', 'w') as file:
    #    file.write(data)
    if enable_debug:
        end = time.time()
        print(f"Execution of one image cycle: {end-begin:.2f}s")
        print(data)

    print("Jobs are done")
    
else:
    print(f'Please install following Tesseract OCR Language: {ocr_extract_lang}')