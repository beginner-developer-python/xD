from captcha import *
from recognition import *
from map import *
from threading import *
from PIL import ImageGrab
path = os.path.dirname(os.path.dirname(__file__))
img_path = os.path.join(path, 'PokeMMO\img')
img_path_overlay = os.path.join(path, 'PokeMMO\img\overlays')

pokecenter_in = locate_image("Pokecenter_in.png", img_path)
yes = locate_image("Yes.png", img_path)


def teleport():
    Attk = locate_image("Attack.png", img_path)
    if Attk is not None:
        Click_Location(Attk[0], Attk[1])
        Run = locate_image("Run.png", img_path)
        if Run is not None:
            Click_Location(Run[0], Run[1])
        while True:
            Abra = locate_image("abra.png", img_path)
            if Abra is not None:
                Click_Location(Abra[0], Abra[1])
                Teleport = locate_image("Teleport.png", img_path)
                if Teleport is not None:
                    Click_Location(Teleport[0], Teleport[1])
                    pokecenter_in = locate_image("Pokecenter_in.png", img_path)
                    if pokecenter_in is not None:
                        Pokecenter()


def Pokecenter():
    while True:
        pokecenter_in = locate_image("Pokecenter_in.png", img_path)
        if pokecenter_in is not None:
            pyautogui.keyDown("Z")
            time.sleep(5)
            pyautogui.keyUp("Z")
            pyautogui.keyDown("S")
            while True:
                time.sleep(1)
                pyautogui.keyUp("S")
                break
            break
    time.sleep(21)
    return_toEarn()


def return_toEarn():
    while True:
        pokecenter_out = locate_image("Pokecenter_out.png", img_path)
        if (pokecenter_out is not None):
            path_main()
            pyautogui.keyDown("1")
            time.sleep(0.3)
            pyautogui.keyUp("1")
            break
    main()


PP = int(input("what is the PP of PayDay: "))
A = PP


def main():
    while True:
        global A, PP
        captcha = locate_image("abra.png", img_path)
        if captcha is not None:
            screenshot = ImageGrab.grab()
            screenshot.save("screenshot.png")
            send_1 = send(['192.168.0.200'], "screenshot.png")
            pyautogui.typewrite(send_1)
            print(send_1)
            os.remove("screenshot.png")
            continue
        time.sleep(1.0)
        Fight = locate_image("Fight.png", img_path)
        if Fight is not None:
            Horde = locate_image("Horde.png", img_path)
            if Horde is not None:
                while True:
                    Run = locate_image("Run.png", img_path)
                    if Run is not None:
                        Click_Location(Run[0], Run[1])
                        break
                continue
            Click_Location(Fight[0], Fight[1])
            if A == 0:
                A = PP
                teleport()
            payday = locate_image("PayDay.png", img_path)
            if payday is not None:
                while True:
                    Click_Location(payday[0], payday[1])
                    A = A - 1
                    break
        else:
            pyautogui.keyDown("A")
            time.sleep(0.2)
            # pyautogui.moveTo(100, 100)  # move mouse cursor to a safe location
            pyautogui.keyUp("A")
            pyautogui.keyDown("D")
            time.sleep(0.2)
            # pyautogui.moveTo(100, 100)  # move mouse cursor to a safe location
            pyautogui.keyUp("D")


keyboard.add_hotkey("p", Quit)
time.sleep(2)
# return_toEarn()
# time.sleep(3)
main()
