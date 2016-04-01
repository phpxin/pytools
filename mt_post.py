# -*- coding: utf-8 -*-
# from Tkinter import Tk
# from Tkinter import Button
import Tkinter
#import ttk
'''
 多线程表单提交
'''

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

#第二行
win_row+=1

txt = Tkinter.Text(ui, width=txt_area_width)
txt.grid(row=win_row, column=0, columnspan=2)




#第三行
win_row+=1

lab = Tkinter.Label(ui, text="key: ", state='disable')
lab.grid(row=win_row, column=0)

inputkey = Tkinter.Text(ui, height=1, width=input_area_width, yscrollcommand=True)
inputkey.grid(row=win_row, column=1)

#第三行
win_row+=1

val_lab = Tkinter.Label(ui, text="value: ", state='disable')
val_lab.grid(row=win_row, column=0)

inputval = Tkinter.Text(ui, height=1, width=input_area_width, yscrollcommand=True)
inputval.grid(row=win_row, column=1)

#第四行
win_row+=1

def btnOnclick():
    global txt
    global inputkey
    global inputval
    _strkey = inputkey.get('0.0')
    print('call del line key is '+_strkey)
    txt.delete('0.0')

btn = Tkinter.Button(ui, text='添加POST参数', command=btnOnclick )
btn.grid(row=win_row, column=0)

btn2 = Tkinter.Button(ui, text='备用')
btn2.grid(row=win_row, column=1)


Tkinter.mainloop() # open windows
