import requests
import json
import os
import tkinter
from tkinter import messagebox,font

# 定义歌曲下载类
class Download():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    }

    def __init__(self):
        # 窗口搭建
        windown = tkinter.Tk()
        windown.title('donmo下载歌曲')
        windown.geometry('500x400')
        windown.resizable(width=False,height=False)

        # 标签
        label_message1 = tkinter.Label(windown,text='警告：本程序仅供学习交流，请勿违法行为，后果自负',font='华文隶书',fg='red')
        label_message2 = tkinter.Label(windown, text=' 请按格式输入，不然找不到你想要的版本', font='华文隶书')
        label_message3 = tkinter.Label(windown, text=' 输入格式：李荣浩 - 年少有为', font= '华文隶书')
        label_message1.pack(side='top', pady=40)
        label_message2.pack(side='top',pady=10)
        label_message3.pack(side='top',pady=10)

        # 输入框
        self.input_name = tkinter.Entry(windown,width=35,font= '华文隶书')
        self.input_name.pack(side='top',pady=10)

        # 按钮
        btn = tkinter.Button(windown,text='搜索',font= '华文隶书',command=self.down)
        btn.pack(side = 'top',pady=20,ipady=10,ipadx=120,)

        label_qun = tkinter.Label(windown, text=' 学习交流群&程序下载：924776571', font='华文隶书',fg='red')
        label_qun.pack(side='top',pady=20)

        windown.mainloop()

    # 发送请求获取响应
    def get_info(self,url):
        return requests.get(url=url, headers=self.headers)

    # 输入要搜索的歌曲和歌手，这样找到你想要的歌曲准确度高一些，得到歌曲的 hash值，后面需要用到
    def get_hash(self):
        name_singer = self.input_name.get()
        #     构建搜索url,这里我设置返回结果是15条
        search_url = 'https://songsearch.kugou.com/song_search_v2?callback=jQuery11240318739477178112_1583839575037&keyword=' + name_singer + '&page=1&pagesize=15&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0&_=1583839575039'

        #     解析返回的json数据，取到 歌曲的 hash值
        response = self.get_info(search_url)

        #     将json数据转成python类型，这里把前缀和后缀给切掉，换成json转字典得格式，便于转化
        songinfo = response.text.replace('jQuery11240318739477178112_1583839575037(', '')[:-2]
        songinfo = json.loads(songinfo)

        #     解析数据
        data = songinfo['data']
        lists = data['lists']

        # 这里可以选择需要下载得类型,不过后面我有一个需求,所以我选择下载热度第一首,可自行选择
        # 我这里用户输入得关键字,与filename 相匹配,匹配上则筛选出用户想要得版本,考虑到翻唱好听的

        for item in lists:
            FileName = item['FileName']
            #     这里判断是否和用户输入的一样
            if name_singer == FileName:
                return item['FileHash'], FileName

        # 与用户输入的不相等   默认返回第一个
        hash = data['lists'][0]['FileHash']

        # 这里对数据进行修改 :  鱼大仙 - <em>我曾</em>,是这样的
        filename = data['lists'][0]['FileName']
        FileName = FileName.replace(' ', '').replace('<em>', '').replace('</em>', '')

        return hash, FileName

    # 得到了歌曲hash，构建歌曲源地址请求url，得到播放源,并下载
    def get_song(self,hash):
        # 这里mid参数，我也不知道有什么作用，但是必须带上，不然请求得不到数据
        song_url = 'https://wwwapi.kugou.com/yy/index.php?r=play/getdata&hash=' + hash + '&mid=0bfd8d07f43f36898c1d68bd2f657099'
        response = self.get_info(song_url)

        #     解析数据
        data = json.loads(response.text)['data']
        #     歌词
        lyrics = data['lyrics']
        #     播放地址
        play_url = data['play_url']

        return lyrics, play_url

    # 歌词,歌曲写入文件
    def download(self,songname, lyrics, play_url):
        path = 'donmo下载歌曲/' + songname
        #     创建一个文件夹
        if not os.path.exists(path):
            os.makedirs(path)

        filename = os.path.join(path, songname + '.txt')
        song = os.path.join(path, songname + '.mp3')
        with open(filename, 'w', encoding='utf-8') as fp:
            fp.write(lyrics)
            fp.close()

        with open(song, 'wb') as fp:
            data = self.get_info(play_url).content
            fp.write(data)
            fp.close()

        print('下载成功!!!!!!!!')




    def down(self):
        try:
            hash, filename = self.get_hash()
            lyrics, play_url = self.get_song(hash)
            self.download(self.input_name.get(), lyrics, play_url)
            messagebox.showinfo('下载成功！！！路径为当前目录')
        except:
            messagebox.showinfo('下载失败，请重新加载！！！')


if __name__ == '__main__':
     Download()
