import requests
from bs4 import BeautifulSoup

def get_pitch_pages(html_page):
    with open(html_page) as page:
        soup = BeautifulSoup(page, 'html.parser')
    links = []
    for row in soup.find_all('tr', role='row'):
        link = str(row.find_all('a')[0])[9:67]
        pitch_type =str(row.find_all('td')[0])[4:6]
        links.append({'pitch_type':pitch_type, 'link':link})
    return links

def get_video_url(pitch_link):
    savant_prefix = "https://baseballsavant.mlb.com"
    page = requests.get(savant_prefix + pitch_link)
    soup = BeautifulSoup(page.content, 'html.parser')
    video_source = soup.find_all('source', type="video/mp4")[0]
    video_source = str(video_source)[13:len(video_source)-20]
    return video_source

def download_video(name, url):
    name = name+".mp4"
    r = requests.get(url)
    print("****Connected****")
    f = open(name, 'wb')
    print("Downloading.....")
    for chunk in r.iter_content(chunk_size=255):
        if chunk:
            f.write(chunk)
    print("Done")
    f.close()

def download_videos(pitcher, pitches):
    for i in range(len(pitches)):
        name = "./" + pitches[i]['pitch_type'] + "/" + pitcher + pitches[i]['pitch_type'] + str(i+1)
        url = get_video_url(pitches[i]['link'])
        download_video(name, url)
        print("Downloaded", i+1)
    print("Downloading Complete for " + pitcher)
    

def upload_video(filename):
    pass

def call_download(pitcher):
    pitches = get_pitch_pages("./" + pitcher + ".html")
    download_videos(pitcher, pitches)

call_download("jeff_hoffman")