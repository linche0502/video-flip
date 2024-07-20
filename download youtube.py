from pytube import YouTube, Stream
from pytube.innertube import _default_clients
import os, ssl, ffmpeg, sys, shutil




# youtube video url
targets_url= [
    "https://www.youtube.com/watch?v=RUH3nUbvYVU",
    "https://www.youtube.com/watch?v=nEpwIioH4Qs",
    "https://www.youtube.com/watch?v=6r4r-SUtQIE",
    "https://www.youtube.com/watch?v=bdtwRejaRs0",
    "https://www.youtube.com/watch?v=haCx3hZWtO4",
    "https://www.youtube.com/watch?v=xGYDCZ7TsnI",
    "https://www.youtube.com/watch?v=k0OJEd4QjGU",
    "https://www.youtube.com/watch?v=MNJPAg9TzLQ",
    "https://www.youtube.com/watch?v=tg06zhvdjFM",
    "https://www.youtube.com/watch?v=PiI0aEhhYis",
    "https://www.youtube.com/watch?v=Oxt9c6X-k3A",
    "https://www.youtube.com/watch?v=QJ92SQLwVD8",
]
download_to= ""
resolution= "1080p"


# 解決需要ssl問題
ssl._create_default_https_context = ssl._create_stdlib_context
# 解決一些影片有年齡限制.需要登入的問題
_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]
download_to= os.path.join(os.path.abspath(os.path.dirname(__file__)), download_to or "static\\video\\downloads")

# 進度條(not working)
def onProgress(stream, chunk, remains):
    total = stream.filesize                     # 取得完整尺寸
    percent = (total-remains) / total * 100     # 減去剩餘尺寸 ( 剩餘尺寸會抓取存取的檔案大小 )
    print(f' 下載中… {percent:05.2f}%', '█'*(int(percent)), ' '*(100-int(percent)), end='\r')  # 顯示進度，\r 表示不換行，在同一行更新
    if percent == 100: print()

for target_url in targets_url:
    print("url:", target_url)
    yt = YouTube(target_url, on_progress_callback=onProgress)
    print("title:", yt.title)
    
    resolutions= ["1080p", "720p", "480p", "360p"]
    resolutions= resolutions[resolutions.index(resolution):]
    for res in resolutions:
        # for stream in yt.streams.all():
        for stream in yt.streams:
            if stream.mime_type=="video/mp4" and stream.resolution==res:
                if stream.is_progressive:
                    stream.download(filename= os.path.join(download_to, f'{yt.title}.mp4'))
                # 影片沒有聲音檔時, 另外下載聲音檔並合併
                else:
                    print(" -由於沒有影音一體的檔案, 將分別下載影片和聲音部分")
                    # 建立暫存目錄
                    temp_path= os.path.join(os.path.dirname(__file__),"static","temp")
                    if not os.path.exists(temp_path):
                        os.mkdir(temp_path)
                    # 分別下載影片和音訊到暫存目錄s
                    stream.download(filename= os.path.join(temp_path, f'{yt.title}.mp4'))
                    yt.streams.filter(only_audio=True).first().download(filename= os.path.join(temp_path,'audio_part.mp4'))
                    # 設定ffmpeg的路徑(環境變數)
                    os.environ['PATH'] += ';'+ os.path.join(os.path.dirname(__file__),"static","ffmpeg")
                    stream= ffmpeg.input(os.path.join(temp_path, f'{yt.title}.mp4'))
                    audio= ffmpeg.input(os.path.join(temp_path,'audio_part.mp4'))
                    print(" 合併中...", end='\r')
                    ffmpeg.output(audio, stream, os.path.join(download_to, f'{yt.title}.mp4')).run(overwrite_output=True, quiet=True)
                    sys.stdout.write("\r\033[K")
                    # 刪除暫存目錄
                    shutil.rmtree(temp_path)
                break
        # 用以跳出多層迴圈
        else:
            continue
        break


