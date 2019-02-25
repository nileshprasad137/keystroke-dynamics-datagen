import pyHook
import pythoncom


def OnKeyboardEvent(event):
    print('MessageName:', event.MessageName)
    print('Message:', event.Message)
    print('Time:', event.Time)
    print('Window:', event.Window)
    print('WindowName:', event.WindowName)
    print('Ascii:', event.Ascii, chr(event.Ascii))
    print('Key:', event.Key)
    print('KeyID:', event.KeyID)
    print('ScanCode:', event.ScanCode)
    print('Extended:', event.Extended)
    print('Injected:', event.Injected)
    print('Alt', event.Alt)
    print('Transition', event.Transition)
    print('---')
    return True


# When the user presses a key down anywhere on their system
# the hook manager will call OnKeyboardEvent function.     
hm = pyHook.HookManager()
hm.KeyDown = OnKeyboardEvent
# Here we register the same function to the KeyUp event. 
# Probably in practice you will create a different function to handle KeyUp functionality
hm.KeyUp = OnKeyboardEvent
hm.HookKeyboard()

try:
    pythoncom.PumpMessages()
except KeyboardInterrupt:
    pass
