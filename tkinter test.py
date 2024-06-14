import tkinter as tk
import tkinter.ttk as ttk
from math import floor, ceil
from PIL import ImageTk, Image
# window = tk.Tk()
# label = tk.Label(text="henlo tkinter", foreground="white", background="black", width=25, height=5)
# button = tk.Button(
#     text="Click me!",
#     width=25,
#     height=5,
#     bg="blue",
#     fg="yellow",
# )
# label.grid(row=1,column=0)
# button.grid(row=2,column=1)
# for i in range(3):
#     window.columnconfigure(i, weight=1)
#     window.rowconfigure(i, weight=1)

# window.mainloop()

window = tk.Tk()
firstboot=True
brown = "#38342C"
window.configure(bg=brown, borderwidth=5)
#window.geometry("750x750")
special = ["ST","PE","EN","CH","IN","AG","LK"]
f=open("stats.txt")
stats = f.read()
statlist = stats.split("\n")
f.close()
specstats = statlist[0].strip('][').split(',')
specstats = [int(i) for i in specstats]
topleft=tk.Frame(master=window, background=brown)
topleft.grid(row=0, column=0, sticky="NW")
specialframe = tk.Frame(master = topleft, background=brown, borderwidth=5)
specialframe.grid(row=0,column=0, sticky = "NW")

specframe = []
numframe = [] 
statframe=[]
specbuttonids = []
statuseffects = ["Poisoned", "Burning", "Radiated", "Eye damage", "Crippled Right Arm", "Crippled Left Arm", "Crippled Right Leg", "Crippled Left Leg"]
statuseffectsresults = statlist[1].strip('][').split(',')
statuseffectsresults = [bool(i) for i in [int(j) for j in statuseffectsresults]]
Resistances = ["Action Points", "Carry Weight", "Damage Res.", "Poison Res.", "Radiation Res.", "Initiative", "Critical Chance"]
resvalues = []
#Must add spec bonuses
specbonus=0
RemSpecPoints = 40-sum(specstats)+specbonus
#Calculates resistances
def APcalc(modifier=0):
    resvalues.append((5+floor(specstats[5])+modifier))
    return

def CWcalc(modifier=0):
    resvalues.append((25+(specstats[0]*25))+modifier)
    return

def DRcalc(modifier=0):
    resvalues.append(min(((5*specstats[2]+modifier)/100), 90))
    return

def PRcalc(modifier=0):
    resvalues.append(modifier/100)
    return

def RRcalc(modifier=0):
    resvalues.append(modifier/100)
    return

def Inicalc(modifier=0):
    resvalues.append(2*specstats[1]+floor(1.5*specstats[5]))
    return

def CCcalc(modifier=0):
    resvalues.append(specstats[6]/100)
    return

# Implements SPECIAL screen, in the window at grid (0,0)

def handle_click(event):
    widget_id = event.widget.winfo_id()
    whichbutton(widget_id)
    print(f"{widget_id=}")
    
    
def whichbutton(widget_id):
    print(len(specbuttonids))
    listnum = specbuttonids.index(widget_id)
    if listnum <= 13:
    #Then SPECIAL        
        if listnum % 2 == 0:
            buttonnum = (f"pos {listnum//2}")
        else:
            buttonnum = (f"neg {listnum//2}")
        updatespecial(buttonnum)
        return
    elif listnum > 13:
        #Then Status effects
        listnum = listnum-14
        if statuseffectsresults[listnum] == False:
            statuseffectsresults[listnum] = True
        else:
            statuseffectsresults[listnum] = False
        updateeffects()
        return
    return


def updatespecial(buttonnum):
    numchange = buttonnum.split(" ")
    i = int(numchange[1])
    if numchange[0] == "pos" and int(specstats[i]) != 10:
        specstats[i] = int(specstats[i]) + 1
    elif numchange[0] == "neg" and int(specstats[i]) != 1:
        specstats[i] = int(specstats[i]) - 1
        
    numframe = (tk.Frame(master = specialframe, bg = brown, padx=5, pady=5))
    numframe.grid(row=i, column=1)
    numframe.columnconfigure(1)
    numframe.rowconfigure(1)
    label = tk.Label(master = numframe, text=specstats[i], foreground = "lime", background = "black", width = 2, height = 1, font="Gothic 20", relief = "sunken")
    label.pack()
    initiative = specstats[1]+specstats[5]
    RemSpecPoints = 40-sum(specstats)+specbonus
    label = tk.Label(master=specialframe, bg="black", fg="lime",  borderwidth=5, relief="sunken", text=RemSpecPoints, font="Gothic 10", width = 2, height = 1)
    label.grid(row=7,column=1)
    GenerateResistancesFrame()
    GenerateHPFrame()
    SkillsFrame()
    
for i in range(len(special)):
    #Labels
    specframe.append(tk.Frame(master = specialframe, bg = brown, padx=5, pady=5))
    specframe[i].grid(row=i, column=0, sticky="NSW")
    label = tk.Label(master = specframe[i], text=special[i], foreground = "yellow", background = brown, width = 2, height = 1, font="Gothic 20", relief = "groove")
    label.pack()
    #Numbers
    numframe.append(tk.Frame(master = specialframe, bg = brown, padx=5, pady=5))
    numframe[i].grid(row=i, column=1)
    numframe[i].columnconfigure(1)
    numframe[i].rowconfigure(1)
    label = tk.Label(master = numframe[i], text=specstats[i], foreground = "lime", background = "black", width = 2, height = 1, font="Gothic 20", relief = "sunken")
    label.pack()
    #Buttons
    statframe.append(tk.Frame(master = specialframe, bg = brown, padx=5, pady=5))
    statframe[i].grid(row=i, column=2, sticky="N")
    statframe[i].columnconfigure(1)
    statframe[i].rowconfigure(1)
    button = tk.Button(master = statframe[i], text="+", bg=brown, fg="yellow", font="Gothic 7")
    specbuttonids.append(button.winfo_id())
    button.bind("<Button-1>", handle_click)
    button.pack()
    button = tk.Button(master = statframe[i], text="-", bg=brown, fg="yellow", font="Gothic 7")
    specbuttonids.append(button.winfo_id())
    button.bind("<Button-1>", handle_click)
    button.pack()

label = tk.Label(master=specialframe, bg=brown, fg="yellow", relief="groove", text="Points \n Available", font="Gothic 10")
label.grid(row=7,column=0, sticky="W")
label = tk.Label(master=specialframe, bg="black", fg="lime",  borderwidth=5, relief="sunken", text=RemSpecPoints, font="Gothic 10", width = 2, height = 1)
label.grid(row=7,column=1)

# Implements status screen
statusframe = tk.Frame(master = topleft, background = brown, borderwidth=5)
statusframe.grid(row=0, column = 1, sticky = "NSEW")
effectsframe = tk.Frame(master = statusframe, background = "black", borderwidth=5, relief="sunken")
effectsframe.grid(row=1, column = 0, sticky = "NSEW")
resframe = tk.Frame(master = statusframe, background = "black", borderwidth=5, relief="sunken")
resframe.grid(row=2, column = 0, sticky = "NSEW")

#HP Screen
def GenerateHPFrame():
    hpframe = tk.Frame(master = statusframe, background=brown, borderwidth = 2)
    hpframe.grid(row=0,column=0, sticky="NSEW")
    label = tk.Label(master = hpframe, text = "Hit Points", relief = "sunken", font="Gothic 10", bg="black", fg="lime")
    label.grid(row=0, column=0, sticky="NSEW")
    hpinput = tk.Entry(master=hpframe, width = 3, bg="black", fg="lime", font = "Gothic 10")
    hpinput.grid(row=0, column = 1, sticky="NSEW")
    hpinput.insert(0, str(15+specstats[0]+specstats[2]*2))

GenerateHPFrame()
#Status screen (+Update function)

for i in statuseffects:
    button = tk.Button(master=effectsframe, text = i, background="black", foreground="dark green", font="Gothic 8")
    specbuttonids.append(button.winfo_id())
    button.bind("<Button-1>", handle_click)
    button.grid(row=statuseffects.index(i), column=0, sticky="W")
        
def updateeffects():
    global specbuttonids
    specbuttonids = specbuttonids[:14]
    for widget in effectsframe.winfo_children():
        widget.destroy()
    for i in statuseffects:
        
        if statuseffectsresults[statuseffects.index(i)] == True:
            button = tk.Button(master=effectsframe, text = i, background="black", foreground="lime", font="Gothic 8")
        else:
            button = tk.Button(master=effectsframe, text = i, background="black", foreground="dark green", font="Gothic 8")
        specbuttonids.append(button.winfo_id())
        button.bind("<Button-1>", handle_click)
        button.grid(row=statuseffects.index(i), column=0, sticky="W")
        
#Resistances frame

def GenerateResistancesFrame(apmod=0,cwmod=0,drmod=0,prmod=0,rrmod=0,inimod=0,ccmod=0):
    resvalues.clear()
    for widget in resframe.winfo_children():
        widget.destroy()
    APcalc(apmod)
    CWcalc(cwmod)
    DRcalc(drmod)
    PRcalc(prmod)
    RRcalc(rrmod)
    Inicalc(inimod)
    CCcalc(ccmod)
    for i in Resistances:
        label = tk.Label(master=resframe, text=i, background="black", foreground="lime", font="Gothic 8")
        label.grid(row=Resistances.index(i), column=0, sticky="W")
        label = tk.Label(master=resframe, text=resvalues[Resistances.index(i)], background="black", foreground="lime", font="Gothic 8")
        label.grid(row=Resistances.index(i), column=1, sticky="E")

GenerateResistancesFrame()

# LevelUp frame

levelframe = tk.Frame(master = window, bg=brown, borderwidth=5)
levelframe.grid(row=1, column=0, sticky="SWE")

def Levelupscreen(stuff=0):
    screen=tk.Tk()
    screen.configure(bg=brown,borderwidth=5)
    textframe=tk.Frame(master=screen, bg=brown,borderwidth=5)
    textframe.grid(row=0,column=0)
    label=tk.Label(master=textframe, text="Enter XP Gained:", fg="lime", bg="black", borderwidth=5, relief="sunken")
    label.grid(row=0,column=0, sticky="W")
    lvlentry = tk.Entry(master=textframe, fg="lime", bg="black", borderwidth=5)
    lvlentry.grid(row=0,column=1, sticky="W")
    buttonframe = tk.Frame(master=screen, bg=brown,borderwidth=5)
    buttonframe.grid(row=1,column=0)
    button=tk.Button(master=buttonframe, fg="Yellow", bg=brown, borderwidth=5, relief="raised", text="OK", command=lambda: Exitlvlup(lvlentry,screen))
    button.grid(row=0,column=0,sticky="NSEW")
    return
    
def Exitlvlup(lvlentry, screen):
    global levelstuff
    xpgained = int("0"+lvlentry.get())
    levelstuff[1] = levelstuff[1]+xpgained
    while levelstuff[1]>levelstuff[2]:
        levelstuff[0]=levelstuff[0]+1
        levelstuff[2]=ceil(levelstuff[2]*1.2)
    GenerateLevelFrame(levelstuff[0], levelstuff[1], levelstuff[2])
    screen.destroy()
    return
    

def GenerateLevelFrame(level, currentxp, targetxp):
    for widget in levelframe.winfo_children():
        widget.destroy()
    levstatframe = tk.Frame(master=levelframe, bg="black", relief="sunken", borderwidth=5)
    levstatframe.grid(row=0,column=0)
    label = tk.Label(master=levstatframe, text=f"Level: {level}", background="black", foreground="lime", font="Gothic 8")
    label.grid(row=0,column=0, sticky="W")
    label = tk.Label(master=levstatframe, text=f"Current EXP: {currentxp}", background="black", foreground="lime", font="Gothic 8")
    label.grid(row=1,column=0, sticky="W")
    label = tk.Label(master=levstatframe, text=f"Next Level: {targetxp}", background="black", foreground="lime", font="Gothic 8")
    label.grid(row=2,column=0, sticky="W")
    button = tk.Button(master=levelframe,background=brown,foreground="yellow",relief="raised", text="Lvl Up", font="Gothic", command=Levelupscreen)
    button.grid(row=0,column=1,sticky="NSEW")
    return
    
    
levelstuff = statlist[2].strip('][').split(',')
levelstuff = [int(i) for i in levelstuff]

GenerateLevelFrame(levelstuff[0], levelstuff[1], levelstuff[2])

#Skills frame

skillsframe = tk.Frame(master=window, bg="black", borderwidth=5, relief="sunken")
skillsframe.grid(row=0,column=1,sticky="NWE")

skillvalues = statlist[3].strip('][').split(',')
skillvalues = [int(i) for i in skillvalues]

skilladj = statlist[4].strip('][').split(',')
skilladj = [int(i) for i in skilladj]

AllFrame = tk.Frame(master=window,borderwidth=5, bg=brown)
AllFrame.grid(row=1,column=1,sticky="SWE")

skillnames = ["Small Guns", "Big Guns", "Energy Weapons", "Explosives", "Unarmed", "Melee Weapons", "Throwing", "First aid", "Surgeon", "Sneak", "Lockpick", "Steal", "Traps", "Science", "Repair", "Speech", "Barter", "Survival"]
AvailablePoints=int(statlist[5])
def SkillsFrame():
    global skillvalues
    global AllFrame
    for widget in skillsframe.winfo_children():
        widget.destroy()
    for widget in AllFrame.winfo_children():
        widget.destroy()
    
    SkillValues(*skilladj)
    for i in range(len(skillnames)):
        label = tk.Label(master=skillsframe, text=f"{skillnames[i]}: {skillvalues[i]}", bg="black", fg="lime", font="Gothic 8")
        label.grid(row=i,column=0,sticky="W")
    
    label = tk.Label(master=AllFrame, bg="black", fg="lime", relief="sunken",text=f"Skill Points to Allocate: {AvailablePoints}", borderwidth=5)
    label.grid(row=0,column=0, sticky="NEW")
    button = tk.Button(master=AllFrame, bg=brown, fg="yellow", borderwidth=5, relief="raised", command=AllocatePointsScreen, text="Allocate Points")
    button.grid(row=1, column=0, sticky="NEW")
    
PointsButtonLoc=[]
    
def AllocatePointsScreen():
    global skilladj
    global skillnames
    global PointsWindow
    global TextFrame1
    global Textframe2
    global ButtonFrame
    PointsWindow=tk.Tk()
    PointsWindow.configure(bg=brown)
    TextFrame1 = tk.Frame(master=PointsWindow, bg="black", borderwidth=5, relief="sunken")
    TextFrame1.grid(row=0,column=0,sticky="NSEW")
    ButtonFrame = tk.Frame(master=PointsWindow, bg=brown, borderwidth=5)
    ButtonFrame.grid(row=0,column=1, sticky="NSEW")
    Textframe2 = tk.Frame(master=PointsWindow, bg=brown)
    Textframe2.grid(row=1,column=0)
    button=tk.Button(master=Textframe2, bg=brown, fg="yellow", relief="raised", text="OK", command=PointsWindow.destroy)
    button.grid(row=0,column=1,sticky="NSEW")
    GeneratePointsPopup()
    
def GeneratePointsPopup():
    global PointsWindow
    global TextFrame1
    global Textframe2
    global ButtonFrame
    global skillnames
    global skillvalues
    global skilladj
    global AvailablePoints
    PointsButtonLoc.clear()
    SkillValues(*skilladj)
    for i in range(len(skillvalues)):
        label = tk.Label(master=TextFrame1, bg="black", fg="lime", text=f"{skillnames[i]}: {skillvalues[i]}", font="Gothic 15")
        label.grid(row=i,column=0,sticky="NSEW")
        ButtonMiniFrame = tk.Frame(master=ButtonFrame, bg="brown")
        ButtonMiniFrame.grid(row=i,column=0)
        button=tk.Button(master=ButtonMiniFrame, bg=brown, fg="yellow", text="+", font="Gothic 11")
        button.bind("<Button-1>", SkillChange)
        button.grid(row=0,column=0, sticky="NSEW")
        PointsButtonLoc.append(button.winfo_id())
        button=tk.Button(master=ButtonMiniFrame, bg=brown, fg="yellow", text="-", font="Gothic 11")
        button.bind("<Button-1>", SkillChange)
        button.grid(row=0,column=1,sticky="NSEW")
        PointsButtonLoc.append(button.winfo_id())
    label = tk.Label(master=Textframe2, bg = "black", fg="lime", text=f"Skill Points to Allocate: {AvailablePoints}", relief="sunken")
    label.grid(row=0,column=0, sticky="NSEW")
   
def SkillChange(event):
    global PointsWindow
    global TextFrame1
    global ButtonFrame
    global AvailablePoints
    WhichButton = PointsButtonLoc.index(event.widget.winfo_id())
    i=WhichButton//2
    if WhichButton % 2 == 0:
        skilladj[i]=skilladj[i]+1
        AvailablePoints=AvailablePoints-1
    else:
        skilladj[i]=skilladj[i]-1
        AvailablePoints=AvailablePoints+1
    GeneratePointsPopup()
    SkillsFrame()
    
    
    

    
# def IncrementSkill(skillname, PointsWindow,TextFrame1,ButtonFrame):
#     global skilladj
#     global skillnames
#     global AvailablePoints
#     i = skillnames.index(skillname)
#     skilladj[i] = skilladj[i]+1
#     AvailablePoints = AvailablePoints-1
#     for widget in TextFrame1.winfo_children():
#         widget.destroy()
#     for widget in ButtonFrame.winfo_children():
#         widget.destroy()
#     GeneratePointsPopup(PointsWindow, TextFrame1, ButtonFrame)
#     return

# def DecrementSkill(skillname, PointsWindow,TextFrame1,ButtonFrame):
#     global skilladj
#     global skillnames
#     global AvailablePoints
#     i = skillnames.index(skillname)
#     skilladj[i] = skilladj[i]-1
#     AvailablePoints = AvailablePoints+1
#     for widget in TextFrame1.winfo_children():
#         widget.destroy()
#     for widget in ButtonFrame.winfo_children():
#         widget.destroy()
#     GeneratePointsPopup(PointsWindow, TextFrame1, ButtonFrame)
#     return
    
    
    
    
    
def SkillValues(SGA=0,BGA=0,EWA=0,EXA=0,UNA=0,MWA=0,THA=0,FAA=0,SRA=0,SNA=0,LPA=0,STA=0,TRA=0,SCA=0,REA=0,SPA=0,BAA=0,SUA=0):
    global skillvalues
    skillvalues[0]=(35+specstats[5]+SGA)
    skillvalues[1]=(10+specstats[5]+BGA)
    skillvalues[2]=(10+specstats[5]+EWA)
    skillvalues[3]=(ceil(2+(2*specstats[1])+(specstats[6]/2))+EXA)
    skillvalues[4]=(ceil(65+(specstats[5]+specstats[0])/2)+UNA)
    skillvalues[5]=(ceil(55+(specstats[5]+specstats[0])/2)+MWA)
    skillvalues[6]=(40+specstats[5]+THA)
    skillvalues[7]=(ceil(30+(specstats[1]+specstats[4])/2)+FAA)
    skillvalues[8]=(ceil(15+(specstats[1]+specstats[4])/2)+SRA)
    skillvalues[9]=(25+specstats[5]+SNA)
    skillvalues[10]=(ceil(20+(specstats[5]+specstats[1])/2)+LPA)
    skillvalues[11]=(20+specstats[5]+STA)
    skillvalues[12]=(ceil(20+(specstats[5]*specstats[1])/2)+TRA)
    skillvalues[13]=(25+2*specstats[4]+SCA)
    skillvalues[14]=(20+specstats[4]+REA)
    skillvalues[15]=(25+2*specstats[3]+SPA)
    skillvalues[16]=(20+2*specstats[3]+BAA)
    skillvalues[17]=(2+2*specstats[2]+ceil(specstats[6]/2)+SUA)
    return


SkillsFrame()

ArmourFrame = tk.Frame(master=window, background=brown, borderwidth=5)
ArmourFrame.grid(row=0,column=2, sticky="n")
ArmourImage = ImageTk.PhotoImage(Image.open("ArmourCard.png"))
LeftArmour = tk.Frame(master=ArmourFrame, bg=brown)
LeftArmour.grid(row=0,column=0, sticky="NS")
label=tk.Label(master=ArmourFrame, image=ArmourImage, borderwidth=5, relief="sunken", bg="black")
label.grid(row=0,column=1)
RightArmour = tk.Frame(master=ArmourFrame, bg=brown)
RightArmour.grid(row=0,column=2, sticky="NS")
LArmFrames=[]
LButtons=[]
RButtons=[]
RArmFrames=[]

for i in range(4):
    frame=(tk.Frame(master=LeftArmour, pady=19, bg=brown))
    frame.grid(row=i, column=0,sticky="NSEW")
    LArmFrames.append(frame)
    
for i in range(4):
    frame=(tk.Frame(master=RightArmour, pady=19, bg=brown))
    frame.grid(row=i, column=0, sticky="NSEW")
    RArmFrames.append(frame)    
    

def ArmourFrameGen():
    LButtons.clear()
    RButtons.clear()

    for i in range(4):
        button=tk.Button(master=LArmFrames[i], bg=brown, fg="yellow", text="L")
        button.pack()
        LButtons.append(button)
        button=tk.Button(master=RArmFrames[i], bg=brown, fg="yellow", text="R")
        button.pack()
        RButtons.append(button)
        
ArmourFrameGen()

window.mainloop()

