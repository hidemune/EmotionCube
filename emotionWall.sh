#! /bin/bash

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

### Executing directory
cd /home/user/bin

### Switch to venv
source venv/bin/activate    

### For KILL :    pkill -f vertical_icon_text_launcher.py

### main screen savior
#exec ./venv/bin/python ./screensave.py "$@"
# exec ./venv/bin/python ./screensave.py "$@" > /dev/null 2>&1
#xwinwrap -fs -fdt -ni -b -nf -- \
#  ./venv/bin/python ./screensave.py --test

# Movie
#mpv --fs --no-border --ontop --no-osd-bar --quiet --geometry=100%x100% /home/user/Videos/#BOOT/HOS_BOOT.mp4 &
#PID_mpv=$!



# ScreenSaver - Wall
./venv/bin/python ./screensave.py --test $width $height &
PID_scr=$!

# 最大5秒間、ウィンドウが出てくるのを待つループ
#for i in {1..25}; do
#    WID=$(xdotool search --onlyvisible --pid "$PID_mpv" 2>/dev/null | head -n1)
#    if [[ -n "$WID" ]]; then
#        # ウィンドウを最前面に（raise）＋アクティブ化
#        xdotool windowraise "$WID"
#        xdotool windowactivate "$WID"
#        break
#    fi
#    sleep 0.2
#done

#wait $PID_mpv
# After Movie Luancher
#./venv/bin/python ./vertical_icon_text_launcher.py &
#PID_vl=$!

# ウィンドウが見つかったら下に送る
#for i in {1..25}; do
#    WID=$(xdotool search --any "　" 2>/dev/null | head -n1)
#    if [[ -n "$WID" ]]; then
#        echo "MyLauncher: below"
#        wmctrl -i -r "$WID" -b remove,above
#        wmctrl -i -r "$WID" -b add,below
#        #xdotool windowminimize "$WID"  # オプション：最小化
#        break
#    fi
#    sleep 0.2
#done

#wait "$PID_scr"
#pkill -f vertical_icon_text_launcher.py

#sleep 5
#xwininfo -name "Emotion Cube"
#window_id=0x5000005
#xprop -id $window_id -f _NET_WM_STATE 32a -set _NET_WM_STATE _NET_WM_STATE_BELOW

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
