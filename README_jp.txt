━━━━━━━━━━━━━━━━━━━━━━
かっちょいいスクリーンセーバーの新作について
━━━━━━━━━━━━━━━━━━━━━━

【作った人】
    おれ

【作り方】
    ChatGPTでざっくりやり方を聞いて、バグでハマったらGeminiで解決した

【豆知識】
    WindowsでExeにした後に、拡張子を「.scr」にしてどこかに置けば、
    Win11でもスクリーンセーバーにできるらしいぞ。

【具体的な手順】
    Ubuntuでのやり方は「emotionSaver.sh」に書いた通り。

━━━━━━━━━━━━━━━━━━━━━━━━━
### Run it first in the folder
#   python3 -m venv venv

### Preparing Python
#   sudo apt install pip
#   pip install pygame PyOpenGL numpy
#   pip install PyOpenGL_accelerate
#   pip install python-xlib
#   sudo apt install freeglut3-dev
━━━━━━━━━━━━━━━━━━━━━━━━━

### Linux の、 xscreensaver に追加したい場合
#
#   nano ~/.xscreensaver
#   ...
#   最後の方に、以下を追加 / Add the following to the end:
#
#   - GL:           "EmotionSaver"  /home/user/bin/emotion.sh --root            \n\
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
━━━━━━━━━━━━━━━━━━━━━━━━━

【その他】
    動かして感想を教えてね！
