import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import csv
import os, sys
import signal
# Xlibはウィンドウのスタッキング操作には不要なため、ここではコメントアウト
# from Xlib.display import Display
# from Xlib import X

from Xlib import display, X, protocol

def remove_window_titles_and_icon():
    d = display.Display()
    win_id = pygame.display.get_wm_info()["window"]
    win = d.create_resource_object('window', win_id)

    for prop in ['_NET_WM_NAME', 'WM_NAME', 'WM_ICON_NAME']:
        atom = d.intern_atom(prop)
        win.delete_property(atom)

    d.flush()

def set_transparent_icon():
    icon_surface = pygame.Surface((1, 1), pygame.SRCALPHA)
    icon_surface.fill((0, 0, 0, 0))  # 完全に透明
    pygame.display.set_icon(icon_surface)

def handle_signal(sig, frame):
    print(f"[INFO] Received signal {sig}, exiting.")
    pygame.quit()
    sys.exit(0)

# SIGTERM（kill や pkill）と SIGINT（Ctrl+C）を捕捉
signal.signal(signal.SIGTERM, handle_signal)
signal.signal(signal.SIGINT, handle_signal)

def lower_window():
    d = display.Display()
    win_id = pygame.display.get_wm_info()["window"]
    window = d.create_resource_object('window', win_id)
    window.configure(stack_mode=X.Below)
    d.sync()

# PygameウィンドウのWM_CLASSをXScreenSaverとして設定
# これにより、XScreenSaverがこのウィンドウを適切に扱うことができます。
os.environ['SDL_VIDEO_X11_WMCLASS'] = 'XScreenSaver'

# XScreenSaverから渡されるウィンドウIDを取得
xscreensaver_window_id = os.getenv('XSCREENSAVER_WINDOW')

winid_hex = None
winid_dec = None
app_mode = 0
fullscreen = False
root_mode = False

WIDTH = int(sys.argv[2]) if len(sys.argv) > 2 else 1920
HEIGHT = int(sys.argv[3]) if len(sys.argv) > 3 else 1080

# --- SDL_WINDOWIDを設定 ---
# XScreenSaverによって起動される場合、--window-idが渡されます
if '--window-id' in sys.argv:
    idx = sys.argv.index('--window-id')
    winid_hex = sys.argv[idx + 1]
    winid_dec = int(winid_hex, 16)
    # Pygameに既存のXウィンドウに描画するよう指示
    os.environ['SDL_WINDOWID'] = str(winid_dec)
    print(f"[INFO] SDL_WINDOWID set to {winid_dec} (hex: {winid_hex})")
    fullscreen = False # XScreenSaverの子ウィンドウとして動作
elif '--test' in sys.argv:
    print("[INFO] Running in test mode.")
    fullscreen = False # 設定画面は通常フルスクリーンではない
    root_mode = True
elif '--settings' in sys.argv:
    print("[INFO] Running in settings screen mode.")
    fullscreen = False # 設定画面は通常フルスクリーンではない
    app_mode = 1 # 設定画面モード
else:
    print(f"[INFO] No --window-id provided, running in fullscreen mode ({sys.argv}).")
    fullscreen = True  # OpenGL 全画面 (XScreenSaver以外で直接実行する場合)

def display_settings_screen(screen):
    """
    設定画面にテキストを表示します。
    Args:
        screen (pygame.Surface): Pygameの表示サーフェス。
    """
    # フォントの初期化 (必要であれば、この関数内で新しく作成することも可能)
    # ただし、main関数で一度作成したfontオブジェクトを引数で渡すか、グローバル変数にするのが一般的です。
    font = pygame.font.SysFont("Arial", 32) # 例: 設定画面用に少し大きめのフォント

    # 画面をクリア（真っ黒に）
    screen.fill((0, 0, 0))

    # --- テキストのレンダリングと配置 ---
    # タイトル
    title_text = font.render("Settings", True, (255, 255, 255)) # 白いテキスト
    # 画面中央上部に配置
    title_rect = title_text.get_rect(center=(screen.get_width() / 2, 50))
    screen.blit(title_text, title_rect)

    # オプション1
    option1_text = font.render("Option 1: Toggle Feature", True, (0, 255, 0)) # 緑色のテキスト
    option1_rect = option1_text.get_rect(topleft=(50, 150))
    screen.blit(option1_text, option1_rect)

    # オプション2
    option2_text = font.render("Option 2: Adjust Value [  50  ]", True, (0, 200, 255)) # 水色のテキスト
    option2_rect = option2_text.get_rect(topleft=(50, 200))
    screen.blit(option2_text, option2_rect)

    # 戻る指示
    back_text = font.render("Press ESC to return", True, (255, 255, 0)) # 黄色のテキスト
    back_rect = back_text.get_rect(center=(screen.get_width() / 2, screen.get_height() - 50))
    screen.blit(back_text, back_rect)

    # 画面を更新
    pygame.display.flip()

    # イベントループ（ユーザー入力を待つ）
    running_settings = True
    while running_settings:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running_settings = False # ESCで設定画面を終了
                # 他の設定変更ロジックをここに追加
                # 例: if event.key == pygame.K_1: # オプション1をトグル
                #        # ...
        pygame.time.Clock().tick(30) # CPU使用率を抑えるためフレームレートを制限

# pygame画面の初期化
def init_display(window_id):
    pygame.init()
    glutInit(sys.argv) # glutInitは通常はメインループ開始前に一度だけ呼ぶのが推奨されます

    if fullscreen:
        screen = pygame.display.set_mode((0, 0), FULLSCREEN | DOUBLEBUF | OPENGL)
        print("[INFO] Running in fullscreen OpenGL mode. window ID: {window_id}")
    elif root_mode:
        #screen = pygame.display.set_mode((1312, 768), DOUBLEBUF | OPENGL) 
        #screen = pygame.display.set_mode((1920, 1080), NOFRAME | DOUBLEBUF | OPENGL) 
        #screen = pygame.display.set_mode((3840, 2160), NOFRAME | DOUBLEBUF | OPENGL) 
        # 2160 - 40 = 2120
        screen = pygame.display.set_mode((WIDTH, HEIGHT - 40), NOFRAME | DOUBLEBUF | OPENGL) 
        lower_window()
        print(f"[INFO] Running as ROOT MODE")
    else:
        # XScreenSaverの子ウィンドウとして動作する場合、サイズはXScreenSaverが決定
        #screen = pygame.display.set_mode((1, 1), DOUBLEBUF | OPENGL) 
        screen = None
        print(f"[INFO] Running as XScreenSaver program on window ID: {window_id}")

    if app_mode == 0:
        info = pygame.display.Info()
        width, height = info.current_w, info.current_h
        if height == 0: height = 1 
        glViewport(0, 0, width, height) 

        # OpenGL初期化後の最初の描画とイベント待機
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        pygame.display.flip() # 最初のフレームをレンダリングして表示

    if app_mode == 0: # スクリーンセーバーモードでは非表示
        pygame.display.flip() # 最初のフレームをレンダリングして表示
        if fullscreen:
            pygame.mouse.set_visible(False)
    else: # 設定画面やプレビューモードでは表示
        pygame.mouse.set_visible(True)
    # カーソルを非表示にする試みをここで追加
    # カーソル表示はモードによって切り替える
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < 3000: # 3秒間待機しつつイベント処理
        for event in pygame.event.get():
            # XScreenSaverのプレビューモードでは、ユーザー入力で終了する可能性があるため、
            # ここでは終了させないようにします。
            # ただし、もし強制終了させるイベントがあれば、ここで処理することも可能。
            pass 
        pygame.time.wait(10) # 短い間隔でポーリング
    
    print(f"[INFO] Initial {pygame.time.get_ticks() - start_time}ms wait completed.")

    return screen

# raise_window_to_top関数はXScreenSaverによって管理されるため、ここでは削除します
# from Xlib import X, display, protocol
# def raise_window_to_top():
#     d = display.Display()
#     root = d.screen().root
#     win_id = pygame.display.get_wm_info()["window"]
#     window = d.create_resource_object('window', win_id)
#     NET_WM_STATE = d.intern_atom('_NET_WM_STATE')
#     NET_WM_STATE_ABOVE = d.intern_atom('_NET_WM_STATE_ABOVE')
#     ev = protocol.event.ClientMessage(
#         window = window,
#         client_type = NET_WM_STATE,
#         data = (32, [1, NET_WM_STATE_ABOVE, 0, 0, 0])
#     )
#     root.send_event(ev, event_mask=X.SubstructureRedirectMask | X.SubstructureNotifyMask)
#     d.flush()


# --- 感情データの読み込み ---
def load_emotions():
    points = []
    # emotion.csv ファイルが存在しない場合は警告を出力して終了
    if not os.path.exists('emotion.csv'):
        print("[ERROR] 'emotion.csv' not found. Please create the file.")
        sys.exit(1) # スクリプトを終了
        
    with open('emotion.csv', mode='r', encoding='utf-8', newline='') as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line or '\t' not in line:
                continue  # 空行や区切りなし行はスキップ

            parts = line.split('\t')
            if len(parts) < 4:
                continue  # 少なすぎる行

            try:
                # 文字列＋3軸（先頭以外はfloatで確認）
                word = parts[0]
                x = float(parts[1])
                y = float(parts[2])
                z = - float(parts[3]) # z軸の反転は元のコードの通り
                points.append((x, y, z))
            except ValueError:
                # 数値でないならスキップし、エラーメッセージは表示しない (大量に出る可能性があるため)
                continue
    return points
    

# --- 感情ポイントをプロット ---
def draw_points(points_np, colors):
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)

    glPointSize(1) # ポイントサイズを小さく設定

    glVertexPointer(3, GL_FLOAT, 0, points_np)
    glColorPointer(3, GL_FLOAT, 0, colors)

    glDrawArrays(GL_POINTS, 0, len(points_np))

    glDisableClientState(GL_COLOR_ARRAY)
    glDisableClientState(GL_VERTEX_ARRAY)


def should_exit(event, initial_mouse_pos):
    # ESCキーで終了
    if event.type == KEYDOWN and event.key == K_ESCAPE:
        print("[INFO] ESC key pressed, exiting.")
        return True
    # マウスクリックで終了
    if not (root_mode):
        if event.type in (MOUSEBUTTONDOWN, MOUSEBUTTONUP):
            print("[INFO] Mouse clicked, exiting.")
            return True
    # マウス移動で終了 (少し動いたら)
    if not (root_mode):
        if event.type == MOUSEMOTION:
            x, y = event.pos
            dx = abs(x - initial_mouse_pos[0])
            dy = abs(y - initial_mouse_pos[1])
            if dx > 5 or dy > 5:  # 少し動いたら終了
                print("[INFO] Mouse moved, exiting.")
                return True
    return False

def draw_label_gl(text, x, y, z, color):
    # テキストの色を設定
    glColor3f(*color)
    # テキストの位置を設定
    glRasterPos3f(x, y, z)
    # 文字列の各文字を描画
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

def get_distance_to_camera_rotated(x, y, z, angle_deg, axis):
    angle_rad = np.radians(angle_deg)
    axis = np.array(axis, dtype=np.float64)
    # 軸がゼロベクトルでないことを確認
    if np.linalg.norm(axis) == 0:
        return np.inf # 無限大を返し、距離計算を避ける
    axis = axis / np.linalg.norm(axis)  # 正規化
    ux, uy, uz = axis

    # Rodriguesの回転公式による回転行列
    cos_a = np.cos(angle_rad)
    sin_a = np.sin(angle_rad)
    one_minus_cos = 1 - cos_a
    R = np.array([
        [cos_a + ux**2 * one_minus_cos,
         ux*uy*one_minus_cos - uz*sin_a,
         ux*uz*one_minus_cos + uy*sin_a],

        [uy*ux*one_minus_cos + uz*sin_a,
         cos_a + uy**2 * one_minus_cos,
         uy*uz*one_minus_cos - ux*sin_a],

        [uz*ux*one_minus_cos - uy*sin_a,
         uz*uy*one_minus_cos + ux*sin_a,
         cos_a + uz**2 * one_minus_cos]
    ])

    pos = np.array([x, y, z])
    rotated = R @ pos
    # カメラは原点にいる想定で、オブジェクトがカメラから-5の位置にあると仮定
    translated = rotated + np.array([0, 0, -5])
    dist = np.linalg.norm(translated)
    return dist


labels = [
    ("Joy", 1, 1, 1),
    ("Trust", 1, -1, 1),
    ("Sadness", -1, -1, 1),
    ("Disgust", -1, 1, 1),
    ("Fear", 1, -1, -1),
    ("Anticipation", 1, 1, -1),
    ("Anger", -1, 1, -1),
    ("Surprise", -1, -1, -1),
    ("Optimism", 1, 1, 0),
    ("Submission", 1, -1, 0),
    ("Contempt", -1, 1, 0),
    ("Disapproval", -1, -1, 0),
    ("Aggressiveness", 0, 1, 0), # スペル修正
    ("Awe", 0, -1, 0),
    ("Remorse", -1, 0, 0),
    ("Love", 1, 0, 0),
]

# --- メイン処理 ---
def main():
    # 感情データファイルを事前に作成してください (例: emotion.csv)
    # CSVの内容例:
    # Word1	1.0	0.5	-0.2
    # Word2	-0.8	0.1	0.7
    # ...
    # 'emotion.csv'ファイルがない場合は、プログラムがエラーで終了します。
    
    points = load_emotions()
    if not points:
        print("[ERROR] No emotion data loaded. Exiting.")
        pygame.quit()
        sys.exit(1)

    points_np = np.array(points, dtype=np.float32)
    # ポイントの色は、元のコードの通り、座標に基づいて計算
    colors = np.array([
        [(y + 1) / 2, (x + 1) / 2, (z + 1) / 2] for (x, y, z) in points_np
    ], dtype=np.float32)
    
    
    init_display(winid_dec) # winid_decはinit_display内部で処理される
    
    pygame.display.set_caption("　")
    set_transparent_icon()
    #remove_window_titles_and_icon()
    if fullscreen:
        pygame.mouse.set_visible(False) # マウスカーソルを非表示に
    
    if app_mode == 0 or app_mode == 2:
        # 現在のディスプレイ情報を取得し、アスペクト比を計算
        info = pygame.display.Info()
        width, height = info.current_w, info.current_h
        if height == 0: # 高さ0の分割を避ける
            height = 1 
        aspect = width / height 
        # OpenGLの透視投影を設定
        gluPerspective(45, aspect, 0.1, 30.0)
        # カメラをZ軸方向に移動
        glTranslatef(0.0, 0.0, -5)
        # 深度テストを有効にする (3Dオブジェクトの重なりを正しく描画するため)
        glEnable(GL_DEPTH_TEST)

    angle = 0
    clock = pygame.time.Clock()

    # マウスの初期位置を取得 (終了条件判定に使用)
    initial_mouse_pos = pygame.mouse.get_pos()

    while True:
        if root_mode:
            lower_window()
        # Xlibによるウィンドウ操作はXScreenSaverの子ウィンドウでは不要なため削除
        # ウィンドウのスタッキングはXScreenSaverが管理します。
        # PygameのXID取得も、ここでは特に必要ないため削除。
        
        for event in pygame.event.get():
            if should_exit(event, initial_mouse_pos):
                pygame.mouse.set_visible(True) # マウスカーソルを再表示
                pygame.quit()
                sys.exit()


        if app_mode == 0: # スクリーンセーバーモードのイベント処理
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # カラーバッファと深度バッファをクリア
            glPushMatrix() # 現在の行列を保存
            glRotatef(angle, 0.486, 0.726, 0) # 回転軸と角度を設定

            draw_points(points_np, colors) # 感情ポイントを描画

            # --- ラベルを描画（カメラからの距離に応じて明るさを調整） ---
            distances = []
            for (_, x, y, z) in labels:
                dist = get_distance_to_camera_rotated(x, y, z, angle, (0.486, 0.726, 0))
                distances.append(dist)
            
            # 距離に基づいて明るさを正規化
            if distances: # リストが空でないことを確認
                min_dist = min(distances)
                max_dist = max(distances)
                dist_range = max_dist - min_dist
                
                for (text, x, y, z), dist in zip(labels, distances):
                    # 距離が0の場合（dist_rangeが0の場合）のゼロ除算を防ぐ
                    if dist_range == 0:
                        norm = 1.0
                    else:
                        norm = 1.0 - (dist - min_dist) / dist_range
                    
                    brightness = 0.1 + 0.8 * norm # 明るさを調整 (0.1から0.9の範囲)
                    draw_label_gl(text, x, y, z, (brightness, brightness, brightness))
            
            glPopMatrix() # 保存した行列を復元 (回転の影響を局所化)
            
            # ----
            # --- Draw 2D Overlay (Provider Name) ---
            glMatrixMode(GL_PROJECTION) # Switch to projection matrix mode
            glPushMatrix()              # Save the current 3D projection matrix
            glLoadIdentity()            # Reset projection matrix

            # Set up an orthographic projection for 2D drawing
            # (0,0) is bottom-left, (width, height) is top-right of the screen
            gluOrtho2D(0, width, 0, height) 

            glMatrixMode(GL_MODELVIEW) # Switch to modelview matrix mode
            glPushMatrix()             # Save the current 3D modelview matrix
            glLoadIdentity()           # Reset modelview matrix

            # Disable depth testing so the text always draws on top
            glDisable(GL_DEPTH_TEST) 

            # --- Text Drawing ---
            provider_name = "--- [ Heart of Flesh ] Sample --- Data provided by Hidemune TANAKA" # <<-- Choose your phrase and name
            theme_title = "Research into the relationship between (The brain's reward system including the hippocampus and amygdala) and (Language)"
            text_color = (0.7, 0.7, 0.7) # Light gray color for the text

            # You'll need to estimate text width for right alignment.
            # GLUT_BITMAP_HELVETICA_18 is used, you'll need to know its approximate pixel width
            # This is a rough estimation; for precise alignment, you might need a font rendering library
            # or calculate character widths.
            text_width_estimate = len(provider_name) * 9 # Rough estimate for GLUT_BITMAP_HELVETICA_18
            text_height_estimate = 18 # Height of GLUT_BITMAP_HELVETICA_18

            # Calculate position for bottom-right corner (with some padding)
            padding_x = 20
            padding_y = 20
            pos_x = width - text_width_estimate - padding_x
            pos_y = padding_y # For bottom alignment
            
            # Draw the text using the existing function (or adapt it for 2D)
            # Note: glRasterPos3f expects 3D coordinates, but in 2D ortho mode, Z doesn't matter much.
            # It's effectively (x, y, 0)
            draw_label_gl(provider_name, pos_x, pos_y, 0, text_color) 
            
            
            #text_width_estimate = len(provider_name) * 10 # Rough estimate for GLUT_BITMAP_HELVETICA_18
            #text_height_estimate = 18 # Height of GLUT_BITMAP_HELVETICA_18
            
            pos_x2 = padding_x
            pos_y2 = height - text_height_estimate - padding_y # 画面上端から下へパディング
            draw_label_gl(theme_title, pos_x2, pos_y2, 0, text_color) 
            
            # --- Restore 3D State ---
            glEnable(GL_DEPTH_TEST)   # Re-enable depth testing for 3D scene
            glPopMatrix()             # Restore 3D modelview matrix
            glMatrixMode(GL_PROJECTION) # Switch back to projection matrix mode
            glPopMatrix()             # Restore 3D projection matrix
            glMatrixMode(GL_MODELVIEW) # Switch back to modelview matrix mode for the next frame
            # ----
            
            pygame.display.flip() # 画面を更新
            clock.tick(60)  # フレームレートを60FPSに制限
            angle += 0.048  # 回転速度を増分
        elif app_mode == 1: # 設定画面モードの描画
            # 設定画面を表示し、その中でイベントを処理
            display_settings_screen(screen) 
            # display_settings_screenから戻ってきたら、メインループを終了させるか、
            # 必要であれば app_mode を変更して別の画面に遷移させます。
            # 今回は設定表示のみなので、ループの継続条件はdisplay_settings_screen内で管理。
            break # 設定画面表示後はメインループを終了
            
    print("[INFO] Application loop ended.") # ループが終了した場合のログ

if __name__ == "__main__":
    main()
