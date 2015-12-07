from tkinter import *
from math import *

def cot(x):
    return 1 / tan(x)

def sec(x):
    return 1 / cos(x)

def format(fn):
    funktsioon = "";
    for i in range(len(fn)):
        if fn[i] == "x":
            if i > 0 and (fn[i - 1].isnumeric() or fn[i - 1] == "x"):
                funktsioon += "*x";
                continue;
            funktsioon += "x";
        else:
            if i > 0 and fn[i - 1] == "x" and fn[i].isnumeric():
                funktsioon += "*" + fn[i];
                continue;
            funktsioon += fn[i];
    return funktsioon;

def funktsiooni_väärtus(y, x):
    return eval(format(y).replace("x", str(x)));

def tõus(y, x):
    try:
        y0 = funktsiooni_väärtus(y, x - 0.1);
        y1 = funktsiooni_väärtus(y, x);
        y2 = funktsiooni_väärtus(y, x + 0.1);
        if (y1 > y0 and y1 > y2) or (y1 < y0 and y1 < y2):
            return 0
        return  y2 - y1;
    except:
        return 0
def kiirendus(y, x):
    try:
        k0 = tõus(y, x - 0.1);
        k1 = tõus(y, x);
        k2 = tõus(y, x + 0.1);
        if (k1 > k0 and k1 > k2) or (k1 < k0 and k1 < k2):
            return x*suurendus
        return None
    except:
        return None

def onLeftDrag(event):
    global tahvel
    tahvel.scan_dragto(event.x, event.y, gain=1)

def onMove(event):
    global tahvel;
    tahvel.scan_mark(event.x, event.y)

def lisa_punkt(list, x, y):
    list.append(x)
    list.append(y)

def joonista_joon(punktid, x, y):
    global näita_tõusu, jooni
    if len(punktid) != 4:
        return
    värv = "Blue"
    if näita_tõusu.get() == 1:
        värv = "Red"
        if tõus(y, x) > 0:
            värv = "Green"
    tahvel.create_line(punktid, width = 2, fill = värv)
    jooni+=1

def joonesta_graafik():
    global fun_number, x_vahe, jooni
    jooni = 0
    y = sisendiruut_joonesta.get()
    fun_number += 1
    funktsioonide_kast.insert(END, str(fun_number)+". y = "+str(y))

    eelmine_punkt = []
    x = -round(suurus/2, 2);
    while x <= round(suurus/2, 2):
        try:
            if round(suurus/2, 2)-x_vahe>x>-round(suurus/2, 2)+x_vahe and tõus(y, x) == 0:
                raise Exception
            
            punkt = []
            if len(eelmine_punkt) >= 2:
                lisa_punkt(punkt, eelmine_punkt[0], eelmine_punkt[1])
            
            y_väärtus = funktsiooni_väärtus(y, x) * suurendus;
            if y_väärtus < -suurus*1.25 or y_väärtus > suurus*1.25:
                x += x_vahe
                x = round(x, 2)
                continue
            lisa_punkt(punkt, (x * suurendus) + suurus / 2, (-y_väärtus) + suurus / 2)

            if len(punkt)>=4:
                if abs(punkt[1]-punkt[3])<300:
                    joonista_joon(punkt, x, y)
                else:
                    pass
                
            #if kiirendus(y, x) != None:
            #   tahvel.create_oval(x * suurendus - 2, -y_väärtus - 2, x * suurendus + 2, -y_väärtus + 2, fill = "pink");
            eelmine_punkt = []
            try:
                lisa_punkt(eelmine_punkt, punkt[2], punkt[3])
            except:
                lisa_punkt(eelmine_punkt, punkt[0], punkt[1])
        except:
            x += x_vahe
            x = round(x, 2)
            if x == 0:
                x = 10**(-120)
                y_väärtus = funktsiooni_väärtus(y, x) * suurendus;
                lisa_punkt(punkt, (x * suurendus) + suurus / 2, (-y_väärtus) + suurus / 2)
                lisa_punkt(eelmine_punkt, punkt[0], punkt[1])
            continue
        x += x_vahe
        x = round(x, 2)
    print("Joonistati", jooni, "joont")

def joonista_teljed():
    nihe = (suurus / suurendus - floor(suurus / suurendus)) * suurendus
    for line_y in range(-suurus, suurus, suurendus):
        tahvel.create_line(-suurus, line_y + nihe, suurus, line_y + nihe, fill = "gray")
    for line_x in range(-suurus, suurus, suurendus):
        tahvel.create_line(line_x + nihe, -suurus, line_x + nihe, suurus, fill = "gray")
    tahvel.create_line(0, suurus, 0, -suurus, arrow = LAST)
    tahvel.create_line(-suurus, 0, suurus, 0, arrow = LAST)
    tahvel.move(ALL, suurus / 2, suurus / 2)

def puhasta():
    global fun_number
    tahvel.delete(ALL)
    joonista_teljed()
    funktsioonide_kast.delete(0,END)
    fun_number = 0
suurendus = 10
x_vahe = 0.1
suurus = 500
fun_number = 0
jooni = 0

raam = Tk()
raam.configure(background="beige")
raam.title("Graafiku joonestaja")
tahvel = Canvas(raam, width = suurus, height = suurus, background = "lightgray", scrollregion=(-suurus//2, -suurus//2, suurus+suurus//2, suurus+suurus//2))
tahvel.pack(fill=BOTH, expand=YES)
tahvel.grid()

uus_raam = Frame(raam)
uus_raam.grid(row=0, column=1, columnspan=2, sticky=(W,S))
keriruut = Scrollbar(uus_raam)
keriruut.pack(side=RIGHT, fill=Y)
funktsioonide_kast = Listbox(uus_raam, height=10, width=27)
funktsioonide_kast.pack(expand=True,fill=Y)
funktsioonide_kast.config(yscrollcommand=keriruut.set)
keriruut.config(command=funktsioonide_kast.yview)

joonista_teljed()

Label(raam, text = "Sisend", background = "beige", foreground = "black").grid(column=1, row=0, columnspan=2, sticky=N)
sisendiruut_joonesta = Entry(raam, width=20);
sisendiruut_joonesta.grid(column=1, row=0, pady=23, sticky=(N,W))
Button(raam, text="Joonesta", command=joonesta_graafik).grid(column=2, row=0, pady=20, sticky=(N,E))
Button(raam, text="Puhasta", command=puhasta).grid(column=1, row=1, columnspan=2, sticky=(S))

Label(raam, text = "Valikud", background = "beige", foreground = "black").grid(column=1, row=0, columnspan=2, pady=60, sticky=N)
näita_tõusu = IntVar()
Checkbutton(raam, text="Näita tõusu", variable=näita_tõusu).grid(row=0, column=1, pady=80, sticky=(N, W))

Label(raam, text = """Juhend:
Astendamine: pow(*astendatav*, *astendaja*)
Logaritm: log(*logartimitav*, *logaritmi alus*)
Naturaallogaritm: log(*logaritmitav*)
Trigonomeertilised funktsioonid: sin/cos/tan/cot(*argument*)
Arkusfunktsioonid: asin/acos/atan/acot(*argument*)""", justify=LEFT, background = "beige", foreground = "black").grid(column=0, row=1, columnspan=2, sticky=W)

tahvel.bind('<ButtonPress-1>', onMove)
tahvel.bind('<B1-Motion>', onLeftDrag)
tahvel.focus();
raam.mainloop();