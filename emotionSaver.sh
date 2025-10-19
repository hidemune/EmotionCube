#! /bin/bash

### Executing directory
cd /home/user/bin

# 現在のアクティブなスクリーンの解像度を取得
resolution=$(xrandr | grep '*' | awk '{print $1}')
width=$(echo $resolution | cut -d'x' -f1)
height=$(echo $resolution | cut -d'x' -f2)

### Run it first in the folder
# python3 -m venv venv       

### Preparing Python
#   sudo apt install pip
#   pip install pygame PyOpenGL numpy
#   pip install PyOpenGL_accelerate
#   pip install python-xlib

### Switch to venv
source venv/bin/activate    

### main screen savior
exec ./venv/bin/python ./screensave.py "$@" $width $height
# exec ./venv/bin/python ./screensave.py "$@" > /dev/null 2>&1


### Linux の、 xscreensaver に追加したい場合
#
#   nano ~/.xscreensaver
#   ...
#   最後の方に、以下を追加 / Add the following to the end:
#   
#   - GL:           "EmotionSaver"  /home/user/bin/emotionSaver.sh --root            \n\
#
#

### Windows で、.exe にした後に拡張子を .src に変更して
#   
#   pip install pyinstaller
#   
#   pyinstaller --noconsole --onefile yourscript.py
#   
#   出力先に dist/yourscript.exe ができます
#   
#   mv yourscript.exe yourscript.scr
#   
#   C:\Windows または C:\Windows\System32 に配置
#   
#   すると、Windowsのスクリーンセーバー設定画面に表示されます
#   管理者権限が必要な場合あり
