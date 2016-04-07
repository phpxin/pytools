# -*- coding: utf-8 -*-
from Tix import COLUMN
import Tkinter
from numbers import Number
import numbers
import string

'''
 多线程表单提交
'''


url = ''
kv_map = dict()

def tools_trim(prestr, chars):
    '''
    切除首尾指定字符
    '''
    if len(chars)<=0 or len(prestr)<=0 :
        return prestr 
    
    darr = tuple(chars)
    prelist = list(prestr)
    for i in range(len(prelist)) :
        
        if darr.count(prelist[i]) > 0 :
            prelist[i] = ''
            pass
        else :
            break
        pass
    
    _a = range(len(prelist))
    _a.reverse()
    for i in _a :
        if darr.count(prelist[i]) > 0 :
            prelist[i] = ''
            pass
        else :
            break
        pass

    return ''.join(prelist)

# 定义样式宽度
win_row = 0
txt_area_width = 80
input_area_width = 70
win_size = '600x600'

ui = Tkinter.Tk()
ui.title("hello tk")
ui.geometry(win_size)

#第一行
url_lab = Tkinter.Label(ui, text="url: ", state='disable')
url_lab.grid(row=win_row, column=0)

url_ta = Tkinter.Text(ui, width=input_area_width, height=1)
url_ta.grid(row=win_row, column=1)
url_ta.insert('0.0', 'http://')

#第二行
win_row+=1

txt = Tkinter.Text(ui, width=txt_area_width)
txt.grid(row=win_row, column=0, columnspan=2, padx=18)


#第三行
win_row+=1

lab = Tkinter.Label(ui, text="key: ", state='disable')
lab.grid(row=win_row, column=0)
inputEKey = ''
inputkey = Tkinter.Text(ui, height=1, width=input_area_width, yscrollcommand=True)
inputkey.grid(row=win_row, column=1)

#第三行
win_row+=1

val_lab = Tkinter.Label(ui, text="value: ", state='disable')
val_lab.grid(row=win_row, column=0)
inputEVal = ''
inputval = Tkinter.Text(ui, height=1, width=input_area_width, yscrollcommand=True)
inputval.grid(row=win_row, column=1)

#第四行
win_row+=1

def eachMap(mapdef):
    global txt
    print '---> begin'
    keys = dict.iterkeys(mapdef)
    #i = 0
    pre_text = '' ;
    for k in keys :
        _ss = k + ' = ' + mapdef[k]
        print _ss
        '''
        txt.delete('0.0', Tkinter.END)
        pos = '%d' %i+'.0'
        txt.insert(Tkinter.CURRENT, _ss+'\n')
        print pos
        i+=1
        '''
        pre_text += _ss + '\n'
        pass
    txt.delete('0.0', Tkinter.END)
    txt.insert('0.0', pre_text)
    return

def btnOnAddParam():
    global txt
    global inputkey
    global inputval
    _strkey = inputkey.get('0.0', Tkinter.END)
    _strkey = tools_trim(_strkey,'\n\t ')
    _strval = inputval.get('0.0', Tkinter.END)
    _strval = tools_trim(_strval,'\n\t ')
    if _strkey == '' :
        return
    kv_map[_strkey] = _strval;
    inputkey.delete('0.0', Tkinter.END)
    inputval.delete('0.0', Tkinter.END)
    eachMap(kv_map)
    return

def btnOnExec():
    global url
    url = url_ta.get('0.0', Tkinter.END)
    url = tools_trim(url, '\n\t ')
    print url
    return

def btnOnClean():
    global kv_map
    kv_map = dict()
    eachMap(kv_map)
    return

btn_frame = Tkinter.Frame(ui)
btn_frame.grid(row=win_row, column=0, columnspan=2)

btn_add = Tkinter.Button(btn_frame, text='添加POST参数', command=btnOnAddParam )
btn_add.grid(row=0, column=0, padx=2)
#btn.pack()
#btn.grid(row=win_row, column=0)

btn_clean = Tkinter.Button(btn_frame, text='清空post参数', command=btnOnClean)
btn_clean.grid(row=0, column=1, padx=2)

btn_post = Tkinter.Button(btn_frame, text='执行', command=btnOnExec )
btn_post.grid(row=0, column=2, padx=2)
#btn2.pack()
#btn2.grid(row=win_row, column=1)


Tkinter.mainloop() # open windows
