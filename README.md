# translate
### 一款调用googletrans接口实现的自动化翻译工具，语言库和输出规则可自行添加修改

使用方法：
 <br/> 将需要翻译的文本命名为a.txt与该程序保存在同一目录下，运行该程序，选择'预设'即可。
 <br/> 该工具会逐行读取原文本进行翻译并逐行输出，翻译后的结果存放在按目标语言命名的对应的txt文件中

所需运行库：
 <br/>googletrans
 <br/>pick
 <br/>已附在requirements.txt中，可使用 pip install -r requirements.txt 命令批量安装


#### 国内使用googletrans超时的问题： 
只需修改源码，把py_translator中的
 gtoken.py
 urls.py
 client.py
3个文件中的 translate.google.com 修改为 translate.google.cn即可
