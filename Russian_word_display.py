import re
import clipboard
import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import quote
import appex
import os
import sys
import console
import time
from threading import Thread
from texttable import Texttable
switch_other_transform = ['不定式：','副动词：','副动词：']
switch_table_length = [(13,13),(6.3,10,10),(6.575,6.575,6.575,6.575),(3.8,5.9,5.9,5.9,5.9)]
def foo():
    global wait_input_str
    wait_input_str=input ()
    return wait_input_str

def full_info(info):
    flag = 0  
    findemp = re.compile(r'">(.*?)</h2>')
    findbds = re.compile(r'不定式:(.*?)</h3>', re.DOTALL)
    findfdc = re.compile(r'副动词:(.*?)</h3>', re.DOTALL)
    findcontent = re.compile(r'left(.*?)</t')
    word_simplified_info = info.find(id="base0").find("div", {"class": "panel-body view"})
    first_word =re.findall(findemp,str(word_simplified_info.find("h2",{'class':'keyword'})))[0]
    first_word_expain = word_simplified_info.find("p",{'class':'exp'}).stripped_strings
    print(f'重音标记：',end = '')
    first_word = first_word.replace('</b>',',').replace('<b>',',')
    first_word_list = first_word.split(',')
    count = 0
    for item in first_word:
        if item == ',' and count == 0:
            console.set_color(1,0,0)
            count = abs(count-1)
        elif item == ',' and count == 1:
            console.set_color(1,1,1)
            count = abs(count-1)
        else:
            print(item,end='')
    print('')                
    print(f'单词解释：', end='')
    for item in first_word_expain:
        print(item,end = ' ')
    print('')
    print('---------------------------')
    
    try:
        
        detail_info = info.find(id="detail0").find('div', {'class': "panel-body"}).find('div', {
            'class': "subExpContainer"}).findAll('div', {'class': "row exp-item-sub"})
        print('详细解释：')
          
        for item in detail_info:
            detail_info_ = str(item.find('div', {'class': "subExp view"}).find('div', {'class': "exp"}))
            if detail_info_ != 'None':
                all_detail_info = detail_info_.replace('<br>', '\n').replace('<br/>', '\n').replace('<div class="exp">',
                                                                                                    '').replace(
                    '</div>', '')
                if all_detail_info != []:
                    print(all_detail_info.replace('~', '').lstrip())
                    flag = 1
                else:
                    print(detail_info_.replace('\r', '').replace('\n', '').lstrip().rstrip())
                break
                
    except Exception as e:
        pass
        

    try:
        print('----------------------------')
        print('----------------------------')
        print('变位变格：')
        all_other_info = info.find(id="grm0").find('div', {'class': "panel-body"}).find('div',
                                                                                             {'class': "grammardiv"})
        grim = all_other_info.findAll('table')
        
        other_info = re.findall(findbds, str(all_other_info))
        other_info_ = re.findall(findfdc, str(all_other_info))
        other_info = other_info + other_info_
        
        #print(all_other_info)
        #print(other_info)
        j = 0
        count = 0
        for item in grim:
            try:
                other_info_disp = other_info[count].replace('<b>', '').replace(
                    '</h2>', '').replace('</b>', '').replace('\n', '').replace('</p>','').replace('<strong>', '').replace('</strong>','').replace('<h3>', '\n').replace('<h2>', '\n')
                if len(other_info)==2 and j==1:
                    count = count-1
                    print(switch_other_transform[j])
                else:
                    print(switch_other_transform[j], end='')
                    print(other_info_disp.lstrip())
            except Exception:
                pass
            count = count+1
            if j < 3:
                tb = Texttable()
                
                j = j + 1
                table = item.findAll('tr')

                for i in range(len(table)):
                    if i == 0:
                        grim_title = re.findall(findcontent, str(table[i]))
                        grim_title = [
                            x.replace('<b>', '').replace('</b>', '').replace('>', '').replace('"', '').replace("'",
                                                                                                               '').replace(
                                '/', '').replace('br', '').replace('', '').replace('\\', '').replace('<', '') for x in
                            grim_title]
                        tb.set_cols_width(switch_table_length[len(grim_title)-2])
                        tb.add_row(grim_title)

                    else:
                        grim_content = re.findall(findcontent, str(table[i]))
                        grim_content = [
                            x.replace('<b>', '').replace('</b>', '').replace('>', '').replace('"', '').replace("'",
                                                                                                               '').replace(
                                '/', '').replace('br', '').replace('', '').replace('\\', '').replace('<', '') for x in
                            grim_content]
                        tb.add_row(grim_content)

                print(tb.draw())
    except Exception as e:
        pass
        # print(item)
        # print('------')
    return flag

def get_data(url,cur_word):
    findorigin = re.compile(r'<a href="#base1">(.*?)</a>，点击滚动到相应位置查看！')

    html = ask_url(url)
    bs = BeautifulSoup(html, "html.parser")
    info = bs.body
    origin_word = re.findall(findorigin, str(info))
    print('🌟',end='')
    print(cur_word)
    print('---------------------------')
    if origin_word != []:
        clipboard.set(origin_word[0])
        print('⚠️',end='')
        print(f'可能的单词原型：{origin_word[0]}')
        print('---------------------------')
    all_info = info.find(id="search").find(id="main").find(id="main-exp").find("div", {"class": "col-md-7"})
    return (full_info(all_info) or origin_word != [])


def ask_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    }
    req = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(req)
    return response
    
         
if __name__ == "__main__":
    global wait_input_str
    wait_input_str = ''
    console.set_color(1,1,1)
    
    try:
        #word = quote('ру**сский')
        word=quote(sys.argv[1])
    except Exception:
        print('小笨蛋没有复制分享单词，请在20秒内输入单词，或者输入1退出!')
        try:
            word = quote(appex.get_text())
        except Exception:
            thd = Thread(target=foo)
            thd.daemon= True
            thd.start()
            for num in range (20,-1,-1):
                if wait_input_str != '':
                    word = quote(wait_input_str)
                    console.clear()
                    break
                time.sleep(1)
                #sys.stdout.write('\r请在'+str(num)+'秒内作出反应,之后程序会自动关闭 \r')
                #sys.stdout.flush()
                if num==0 or wait_input_str=='1':
                    console.clear()
                    sys.exit(0)
    #print(sys.argv[1])
    #去除特殊字符，只保留汉子，字母、数字

    flag = 0
    for i in range(3):
        try:
            flag = get_data(f'https://w.qianyix.com/index.php?q={word}',urllib.parse.unquote(word))
            break
        except Exception as e:
            time.sleep(0.5)
            continue    
            
    if flag == 0:
        try:
            console.clear()
            word = urllib.parse.unquote(word)
            print(f'📋复制到的单词：{word}')
            word =re.sub('[^\u0400-\u052f]+','',word)
            print(f'♻️转换后得到字符：{word}')
            word = quote(word)
            flag = get_data(f'https://w.qianyix.com/index.php?q={word}',urllib.parse.unquote(word))
        except Exception as e:
            pass
    if flag == 0:
        console.clear()
        print(f'此单词{urllib.parse.unquote(word)}无法获取，联系男朋友获取帮助')
        print('小笨蛋请在20秒内输入单词，或者输入1退出!')
        try:
            word = quote(appex.get_text())
        except Exception:
            thd = Thread(target=foo)
            thd.daemon= True
            thd.start()
            for num in range (20,-1,-1):
                if wait_input_str != '':
                    word = quote(wait_input_str)
                    console.clear()
                    break
                time.sleep(1)
                #sys.stdout.write('\r请在'+str(num)+'秒内作出反应,之后程序会自动关闭 \r')
                #sys.stdout.flush()
                if num==0 or wait_input_str=='1':
                    console.clear()
                    sys.exit(0)
        for i in range(3):
            try:
                flag = get_data(f'https://w.qianyix.com/index.php?q={word}',urllib.parse.unquote(word))
                break
            except Exception as e:
                time.sleep(0.5)
                continue  
