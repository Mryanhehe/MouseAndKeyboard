import time
import sys
import json
from pynput import mouse
from pynput import keyboard
from pynput.mouse import Button
from pynput.keyboard import Key,KeyCode
import Frame1
import wx
# 脚本格式，第一个元素：时间间隔
# 第二个元素：鼠标动作或者键盘动作  EM:鼠标  KM：键盘
# 三个元素：动作类型
# 第四个元素：具体参数
class BoaApp(wx.App):
    def OnInit(self):
        self.main = Frame1.create(None)
        print('create')
        # self.main = wx.Frame(parent = None)
        self.main.Show()
        self.SetTopWindow(self.main)
        return True

def main():
    application = BoaApp()
    application.MainLoop()

def single_run(script_path , run_time = 1):
    s = open(script_path,'r').read()
    print(s)
    s = json.loads(s)
    steps = len(s)
    mouse_ctl = mouse.Controller()
    keyboard_ctl = keyboard.Controller()
    j = 0
    while j < run_time or run_time == 0:
        j += 1
        for i in range(steps):
            print(s[i])
            if isinstance(s[i][0] ,str) and isinstance(s[i][3],int):
                s[i].insert(0,s[i][3])
            delay = s[i][0]
            event_type = s[i][1]
            message = s[i][2]
            action = s[i][3]
            time.sleep(delay/1000.0)

            if event_type == "EM":
                x,y = action
                mouse_ctl.position = (x,y)
                if message == 'mouse left down':
                    mouse_ctl.press(Button.left)
                elif message == 'mouse left up':
                    mouse_ctl.release(Button.left)
                elif message == 'mouse right down':
                    mouse_ctl.press(Button.right)
                elif message == 'mouse right up':
                    mouse_ctl.release(Button.right)
                else:
                    print('unknow mouse Event',message)

            elif event_type == 'EK':
                key_name = action
                if len(key_name) == 1:
                    key = key_name
                else:
                    key = getattr(Key , key_name)
                if message == 'key dowm':
                    keyboard_ctl.press(key)
                elif message == 'key up':
                    keyboard_ctl.release(key)
                else:
                    print('unknow keyboard event' , message)
    print('script run finish!!!')

    pass


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) > 1:
        script_path = sys.argv[1]
        runtimes = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        single_run(script_path , runtimes)
    else:
        main()