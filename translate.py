from googletrans import Translator
from time import sleep
import os as os
from progress.bar import ShadyBar
from random import random
import threading
import json
from pick import pick

origin_name = 'a.txt'  # 源文件名称
origin_path = './'+origin_name  # 源文件地址
target_path_ios = './iOS/'  # 生成文件目录
target_path_android = './安卓/'
target_path_web = './web/'
choose = None
language = {
'印尼语': 'id',
'意大利语': 'it',
'葡萄牙语-巴西': 'pt',
'俄语': 'ru',
'阿拉伯语': 'ar',
'德语': 'de',
'英语': 'en',
'西班牙语': 'es',
'越南语': 'vi',
'繁体中文': 'zh-TW',
'波斯语': 'fa',
'法语': 'fr'
}
title = '\n将要翻译的文本命名为'+origin_name +'与该程序保存在同一目录下(web直接选择即可），然后选择要输出的平台:'
options = ['iOS', 'Android', 'Web']
option, choose = pick(options, title)

random_language_list = ['fa', 'ar', 'de', 'fr', 'pt']
random_text_list = ['落叶的一生只是为了归根吗', 'What a wonderful day! ',
    'Domani andrà meglio', '长路漫漫，唯剑作伴', '飞湍瀑流争喧豗,砯崖转石万壑雷']


def request(line_str, language_key, translator):
  request_str = line_str
  try:
    request_str = translator.translate(line_str, dest=language_key).text
  except BaseException:
    print('\n'+'请求超时，正在重试...')
  return request_str


def getrandom():
  randomNum = int(random()*100)
  while randomNum > min(len(random_language_list), len(random_text_list))-1:
    randomNum = int(random()*100)
  return randomNum


def translation(language_key, language_value, path):
    translator = Translator()
    file = open(origin_path)
    lines = file.readlines()
    file.close()
    result = ''
    origin = []
    target = []
    # bar = ShadyBar('\n总进度', max=len(lines))
    for line in lines:
      origin_str = line.split('\n')[0]
      target_str = request(line.split('\n')[0], language_value, translator)
      times = 0  # 重新尝试的次数
      if language_value != 'zh-TW':
        while origin_str == target_str:  # 翻译不成功时的处理
          sleep(times*2)
          random_text = random_text_list[getrandom()]
          request(random_text, random_language_list[getrandom()], translator)
          print(language_key+' 向google发动'+str(times)+'次吟唱:'+random_text)
          sleep(times*2)
          target_str = request(line.split('\n')[0], language_value, translator)
          times += 1
      origin.append(origin_str)
      target.append(target_str)
    for i in range(len(origin)):
      if(path == target_path_ios):
        result = result+'"'+origin[i]+'"='+'"'+target[i]+'";\n'
      elif(path == target_path_android):
        result = result+origin[i]+'='+target[i]+'\n'
    target_file = open(path+language_key+'.txt', 'w+')
    target_file.write(result)
    print(language_key+':完成')
    target_file.close()
    file.close()

def tranlate_web(language_value, path):
    translator = Translator()
    file = open('./target.json')
    json_str=file.read()
    json_obj=json.loads(json_str)
    target_obj={}
    times = 0  # 重新尝试的次数
    for key,value in  json_obj.items():
      target_value=request(value, language_value, translator)
      if language_value != 'zh-TW':
        while value == target_value:  # 翻译不成功时的处理
          sleep(times*2)
          random_text = random_text_list[getrandom()]
          request(random_text, random_language_list[getrandom()], translator)
          print(' 向google发动'+str(times)+'次吟唱:'+random_text)
          sleep(times*2)
          target_value=request(value, language_value, translator)
          times += 1
      target_obj[key]=target_value
    file_str=json.dumps(target_obj, ensure_ascii=False)
    target_file = open(path+language_value+'.json', 'w+')
    target_file.write(file_str)
    target_file.close()
    

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter, key, value, path):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.key = key
        self.value = value
        self.path = path

    def run(self):
        # print ("开始线程：" + self.name)
        if(choose==2):
          tranlate_web(self.value, self.path)
        else:
          translation(self.key, self.value, self.path)
        # print ("退出线程：" + self.name)


def trans():
  if not os.path.exists(origin_path) and choose in (0, 1):
    print('error:找不到源文件，请检查文件名是否正确')
    return
  if not os.path.exists('./target.json') and choose == 2:
    print('error:找不到源文件，请检查文件名是否正确')
    return
  if choose == 0:
    path = target_path_ios
  elif choose == 1:
    path = target_path_android
  elif choose == 2:
    path = target_path_web
  if not os.path.exists(path):
    os.makedirs(path)
  print('翻译中...')
  threads = []
  i = 0
  for key in language.keys():
    thread = myThread(i, "Thread-"+str(i), i, key, language[key], path)
    threads.append(thread)
    i += 1
  for thread in threads:
    thread.start()
  for thread in threads:
    thread.join()
  print('\n翻译完成✓\n'+'保存在'+path+'目录下')


trans() #开始运行
