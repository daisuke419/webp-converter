import os
import glob
from tkinter import ttk, filedialog
import tkinter
from PIL import Image

# フォルダ選択処理
def folderOpenCommand() :
    filepath = filedialog.askdirectory(title=u'フォルダ選択')
    print(filepath)

    onFolderOpened(filepath)

# フォルダ選択完了後の処理
def onFolderOpened(filepath) :

    if (filepath != '') :
        textbox.insert(1, filepath)
        insertTable(glob.iglob(filepath + '/*'))


# テーブルにテキスト挿入
def insertTable(file_list) :
    #print(table.get_children())
    
    targets = getTagetFiles(file_list)
    
    # テーブルのクリア
    for child in table.get_children() : table.delete(child)

    for file in targets :
        table.insert('', 'end', tag=0, values=[os.path.basename(file), '未変換', file])


# 対象ファイルの取得
def getTagetFiles(files) :
    ext_list = ['.jpg', '.jpeg', '.png', '.gif']
    out_list = []

    for file in files :
        ext = os.path.splitext(file)[1]
        
        if (ext in ext_list) :
            out_list.append(file)
    
    return out_list

# 変換処理実行
def commandConvert() :

    if os.path.exists('./output') == False : os.mkdir('output')

    for child in table.get_children() :
        item = table.item(child, option=u'values')
        print(item)
        table.set(child, column=2, value=u'変換中')
        convert(item[2], 'output/')
        table.set(child, column=2, value=u'完了')
        
    

#
#
#
def convert(file_path, out_dir) :

    image = Image.open(file_path)
    image.save(out_dir + os.path.split(file_path)[1].split('.')[0] + '.webp', 'webp')


def createSettingWindow() :
    setting = tkinter.Tk()
    setting.title(u'設定画面')
    setting.mainloop()


#input_dir = StringVar()

#--------------------------------------------------
root = tkinter.Tk()
root.title(u'Webp画像変換ツール')
root.geometry('640x480')
root.columnconfigure(0)
root.rowconfigure(0)

#--------------------------------------------------
menu = tkinter.Menu()
menu_files = tkinter.Menu(menu, tearoff=False)
menu_tools = tkinter.Menu(menu, tearoff=False)
menu_help = tkinter.Menu(menu, tearoff=False)

#menu_files.add_command(label=u'ファイルを開く')
menu_files.add_command(label=u'フォルダを開く', command=folderOpenCommand)
menu_files.add_separator()
menu_files.add_command(label=u'終了', command=root.quit)

menu_tools.add_command(label=u'実行', command=commandConvert)
menu_tools.add_command(label=u'設定', command=createSettingWindow)

menu_help.add_command(label=u'バージョン')
menu_help.add_command(label=u'ヘルプ')

menu.add_cascade(menu=menu_files, label=u'ファイル')
menu.add_cascade(menu=menu_tools, label=u'ツール')
menu.add_cascade(menu=menu_help, label=u'ヘルプ')

#--------------------------------------------------
frame = ttk.Frame(root, padding=10)
frame.grid(sticky=tkinter.NW, padx=5, pady=10)

textbox = ttk.Entry(frame, width='64')
button = ttk.Button(frame, text=u'フォルダ読込', command=folderOpenCommand)
submit = ttk.Button(frame, text=u'変換', command=commandConvert)
textarea = tkinter.Text(frame, width=64, height=20)
table = ttk.Treeview(frame, show='headings', columns=(1, 2, 3), displaycolumns=(1, 2))

#table['columns'] = (1, 2, 3)
#table['displaycolumns'] = (1, 2)
#table['show'] = 'headings'
table.column(1, width=200)
table.column(2, width=150)
table.column(3)
table.heading(1, text=u'ファイル名')
table.heading(2, text=u'ステータス')
vbar = ttk.Scrollbar(frame, orient='vertical', command=table.yview)
table.configure(yscrollcommand=vbar.set)


textbox.grid(row=0, column=0, padx=5, pady=5, sticky=tkinter.NW)
button.grid(row=0, column=1, padx=5, pady=5, sticky=tkinter.NE)
table.grid(row=1, column=0, padx=5, pady=5, sticky=tkinter.NW)
submit.grid(row=1, column=1, padx=5, pady=5, sticky=tkinter.SE)

root['menu'] = menu
root.mainloop()



