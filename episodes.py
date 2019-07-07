from lib import genio
from parallel import Parallel_Downloader
import threading
import json
import time










class episode:
    s = None
    e = None
    name = None
    link = None
    path = None
    src = None
    status = 0
    cpos = 0
    len = None
    Mb = 1024*1024
    percentage = 0


    def __init__(self, s, e, name, link, path):
        self.s = s
        self.e = e
        self.name = name
        self.link = link
        self.path = path

        self.status = 0
        self.percentage = 0


    def get_dict(self):
        return self.__dict__

    def get_src(self, bot):
        self.src = bot.get_src_with_selenium_exp(self.link)

    def get_id(self):
        return str(self.s)+str(self.e)+self.name

    def watchdog(self, x):

        time.sleep(5)

        while 1:

            if x==None:
                print("\n----------------------------------------\nDOWNLOAD FINITO\n----------------------------------------\n")
                break

            self.percentage = x.get_percentage()
            print("th aggiorna: "+str(self.percentage))
            time.sleep(1)
            

        self.status = 4



    def start_fast(self, bot):

        
        src = bot.get_src_with_selenium(self.link)
        


        if src!=None:
            path = self.path+self.s+"x"+self.e+" "+self.name+".mp4"
            x = Parallel_Downloader(src, path)

            t = threading.Thread(target=self.watchdog, args=(x, ))
            t.daemon = True
            t.start()

            x.download(8)

    '''
    def start_normal(self, bot):

        if self.src==None:
            self.src = bot.get_src_with_selenium(self.link)
        
        if self.len==None:
            self.len = bot.get_length(self.src)
        

        if self.src!=None and self.len!=None:
            
            print("inizio download")
            nb = self.len - self.cpos
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0','Range': 'bytes='+str(self.cpos)+'-'+str(nb)}

            stream = bot.get_session().get(self.src, headers=headers, stream=True)

            print(stream.status_code)
            if stream.status_code==200 or stream.status_code==206:

                mode = "wb"
                if self.cpos>0:
                    mode = "ab"
                

                path = self.path+self.s+"x"+self.e+" "+self.name+".mp4"
                fw = open(path, mode)
                for chunk in stream.iter_content(4096):
                    self.cpos += len(chunk)

                    fw.write(chunk)
                    if self.status!=0:
                        break
                fw.close()


                if self.status==0:
                    self.status=4
                
                return True
        
        return False
        '''










class episodes:

    def __init__(self):
        self.episodes = {}

    def get_episodes(self):
        return self.episodes
    
    def add_esisodes_as_json_or_dict(self, x):

        if type(x).__name__ == "str":
            x = json.loads(x)
        

        for ele in x:
            epi = episode(**ele)
            id = epi.get_id()

            #aggiunge l'episodio solo se non già presente
            if not id in self.episodes:
                self.episodes[id] = epi

    
    def rem_episodes_by_id(self, ids):

        #molto permissiva
        if isinstance(ids, list):
            for id in ids:
                del self.episodes[id]
        else:
            del self.episodes[ids]

    def get_episode_by_status(self, x):
        for ele in self.episodes:

            t = self.episodes[ele]
            if t.get_dict()["status"] == x:
                return t

    def get_episodes_as_array_dict(self):
        ret = []
        for ele in self.episodes:

            t = self.episodes[ele]
            ret.append(t.get_dict())
        return ret




