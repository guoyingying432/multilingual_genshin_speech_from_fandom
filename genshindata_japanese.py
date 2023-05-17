from bs4 import BeautifulSoup
import os,re,traceback
from httpx import AsyncClient
import asyncio

FILE_PATH = os.path.dirname(__file__)
Audio_PATH = os.path.join(FILE_PATH,"jaAudio")
baseurl = "https://genshin-impact.fandom.com/wiki/Genshin_Impact_Wiki"

async def get_url(url):
    async with AsyncClient() as client:
        req = await client.get(
            url=url
        )
    return req.text

async def download(url,char_name,file_name,text):
    #print("正在下载{} 的 {}".format(char_name,file_name))
    #print(url)
    #text=text.replace("...","")
    #text=text.replace("—","")
    try:
        async with AsyncClient() as client:
            req = await client.get(
                url=url
            )

        while(1):
            if os.path.exists(os.path.join(Audio_PATH,char_name)):
                with open (os.path.join(os.path.join(Audio_PATH,char_name),file_name), 'wb') as f:
                    f.write(req.content)
                    f.close
                #print("下载完成!")
                break
            else:
                os.makedirs(os.path.join(Audio_PATH,char_name), exist_ok=True)
        #with open(os.path.join(Audio_PATH,char_name,char_name+".txt"), 'a') as file:
        #    file.write(file_name+"|"+text+ "\n")
    except:
        traceback.print_exc()
        print("下载失败，{}文件不存在。".format(url),"文本是{}".format(text))
        #print(text[41])
        #import sys
        #sys.exit()

async def main():
    print("runn")
    base_data = await get_url(baseurl)
    content_bs = BeautifulSoup(base_data, 'lxml')
    #print(content_bs)
    raw_data_5star = content_bs.find_all("span",class_='card-image card-rarity-5')
    raw_data_4star = content_bs.find_all("span",class_='card-image card-rarity-4')
    raw_data = raw_data_5star + raw_data_4star
    char_list = {}
    #print(raw_data)
    for i in raw_data:
        char_url = "https://genshin-impact.fandom.com" + i.find("a")["href"] + "/Voice-Overs/Japanese"
        if i.find("a")["title"] != "Traveler":
            char_list[i.find("a")["title"]] = char_url
    print(char_list)
    print(len(char_list))
    for i in char_list.keys():
        cahr_voice_data = await get_url(char_list[i])
        voice_bs = BeautifulSoup(cahr_voice_data, 'lxml')
        voice_data = voice_bs.find_all("table",class_='wikitable')

        #voice_data = voice_bs.find_all("span",class_='audio-button custom-theme hidden')
        tasks = []
        if len(voice_data)//2 == 6:
            audio_index = [0,4,8]
        else:
            audio_index = [0,len(voice_data)//2]
        #print(voice_data)
        #print(audio_index)
        temp_title = ""
        """
        print(voice_data[0].tbody.find_all("tr")[1])
        print(voice_data[0].tbody.find_all("tr")[2])
        print(voice_data[0].tbody.find_all("tr")[3])
        print(voice_data[0].tbody.find_all("tr")[4])
        print(voice_data[1].tbody.find_all("tr")[-2])
        print(voice_data[1].tbody.find_all("tr")[-1])
        """
        #import sys
        #sys.exit()
        for g in audio_index:
            #print(voice_data[g])
            for k in voice_data[g].tbody.find_all("tr")[1:]:
                #print(k)
                if len(k.find_all("td")) == 0:
                    continue
                if len(k.td.find_all("span",lang='ja'))==0:
                    continue
                #print(k)
                #print(k.td.find_all("span",lang='en'))
                tmp=k.td.find_all("span",lang='ja')
                #print(tmp[0])
                # Parse the HTML text
                soup = BeautifulSoup(str(tmp[0]), 'html.parser')

                # Extract the cleaned text
                cleaned_text = soup.get_text()

                
                
                
                #print(k)
                if len(k.find_all("th")) == 0:
                    audio_title = temp_title
                else:
                    audio_title = k.find_all("th")[0].text
                    temp_title = audio_title

                audio_url = []
                title=[]
                for j in k.td.find_all("span",class_='audio-button custom-theme hidden'):
                    audio_url.append(j.find_all("a")[0]["href"])
                    title.append(j.find_all("a")[0]["title"])
                
                
                
                #audio_chinese_title = ''.join(re.findall('[\u4e00-\u9fa5]', audio_title))
                #print(audio_url)
                #print(title)
                
                if len(audio_url) == 1:
                    tasks.append(
                        download(audio_url[0],i,"{}".format(title[0]),cleaned_text))
                elif len(audio_url) > 1:
                    print(cleaned_text)
                    print(audio_url)
                    print(title)
                    continue
                    
                    #for index,j in enumerate(audio_url):
                    #    tasks.append(
                    #        download(j,i,"{}".format(title[index])))
                

                #await download(audio_url,i,"{}.ogg".format(audio_chinese_title))

                #audio_url = k.find("a")["href"]
                #print(audio_url)

        await asyncio.wait(tasks)
      
        

    #os.makedirs(file, exist_ok=True)

if __name__ == "__main__":
    print("run")
    asyncio.run(main())