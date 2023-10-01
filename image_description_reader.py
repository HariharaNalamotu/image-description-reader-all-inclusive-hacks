import requests
from gtts import gTTS
import os
import time
from pywinauto import Application
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

print("import statements done")

time.sleep(10)

while __name__ == '__main__':
    failed = False
    print("x")
    app = Application(backend='uia')
    print("x")
    app.connect(title_re=".*Chrome.*", visible_only=True)
    print("x")
    element_name="Address and search bar"
    print("x")
    dlg = app.top_window()
    print("x")
    open_url = dlg.child_window(title=element_name, control_type="Edit").get_value()
    print('https://'+open_url)
    response = requests.get('https://'+open_url)
    print("x")
    print("window url recieved")
    print("x")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')
        image_urls = []
        for img_tag in img_tags:
            src = img_tag.get('src')
            if src:
                absolute_url = urljoin(open_url, src)
                image_urls.append(absolute_url)
                print(absolute_url)
                print("image gotten")

    else:
        failed = True
        print("images not gotten")

    if not failed:
        url = "https://image-caption-generator2.p.rapidapi.com/v2/captions"
        for image_url in image_urls[1:-2]:
            print(image_url)
            print(open_url)
            querystring = {"imageUrl":image_url,"useEmojis":"false","useHashtags":"false","limit":"3"}
    
            headers = {
                "X-RapidAPI-Key": "e7e186ed7dmsha150a1dd0b1525fp1aa0f1jsn21b71f49a691",
                "X-RapidAPI-Host": "image-caption-generator2.p.rapidapi.com"
            }
            
            response = requests.get(url, headers=headers, params=querystring)
            print(response.json())
            text = response.json()['captions'][0]
            
            tts = gTTS(text)
            
            temp_audio_file = "output.mp3"
            tts.save(temp_audio_file)
            
            os.system(f"start {temp_audio_file}")
            
            estimated_duration = len(text) / 6.0
            
            time.sleep(estimated_duration + 1)
            
            os.remove(temp_audio_file)
    else:
        text = "Permission to website denied"
        tts = gTTS(text)
            
        temp_audio_file = "output.mp3"
        tts.save(temp_audio_file)
            
        os.system(f"start {temp_audio_file}")
            
        estimated_duration = len(text) / 6.0
           
        time.sleep(estimated_duration + 1)
        
        os.remove(temp_audio_file)
