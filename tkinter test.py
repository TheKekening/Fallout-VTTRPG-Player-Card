import tkinter as tk
import tkinter.ttk as ttk
from math import floor, ceil
from PIL import ImageTk, Image
import os
import re
path = str(__file__)
print(f"{path=}")
dirpath = path.removesuffix("\\tkinter test.py")

print(dirpath)

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
firstboot = True
brown = "#38342C"
window.configure(bg=brown, borderwidth=5)
# window.geometry("750x750")
special = ["ST", "PE", "EN", "CH", "IN", "AG", "LK"]
f = open("Stats.txt")
Skills = f.read()
Skilllist = Skills.split("\n")
f.close()
specSkills = Skilllist[0].strip('][').split(',')
specSkills = [int(i) for i in specSkills]

Skilluseffectsresults = Skilllist[1].strip('][').split(',')
Skilluseffectsresults = [bool(i) for i in [int(j)
                                          for j in Skilluseffectsresults]]

levelstuff = Skilllist[2].strip('][').split(',')
levelstuff = [int(i) for i in levelstuff]


skillvalues = [0,]*18
skillallocated = Skilllist[3].strip('][').split(',')
skillallocated = [int(i) for i in skillallocated]

skilladj = Skilllist[4].strip('][').split(',')
skilladj = [int(i) for i in skilladj]
print(f"OUTSIDE FUNCTION {skilladj=}")

AvailablePoints = int(Skilllist[5].replace("[","").replace("]",""))

ArmourWorn = Skilllist[6].strip('][').split(',')
ArmourWorn = [str(i).replace("'", "").replace('"',"") for i in ArmourWorn]

topframe = tk.Frame(master=window, bg=brown)
topframe.grid(row=0,column=0)
topleft = tk.Frame(master=topframe, background=brown)
topleft.grid(row=0, column=0, sticky="NW")
specialframe = tk.Frame(master=topleft, background=brown, borderwidth=5)
specialframe.grid(row=0, column=0, sticky="NW")

specframe = []
numframe = []
Skillframe = []
specbuttonids = []
Skilluseffects = ["Poisoned", "Burning", "Radiated", "Eye damage",
                 "Crippled Right Arm", "Crippled Left Arm", "Crippled Right Leg", "Crippled Left Leg"]

Resistances = ["Action Points", "Carry Weight", "Damage Res.",
               "Poison Res.", "Radiation Res.", "Initiative", "Critical Chance"]
resvalues = []
# Must add spec bonuses
specbonus = 0
RemSpecPoints = 40-sum(specSkills)+specbonus
# Calculates resistances


def APcalc(modifier=0):
    resvalues.append((5+floor(specSkills[5])+modifier))
    return


def CWcalc(modifier=0):
    resvalues.append((25+(specSkills[0]*25))+modifier)
    return


def DRcalc(modifier=0):
    resvalues.append(min(((5*specSkills[2]+modifier)/100), 90))
    return


def PRcalc(modifier=0):
    resvalues.append(modifier/100)
    return


def RRcalc(modifier=0):
    resvalues.append(modifier/100)
    return


def Inicalc(modifier=0):
    resvalues.append(2*specSkills[1]+floor(1.5*specSkills[5]))
    return


def CCcalc(modifier=0):
    resvalues.append(specSkills[6]/100)
    return

# Implements SPECIAL screen, in the window at grid (0,0)


def handle_click(event):
    widget_id = event.widget.winfo_id()
    whichbutton(widget_id)


def whichbutton(widget_id):
    listnum = specbuttonids.index(widget_id)
    if listnum <= 13:
        # Then SPECIAL
        if listnum % 2 == 0:
            buttonnum = (f"pos {listnum//2}")
        else:
            buttonnum = (f"neg {listnum//2}")
        updatespecial(buttonnum)
        return
    elif listnum > 13:
        # Then Skillus effects
        listnum = listnum-14
        if Skilluseffectsresults[listnum] == False:
            Skilluseffectsresults[listnum] = True
        else:
            Skilluseffectsresults[listnum] = False
        updateeffects()
        return
    return


def updatespecial(buttonnum):
    global specbonus
    numchange = buttonnum.split(" ")
    i = int(numchange[1])
    if numchange[0] == "pos" and int(specSkills[i]) != 10:
        specSkills[i] = int(specSkills[i]) + 1
    elif numchange[0] == "neg" and int(specSkills[i]) != 1:
        specSkills[i] = int(specSkills[i]) - 1

    numframe = (tk.Frame(master=specialframe, bg=brown, padx=5, pady=5))
    numframe.grid(row=i, column=1)
    numframe.columnconfigure(1)
    numframe.rowconfigure(1)
    label = tk.Label(master=numframe, text=specSkills[i], foreground="lime",
                     background="black", width=2, height=1, font="Gothic 20", relief="sunken")
    label.pack()
    RemSpecPoints = 40-sum(specSkills)+specbonus
    label = tk.Label(master=remainingframe, bg="black", fg="lime",  borderwidth=5,
                     relief="sunken", text=RemSpecPoints, font="Gothic 10", width=2, height=1)
    label.grid(row=0, column=1)
    GenerateResistancesFrame()
    GenerateHPFrame()
    SkillsFrame()


for i in range(len(special)):
    # Labels
    specframe.append(tk.Frame(master=specialframe, bg=brown, padx=5, pady=5))
    specframe[i].grid(row=i, column=0, sticky="NSW")
    label = tk.Label(master=specframe[i], text=special[i], foreground="yellow",
                      background=brown, width=2, height=1, font="Gothic 20", relief="groove")
    label.pack()
    # Numbers
    numframe.append(tk.Frame(master=specialframe, bg=brown, padx=5, pady=5))
    numframe[i].grid(row=i, column=1)
    numframe[i].columnconfigure(1)
    numframe[i].rowconfigure(1)
    label = tk.Label(master=numframe[i], text=specSkills[i], foreground="lime",
                      background="black", width=2, height=1, font="Gothic 20", relief="sunken")
    label.pack()
    # Buttons
    Skillframe.append(tk.Frame(master=specialframe, bg=brown, padx=5, pady=5))
    Skillframe[i].grid(row=i, column=2, sticky="N")
    Skillframe[i].columnconfigure(1)
    Skillframe[i].rowconfigure(1)
    button = tk.Button(
        master=Skillframe[i], text="+", bg=brown, fg="yellow", font="Gothic 7")
    specbuttonids.append(button.winfo_id())
    button.bind("<Button-1>", handle_click)
    button.pack()
    button = tk.Button(
        master=Skillframe[i], text="-", bg=brown, fg="yellow", font="Gothic 7")
    specbuttonids.append(button.winfo_id())
    button.bind("<Button-1>", handle_click)
    button.pack()



# Implements Skillus screen
Skillusframe = tk.Frame(master=topleft, background=brown, borderwidth=5)
Skillusframe.grid(row=0, column=1, sticky="NSEW")
effectsframe = tk.Frame(
    master=Skillusframe, background="black", borderwidth=5, relief="sunken")
effectsframe.grid(row=1, column=0, sticky="NSEW")
resframe = tk.Frame(master=Skillusframe, background="black",
                    borderwidth=5, relief="sunken")
resframe.grid(row=2, column=0, sticky="NSEW")

# HP Screen


def GenerateHPFrame():
    hpframe = tk.Frame(master=Skillusframe, background=brown, borderwidth=2)
    hpframe.grid(row=0, column=0, sticky="NSEW")
    label = tk.Label(master=hpframe, text="Hit Points",
                     relief="sunken", font="Gothic 10", bg="black", fg="lime")
    label.grid(row=0, column=0, sticky="NSEW")
    hpinput = tk.Entry(master=hpframe, width=3, bg="black",
                       fg="lime", font="Gothic 10")
    hpinput.grid(row=0, column=1, sticky="NSEW")
    hpinput.insert(0, str(15+specSkills[0]+specSkills[2]*2))


# Skillus screen (+Update function)

for i in Skilluseffects:
    button = tk.Button(master=effectsframe, text=i, background="black",
                       foreground="dark green", font="Gothic 8")
    specbuttonids.append(button.winfo_id())
    button.bind("<Button-1>", handle_click)
    button.grid(row=Skilluseffects.index(i), column=0, sticky="W")


def updateeffects():
    global specbuttonids
    specbuttonids = specbuttonids[:14]
    for widget in effectsframe.winfo_children():
        widget.destroy()
    for i in Skilluseffects:

        if Skilluseffectsresults[Skilluseffects.index(i)] == True:
            button = tk.Button(master=effectsframe, text=i,
                               background="black", foreground="lime", font="Gothic 8")
        else:
            button = tk.Button(master=effectsframe, text=i, background="black",
                               foreground="dark green", font="Gothic 8")
        specbuttonids.append(button.winfo_id())
        button.bind("<Button-1>", handle_click)
        button.grid(row=Skilluseffects.index(i), column=0, sticky="W")

# Resistances frame


def GenerateResistancesFrame(apmod=0, cwmod=0, drmod=0, prmod=0, rrmod=0, inimod=0, ccmod=0):
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
        label = tk.Label(master=resframe, text=i,
                         background="black", foreground="lime", font="Gothic 8")
        label.grid(row=Resistances.index(i), column=0, sticky="W")
        label = tk.Label(master=resframe, text=resvalues[Resistances.index(
            i)], background="black", foreground="lime", font="Gothic 8")
        label.grid(row=Resistances.index(i), column=1, sticky="E")


# LevelUp frame
levelframe = tk.Frame(master=topframe, bg=brown, borderwidth=5)
levelframe.grid(row=1, column=0, sticky="SWE")


def Levelupscreen(stuff=0):
    screen = tk.Tk()
    screen.configure(bg=brown, borderwidth=5)
    textframe = tk.Frame(master=screen, bg=brown, borderwidth=5)
    textframe.grid(row=0, column=0)
    label = tk.Label(master=textframe, text="Enter XP Gained:",
                     fg="lime", bg="black", borderwidth=5, relief="sunken")
    label.grid(row=0, column=0, sticky="W")
    lvlentry = tk.Entry(master=textframe, fg="lime", bg="black", borderwidth=5)
    lvlentry.grid(row=0, column=1, sticky="W")
    buttonframe = tk.Frame(master=screen, bg=brown, borderwidth=5)
    buttonframe.grid(row=1, column=0)
    button = tk.Button(master=buttonframe, fg="Yellow", bg=brown, borderwidth=5,
                       relief="raised", text="OK", command=lambda: Exitlvlup(lvlentry, screen))
    button.grid(row=0, column=0, sticky="NSEW")
    return


def Exitlvlup(lvlentry, screen):
    global levelstuff
    global AvailablePoints
    xpgained = int("0"+lvlentry.get())
    levelstuff[1] = levelstuff[1]+xpgained
    while levelstuff[1] >= levelstuff[2]:
        levelstuff[0] = levelstuff[0]+1
        n = levelstuff[0] + 1
        levelstuff[2] = ceil((n*(n-1)/2)*1000)
        AvailablePoints += 15
    GenerateLevelFrame(levelstuff[0], levelstuff[1], levelstuff[2])
    Update()
    screen.destroy()
    return


def GenerateLevelFrame(level, currentxp, targetxp):
    for widget in levelframe.winfo_children():
        widget.destroy()
    levSkillframe = tk.Frame(master=levelframe, bg="black",
                            relief="sunken", borderwidth=5)
    levSkillframe.grid(row=0, column=0)
    label = tk.Label(master=levSkillframe,
                     text=f"Level: {level}", background="black", foreground="lime", font="Gothic 8")
    label.grid(row=0, column=0, sticky="W")
    label = tk.Label(master=levSkillframe,
                     text=f"Current EXP: {currentxp}", background="black", foreground="lime", font="Gothic 8")
    label.grid(row=1, column=0, sticky="W")
    label = tk.Label(master=levSkillframe,
                     text=f"Next Level: {targetxp}", background="black", foreground="lime", font="Gothic 8")
    label.grid(row=2, column=0, sticky="W")
    button = tk.Button(master=levelframe, background=brown, foreground="yellow",
                       relief="raised", text="Lvl Up", font="Gothic", command=Levelupscreen)
    button.grid(row=0, column=1, sticky="NSEW")
    return




GenerateLevelFrame(levelstuff[0], levelstuff[1], levelstuff[2])

# Skills frame

skillsframe = tk.Frame(master=topframe, bg="black",
                       borderwidth=5, relief="sunken")
skillsframe.grid(row=0, column=1, sticky="NWE")



AllFrame = tk.Frame(master=topframe, borderwidth=5, bg=brown)
AllFrame.grid(row=1, column=1, sticky="SWE")

skillItems = ["Small Guns", "Big Guns", "Energy Weapons", "Explosives", "Unarmed", "Melee Weapons", "Throwing",
              "First aid", "Surgeon", "Sneak", "Lockpick", "Steal", "Traps", "Science", "Repair", "Speech", "Barter", "Survival"]



def SkillsFrame():
    global AllFrame
    for widget in skillsframe.winfo_children():
        widget.destroy()
    for widget in AllFrame.winfo_children():
        widget.destroy()
        
    skilladjfinal = [x + y for x, y in zip(skillallocated, skilladj)]
    SkillValues(*skilladjfinal)
    for i in range(len(skillItems)):
        label = tk.Label(
            master=skillsframe, text=f"{skillItems[i]}: {skillvalues[i]}", bg="black", fg="lime", font="Gothic 8")
        label.grid(row=i, column=0, sticky="W")

    label = tk.Label(master=AllFrame, bg="black", fg="lime", relief="sunken",
                     text=f"Skill Points to Allocate: {AvailablePoints}", borderwidth=5)
    label.grid(row=0, column=0, sticky="NEW")
    button = tk.Button(master=AllFrame, bg=brown, fg="yellow", borderwidth=5,
                       relief="raised", command=AllocatePointsScreen, text="Allocate Points")
    button.grid(row=1, column=0, sticky="NEW")


PointsButtonLoc = []


def AllocatePointsScreen():
    global skillItems
    global PointsWindow
    global TextFrame1
    global Textframe2
    global ButtonFrame
    PointsWindow = tk.Tk()
    PointsWindow.configure(bg=brown)
    TextFrame1 = tk.Frame(master=PointsWindow, bg="black",
                          borderwidth=5, relief="sunken")
    TextFrame1.grid(row=0, column=0, sticky="NSEW")
    ButtonFrame = tk.Frame(master=PointsWindow, bg=brown, borderwidth=5)
    ButtonFrame.grid(row=0, column=1, sticky="NSEW")
    Textframe2 = tk.Frame(master=PointsWindow, bg=brown)
    Textframe2.grid(row=1, column=0)
    button = tk.Button(master=Textframe2, bg=brown, fg="yellow",
                       relief="raised", text="OK", command=PointsWindow.destroy)
    button.grid(row=0, column=1, sticky="NSEW")
    GeneratePointsPopup()


def GeneratePointsPopup():
    global PointsWindow
    global TextFrame1
    global Textframe2
    global ButtonFrame
    global skillItems
    global skillvalues
    global AvailablePoints
    PointsButtonLoc.clear()
    skilladjfinal = [x + y for x, y in zip(skillallocated, skilladj)]
    SkillValues(*skilladjfinal)
    for i in range(len(skillvalues)):
        label = tk.Label(master=TextFrame1, bg="black", fg="lime",
                         text=f"{skillItems[i]}: {skillvalues[i]}", font="Gothic 15")
        label.grid(row=i, column=0, sticky="NSEW")
        ButtonMiniFrame = tk.Frame(master=ButtonFrame, bg="brown")
        ButtonMiniFrame.grid(row=i, column=0)
        button = tk.Button(master=ButtonMiniFrame, bg=brown,
                           fg="yellow", text="+", font="Gothic 11")
        button.bind("<Button-1>", SkillChange)
        button.grid(row=0, column=0, sticky="NSEW")
        PointsButtonLoc.append(button.winfo_id())
        button = tk.Button(master=ButtonMiniFrame, bg=brown,
                           fg="yellow", text="-", font="Gothic 11")
        button.bind("<Button-1>", SkillChange)
        button.grid(row=0, column=1, sticky="NSEW")
        PointsButtonLoc.append(button.winfo_id())
    label = tk.Label(master=Textframe2, bg="black", fg="lime",
                     text=f"Skill Points to Allocate: {AvailablePoints}", relief="sunken")
    label.grid(row=0, column=0, sticky="NSEW")


def SkillChange(event):
    global PointsWindow
    global TextFrame1
    global ButtonFrame
    global AvailablePoints
    WhichButton = PointsButtonLoc.index(event.widget.winfo_id())
    i = WhichButton//2
    if WhichButton % 2 == 0:
        skillallocated[i] = skillallocated[i]+1
        AvailablePoints = AvailablePoints-1
    else:
        skillallocated[i] = skillallocated[i]-1
        AvailablePoints = AvailablePoints+1
    GeneratePointsPopup()
    SkillsFrame()


# def IncrementSkill(skillItem, PointsWindow,TextFrame1,ButtonFrame):
#     global skilladj
#     global skillItems
#     global AvailablePoints
#     i = skillItems.index(skillItem)
#     skilladj[i] = skilladj[i]+1
#     AvailablePoints = AvailablePoints-1
#     for widget in TextFrame1.winfo_children():
#         widget.destroy()
#     for widget in ButtonFrame.winfo_children():
#         widget.destroy()
#     GeneratePointsPopup(PointsWindow, TextFrame1, ButtonFrame)
#     return

# def DecrementSkill(skillItem, PointsWindow,TextFrame1,ButtonFrame):
#     global skilladj
#     global skillItems
#     global AvailablePoints
#     i = skillItems.index(skillItem)
#     skilladj[i] = skilladj[i]-1
#     AvailablePoints = AvailablePoints+1
#     for widget in TextFrame1.winfo_children():
#         widget.destroy()
#     for widget in ButtonFrame.winfo_children():
#         widget.destroy()
#     GeneratePointsPopup(PointsWindow, TextFrame1, ButtonFrame)
#     return


def SkillValues(SGA=0, BGA=0, EWA=0, EXA=0, UNA=0, MWA=0, THA=0, FAA=0, SRA=0, SNA=0, LPA=0, STA=0, TRA=0, SCA=0, REA=0, SPA=0, BAA=0, SUA=0):
    print(SGA)
    global skillvalues
    skillvalues[0] = (35+specSkills[5]+SGA)
    skillvalues[1] = (10+specSkills[5]+BGA)
    skillvalues[2] = (10+specSkills[5]+EWA)
    skillvalues[3] = (ceil(2+(2*specSkills[1])+(specSkills[6]/2))+EXA)
    skillvalues[4] = (ceil(65+(specSkills[5]+specSkills[0])/2)+UNA)
    skillvalues[5] = (ceil(55+(specSkills[5]+specSkills[0])/2)+MWA)
    skillvalues[6] = (40+specSkills[5]+THA)
    skillvalues[7] = (ceil(30+(specSkills[1]+specSkills[4])/2)+FAA)
    skillvalues[8] = (ceil(15+(specSkills[1]+specSkills[4])/2)+SRA)
    skillvalues[9] = (25+specSkills[5]+SNA)
    skillvalues[10] = (ceil(20+(specSkills[5]+specSkills[1])/2)+LPA)
    skillvalues[11] = (20+specSkills[5]+STA)
    skillvalues[12] = (ceil(20+(specSkills[5]*specSkills[1])/2)+TRA)
    skillvalues[13] = (25+2*specSkills[4]+SCA)
    skillvalues[14] = (20+specSkills[4]+REA)
    skillvalues[15] = (25+2*specSkills[3]+SPA)
    skillvalues[16] = (20+2*specSkills[3]+BAA)
    skillvalues[17] = (2+2*specSkills[2]+ceil(specSkills[6]/2)+SUA)
    return


# Armour frame stuff
ArmourFrame = tk.Frame(master=topframe, background=brown, borderwidth=5)
ArmourFrame.grid(row=0, column=2, sticky="n")
ArmourImage = ImageTk.PhotoImage(Image.open("ArmourCard.png"))
LeftArmour = tk.Frame(master=ArmourFrame, bg=brown)
LeftArmour.grid(row=0, column=0, sticky="NS")
label = tk.Label(master=ArmourFrame, image=ArmourImage,
                 borderwidth=5, relief="sunken", bg="black")
label.grid(row=0, column=1)
RightArmour = tk.Frame(master=ArmourFrame, bg=brown)
RightArmour.grid(row=0, column=2, sticky="NS")
LArmFrames = []
LButtons = []
RButtons = []
RArmFrames = []

LArmour_Skills = []
RArmour_Skills = []
LBodyParts = ["Head", "Right Arm", "Right Leg", "Groin"]
RBodyParts = ["Eyes", "Torso", "Left Arm", "Left Leg"]


def ArmourSkills():
    LArmour_Skills.clear()
    RArmour_Skills.clear()
    for i in range(len(ArmourWorn)):
        if "None" in ArmourWorn[i]:
            if i <= 3:
                LArmour_Skills.append(("No Armour", 0, 0, "None"))
            else:
                RArmour_Skills.append(("No Armour", 0, 0, "None"))
            continue
        print(f"{ArmourWorn[i]=}")
        ArmType, ArmSlot = ArmourWorn[i].split("-")
        f = open(f"{dirpath}/Armour/{ArmSlot}/{ArmType}.txt", mode="r")
        TheThingy = (f.read()).strip(")(")
        Item, ArmourDT, ArmourDR, spec = (TheThingy).split(",")
        f.close()
        if i <= 3:
            LArmour_Skills.append((Item, ArmourDT, ArmourDR, spec))
        else:
            RArmour_Skills.append((Item, ArmourDT, ArmourDR, spec))


for i in range(4):
    frame = (tk.Frame(master=LeftArmour, pady=0, bg=brown))
    frame.grid(row=i, column=0, sticky="E")
    LArmFrames.append(frame)

for i in range(4):
    frame = (tk.Frame(master=RightArmour, pady=0, bg=brown))
    frame.grid(row=i, column=0, sticky="W")
    RArmFrames.append(frame)

ArmourList = []


def ArmourChangeScreen(event):
    global ArmourList
    global ACS
    global ACSframe
    global var
    ArmourList.clear()
    ACS = tk.Tk()
    ACS.configure(bg=brown)
    Buttons = LButtons+RButtons
    ButtonNum = Buttons.index(event.widget.winfo_id())
    BodyParts = LBodyParts+RBodyParts
    global SpecBodyPart
    SpecBodyPart = BodyParts[ButtonNum]
    label = tk.Label(text=SpecBodyPart, bg="black", fg="lime",
                     font="Gothic 10", master=ACS, relief="sunken", borderwidth=5)
    label.grid(row=0, column=0, sticky="N")
    ACSframe = tk.Frame(master=ACS, bg=brown)
    ACSframe.grid(row=2, column=0, sticky="N")
    print(f"{dirpath=}")
    for i in os.scandir(f"{dirpath}\Armour\{SpecBodyPart}"):
        DirTree = str(i).split("'")
        txt = DirTree[1]
        txt = txt[:(len(txt)-4)]
        ArmourList.append(txt)
    var = tk.StringVar(master=ACS)
    var.set("None")
    var.trace("w", UpdateACS)
    option = tk.OptionMenu(ACS, var, *ArmourList)
    option.configure(bg="black", fg="lime", borderwidth=5, relief="sunken")
    option.grid(row=1, column=0, sticky="N")
    labellist = ["Item:", "DT:", "DR:", "Special Effect:"]
    for i in labellist:
        label = tk.Label(text=f"{i} None", bg="black", fg="lime",
                         font="Gothic 10", relief="sunken", borderwidth=5, master=ACSframe)
        label.grid(row=labellist.index(i), column=0, sticky="W")


def UpdateACS(*stuff):
    for widget in ACSframe.winfo_children():
        widget.destroy()
    labellist = ["Item:", "DT:", "DR:", "Special Effect:"]
    with open(f"Armour\{SpecBodyPart}\{var.get()}.txt") as f:
        ArmSkillList = f.read().strip(')(').split(',')
        ArmSkillList = [str(i) for i in ArmSkillList]
    for i in range(len(labellist)):

        label = tk.Label(text=f"{labellist[i]} {ArmSkillList[i]}", font="Gothic 10", relief="sunken",
                         borderwidth=2, master=ACSframe, background="black", foreground="lime")
        label.grid(row=i, column=0, sticky="W")

    BodyParts = LBodyParts+RBodyParts
    ArmourWorn[BodyParts.index(SpecBodyPart)] = f"{var.get()}-{SpecBodyPart}"
    ArmourFrameGen()


def ArmourFrameGen():
    LButtons.clear()
    RButtons.clear()
    ArmourSkills()
    for i in range(4):
        for widget in LArmFrames[i].winfo_children():
            widget.destroy()
        for widget in RArmFrames[i].winfo_children():
            widget.destroy()
        button = tk.Button(master=LArmFrames[i], bg="black", fg="lime",
                           text=f"{LBodyParts[i]} \n{LArmour_Skills[i][0]} \nDT: {LArmour_Skills[i][1]} \nDR: {LArmour_Skills[i][2]} \nEffects: {LArmour_Skills[i][3]}", relief="sunken", font="Gothic 10", justify="left", borderwidth=5)
        button.grid(row=0, column=0)
        LButtons.append(button.winfo_id())
        button.bind("<Button-1>", ArmourChangeScreen)
        button = tk.Button(master=RArmFrames[i], bg="black", fg="lime",
                           text=f"{RBodyParts[i]} \n{RArmour_Skills[i][0]} \nDT: {RArmour_Skills[i][1]} \nDR: {RArmour_Skills[i][2]} \nEffects: {LArmour_Skills[i][3]}", relief="sunken", font="Gothic 10", justify="left", borderwidth=5)
        button.grid(row=0, column=0)
        RButtons.append(button.winfo_id())
        button.bind("<Button-1>", ArmourChangeScreen)


ArmourFrameGen()

# Perks


PerksFrame = tk.Frame(master=topframe, bg=brown, borderwidth=5)
PerksFrame.grid(row=0, column=3, sticky="n")

label = tk.Label(master=PerksFrame, bg=brown, fg="yellow",
                 relief="groove", text="Perks", font="Gothic 20")
label.grid(row=0, column=0, sticky="NEW")

PerksStuff = tk.Frame(master=PerksFrame, bg="black",
                      borderwidth=5, relief="groove")
PerksStuff.grid(row=1, column=0, sticky="NSEW")

PerksItems = tk.Frame(master=PerksStuff, bg="black")
PerksItems.grid(row=0, column=0, sticky="w")

PerksSkills = tk.Frame(master=PerksStuff, bg="black")
PerksSkills.grid(row=0, column=1, sticky="e")

# Add perks button


def NewPerk():
    NewPerkWin = tk.Tk()
    NewPerkWin.configure(bg=brown)

    def ClosePerkWin():
        with open("perks.txt", "a") as f:
            f.write(f"\n({Item.get()},{Skill.get()})")
        Update()
        NewPerkWin.destroy()

    LabelPerk = tk.Label(master=NewPerkWin, bg=brown, fg="yellow",
                         relief="groove", text="New Perk", font="Gothic 10")
    LabelPerk.grid(row=0, column=0)

    Colframe = tk.Frame(master=NewPerkWin, bg=brown)
    Colframe.grid(row=1, column=0)

    ItemFrame = tk.Frame(master=Colframe, bg="black",
                         borderwidth=5, relief="sunken")
    ItemFrame.grid(row=0, column=0)

    SkillFrame = tk.Frame(master=Colframe, bg="black",
                         borderwidth=5, relief="sunken")
    SkillFrame.grid(row=0, column=1)

    ExitButton = tk.Button(master=NewPerkWin, bg=brown, fg="yellow",
                           relief="groove", text="Save", font="Gothic 10", command=ClosePerkWin)
    ExitButton.grid(row=2, column=0)

    ItemLabel = tk.Label(master=ItemFrame, bg="black", fg="lime", text="Item")
    ItemLabel.grid(row=0, column=0)

    SkillLabel = tk.Label(master=SkillFrame, bg="black",
                         fg="lime", text="Modifier")
    SkillLabel.grid(row=0, column=0)

    Item = tk.StringVar(master=NewPerkWin)
    Skill = tk.StringVar(master=NewPerkWin)

    ItemEntry = tk.Entry(master=ItemFrame, textvariable=Item)
    ItemEntry.grid(row=1, column=0)

    SkillEntry = tk.Entry(master=SkillFrame, textvariable=Skill)
    SkillEntry.grid(row=1, column=0)


AddPerkButton = tk.Button(master=PerksFrame, bg=brown, fg="yellow",
                          relief="groove", text="New Perk", font="Gothic 10", command=NewPerk)
AddPerkButton.grid(row=2, column=0)


def PerksFrameGen():
    with open("perks.txt") as f:
        PerksList = f.read().split("\n")
    for widget in PerksItems.winfo_children():
        widget.destroy()
    for widget in PerksSkills.winfo_children():
        widget.destroy()
    for perks in PerksList:
        PerkStuff = perks.strip(")(").split(",")
        print(f"{PerkStuff =}")
        label = tk.Label(master=PerksItems, bg="black", fg="lime",
                         font="Gothic 8", text=PerkStuff[0], anchor="w")
        label.grid(row=PerksList.index(perks), column=0, sticky="w")
        label = tk.Label(master=PerksSkills, bg="black", fg="lime",
                         font="Gothic 8", text=PerkStuff[1], anchor="e")
        label.grid(row=PerksList.index(perks), column=0, sticky="e")

# Perk Bonuses cause change in Skills


# def PerkCheck():
#     global specbonus
#     AA0,AA1,AA2,AA3,AA4,AA5,AA6,AA7,AA8,AA9,AA10,AA11,AA12,AA13,AA14,AA15,AA16,AA17,AA18,AA19,AA20,AA21,AA22,AA23,AA24 = (0,)*25
#     specbonus = 0
#     with open("perks.txt") as f:
#         PerksList = f.read().split("\n")
#     for perks in PerksList:
#         PerkStuff = perks.strip(")(").split(",")
#         if "small" in PerkStuff[1].lower():
#             SGA = re.findall(r"\d+", PerkStuff[1])
#             skilladj[0] = skilladj[0] + int(SGA[0]) - AA0
#             AA0 += int(SGA[0])
#         elif "big" in PerkStuff[1].lower():
#             ADJ = re.findall(r"\d+", PerkStuff[1])
#             skilladj[1] = skilladj[1] + int(ADJ[0]) - AA1
#             AA1 += int(ADJ[0])
#         elif "energy" in PerkStuff[1].lower():
#             ADJ = re.findall(r"\d+", PerkStuff[1])
#             skilladj[2] = skilladj[2] + int(ADJ[0])
#         elif "explosives" in PerkStuff[1].lower():
#             ADJ = re.findall(r"\d+", PerkStuff[1])
#             skilladj[3] = skilladj[3] + int(ADJ[0])
#         elif "unarmed" in PerkStuff[1].lower():
#             ADJ = re.findall(r"\d+", PerkStuff[1])
#             skilladj[4] = skilladj[4] + int(ADJ[0])
#         elif "melee" in PerkStuff[1].lower():
#             ADJ = re.findall(r"\d+", PerkStuff[1])
#             skilladj[5] = skilladj[5] + int(ADJ[0])
#         elif "throwing" in PerkStuff[1].lower():
#             ADJ = re.findall(r"\d+", PerkStuff[1])
#             skilladj[6] = skilladj[6] + int(ADJ[0])
#         elif "first" in PerkStuff[1].lower():
#             ADJ = re.findall(r"\d+", PerkStuff[1])
#             skilladj[7] += int(ADJ[0])
#         elif "surgeon" in PerkStuff[1].lower():
#             ADJ = re.findall(r"\d+", PerkStuff[1])
#             skilladj[8] += int(ADJ[0])
#         elif "sneak" in PerkStuff[1].lower():
#             ADJ = re.findall(r"\d+", PerkStuff[1])
#             skilladj[9] += int(ADJ[0])
#         elif "lockpick" in PerkStuff[1].lower():
#             ADJ = re.findall(r"\d+", PerkStuff[1])
#             skilladj[10] += int(ADJ[0])
#         elif "steal" in PerkStuff[1].lower():
#             ADJ = re.findall(r"\d+", PerkStuff[1])
#             skilladj[11] += int(ADJ[0])
#         elif "traps" in PerkStuff[1].lower():
#             ADJ = re.findall(r"\d+", PerkStuff[1])
#             skilladj[12] += int(ADJ[0])
#         elif "science" in PerkStuff[1].lower():
#             ADJ = re.findall(r"\d+", PerkStuff[1])
#             skilladj[13] += int(ADJ[0])
#         elif "repair" in PerkStuff[1].lower():
#             ADJ = re.findall(r"\d+", PerkStuff[1])
#             skilladj[14] += int(ADJ[0])
#         elif "speech" in PerkStuff[1].lower():
#             ADJ = re.findall(r"\d+", PerkStuff[1])
#             skilladj[15] += int(ADJ[0])
#         elif "barter" in PerkStuff[1].lower():
#             ADJ = re.findall(r"\d+", PerkStuff[1])
#             skilladj[16] += int(ADJ[0])
#         elif "survival" in PerkStuff[1].lower():
#             ADJ = re.findall(r"\d+", PerkStuff[1])
#             skilladj[17] += int(ADJ[0])
#         elif "crit" in PerkStuff[1].lower():
#             ADJ = re.findall(r"\d+", PerkStuff[1])
#             resvalues[6] += int(ADJ[0])/100
#         elif "initiative" in PerkStuff[1].lower():
#             ADJ = re.findall(r"\d+", PerkStuff[1])
#             resvalues[5] += int(ADJ[0])
#         elif "radiation" in PerkStuff[1].lower():
#             ADJ = re.findall(r"\d+", PerkStuff[1])
#             resvalues[4] += int(ADJ[0])/100
#         elif "poison" in PerkStuff[1].lower():
#             ADJ = re.findall(r"\d+", PerkStuff[1])
#             resvalues[3] += int(ADJ[0])/100
#         elif "damage" in PerkStuff[1].lower():
#             ADJ = re.findall(r"\d+", PerkStuff[1])
#             resvalues[2] += int(ADJ[0])/100
#         elif "carry" in PerkStuff[1].lower():
#             ADJ = re.findall(r"\d+", PerkStuff[1])
#             resvalues[1] += int(ADJ[0])
#         elif "ap" in PerkStuff[1].lower():
#             ADJ = re.findall(r"\d+", PerkStuff[1])
#             resvalues[0] += int(ADJ[0])
#         elif "special" in PerkStuff[1].lower():
#             ADJ = re.findall(r"\d+", PerkStuff[1])
#             specbonus += int(ADJ[0])


# USED AI TO COMPLETE THIS
AA0, AA1, AA2, AA3, AA4, AA5, AA6, AA7, AA8, AA9, AA10, AA11, AA12, AA13, AA14, AA15, AA16, AA17, AA18, AA19, AA20, AA21, AA22, AA23, AA24, AA25 = (0,)*26

def PerkCheck():
    global specbonus
    global AA0, AA1, AA2, AA3, AA4, AA5, AA6, AA7, AA8, AA9, AA10, AA11, AA12, AA13, AA14, AA15, AA16, AA17, AA18, AA19, AA20, AA21, AA22, AA23, AA24, AA25 
    print(f"{skilladj=}")
    print(f"{resvalues=}")

    with open("perks.txt") as f:
        PerksList = f.read().split("\n")
    
    print(f"{AA25=}")
    skilladj[0] -= AA0
    skilladj[1] -= AA1
    skilladj[2] -= AA2
    skilladj[3] -= AA3
    skilladj[4] -= AA4
    skilladj[5] -= AA5
    skilladj[6] -= AA6
    skilladj[7] -= AA7
    skilladj[8] -= AA8
    skilladj[9] -= AA9
    skilladj[10] -= AA10
    skilladj[11] -= AA11
    skilladj[12] -= AA12
    skilladj[13] -= AA13
    skilladj[14] -= AA14
    skilladj[15] -= AA15
    skilladj[16] -= AA16
    skilladj[17] -= AA17
    resvalues[6] -= AA18 / 100
    resvalues[5] -= AA19
    resvalues[4] -= AA20 / 100
    resvalues[3] -= AA21 / 100
    resvalues[2] -= AA22 / 100
    resvalues[1] -= AA23
    resvalues[0] -= AA24
    specbonus -= AA25
    
    AA0, AA1, AA2, AA3, AA4, AA5, AA6, AA7, AA8, AA9, AA10, AA11, AA12, AA13, AA14, AA15, AA16, AA17, AA18, AA19, AA20, AA21, AA22, AA23, AA24, AA25 = (0,)*26
    
    for perks in PerksList:
        
        PerkStuff = perks.strip(")(").split(",")
        print(f"{PerkStuff[1].lower() = }")
        if "small" in PerkStuff[1].lower():
            SGA = re.findall(r"\d+", PerkStuff[1])
            skilladj[0] = skilladj[0] + int(SGA[0])
            AA0 += int(SGA[0])
        elif "big" in PerkStuff[1].lower():
            ADJ = re.findall(r"\d+", PerkStuff[1])
            skilladj[1] = skilladj[1] + int(ADJ[0])
            AA1 += int(ADJ[0])
        elif "energy" in PerkStuff[1].lower():
            ADJ = re.findall(r"\d+", PerkStuff[1])
            skilladj[2] = skilladj[2] + int(ADJ[0])
            AA2 += int(ADJ[0])
        elif "explosives" in PerkStuff[1].lower():
            ADJ = re.findall(r"\d+", PerkStuff[1])
            skilladj[3] = skilladj[3] + int(ADJ[0])
            AA3 += int(ADJ[0])
        elif "unarmed" in PerkStuff[1].lower():
            ADJ = re.findall(r"\d+", PerkStuff[1])
            skilladj[4] = skilladj[4] + int(ADJ[0])
            AA4 += int(ADJ[0])
        elif "melee" in PerkStuff[1].lower():
            ADJ = re.findall(r"\d+", PerkStuff[1])
            skilladj[5] = skilladj[5] + int(ADJ[0])
            AA5 += int(ADJ[0])
        elif "throwing" in PerkStuff[1].lower():
            ADJ = re.findall(r"\d+", PerkStuff[1])
            skilladj[6] = skilladj[6] + int(ADJ[0])
            AA6 += int(ADJ[0])
        elif "first" in PerkStuff[1].lower():
            ADJ = re.findall(r"\d+", PerkStuff[1])
            skilladj[7] = skilladj[7] + int(ADJ[0])
            AA7 += int(ADJ[0])
        elif "surgeon" in PerkStuff[1].lower():
            ADJ = re.findall(r"\d+", PerkStuff[1])
            skilladj[8] = skilladj[8] + int(ADJ[0])
            AA8 += int(ADJ[0])
        elif "sneak" in PerkStuff[1].lower():
            ADJ = re.findall(r"\d+", PerkStuff[1])
            skilladj[9] = skilladj[9] + int(ADJ[0])
            AA9 += int(ADJ[0])
        elif "lockpick" in PerkStuff[1].lower():
            ADJ = re.findall(r"\d+", PerkStuff[1])
            skilladj[10] = skilladj[10] + int(ADJ[0])
            AA10 += int(ADJ[0])
        elif "steal" in PerkStuff[1].lower():
            ADJ = re.findall(r"\d+", PerkStuff[1])
            skilladj[11] = skilladj[11] + int(ADJ[0])
            AA11 += int(ADJ[0])
        elif "traps" in PerkStuff[1].lower():
            ADJ = re.findall(r"\d+", PerkStuff[1])
            skilladj[12] = skilladj[12] + int(ADJ[0])
            AA12 += int(ADJ[0])
        elif "science" in PerkStuff[1].lower():
            ADJ = re.findall(r"\d+", PerkStuff[1])
            skilladj[13] = skilladj[13] + int(ADJ[0])
            AA13 += int(ADJ[0])
        elif "repair" in PerkStuff[1].lower():
            ADJ = re.findall(r"\d+", PerkStuff[1])
            skilladj[14] = skilladj[14] + int(ADJ[0])
            AA14 += int(ADJ[0])
        elif "speech" in PerkStuff[1].lower():
            ADJ = re.findall(r"\d+", PerkStuff[1])
            skilladj[15] = skilladj[15] + int(ADJ[0])
            AA15 += int(ADJ[0])
        elif "barter" in PerkStuff[1].lower():
            ADJ = re.findall(r"\d+", PerkStuff[1])
            skilladj[16] = skilladj[16] + int(ADJ[0])
            AA16 += int(ADJ[0])
        elif "survival" in PerkStuff[1].lower():
            ADJ = re.findall(r"\d+", PerkStuff[1])
            skilladj[17] = skilladj[17] + int(ADJ[0])
            AA17 += int(ADJ[0])
        elif "crit" in PerkStuff[1].lower():
            ADJ = re.findall(r"\d+", PerkStuff[1])
            resvalues[6] = resvalues[6] + int(ADJ[0])/100
            AA18 += int(ADJ[0])
        elif "initiative" in PerkStuff[1].lower():
            ADJ = re.findall(r"\d+", PerkStuff[1])
            resvalues[5] = resvalues[5] + int(ADJ[0])
            AA19 += int(ADJ[0])
        elif "radiation" in PerkStuff[1].lower():
            ADJ = re.findall(r"\d+", PerkStuff[1])
            resvalues[4] = resvalues[4] + int(ADJ[0])/100
            AA20 += int(ADJ[0])
        elif "poison" in PerkStuff[1].lower():
            ADJ = re.findall(r"\d+", PerkStuff[1])
            resvalues[3] = resvalues[3] + int(ADJ[0])/100
            AA21 += int(ADJ[0])
        elif "damage" in PerkStuff[1].lower():
            ADJ = re.findall(r"\d+", PerkStuff[1])
            resvalues[2] = resvalues[2] + int(ADJ[0])/100
            AA22 += int(ADJ[0])
        elif "carry" in PerkStuff[1].lower():
            ADJ = re.findall(r"\d+", PerkStuff[1])
            resvalues[1] = resvalues[1] + int(ADJ[0])
            AA23 += int(ADJ[0])
        elif "ap" in PerkStuff[1].lower():
            ADJ = re.findall(r"\d+", PerkStuff[1])
            resvalues[0] = resvalues[0] + int(ADJ[0])
            AA24 += int(ADJ[0])
        elif "special" in PerkStuff[1].lower():
            ADJ = re.findall(r"\d+", PerkStuff[1])
           # print(f"Before stuff {specbonus =}, {AA25=}")
            specbonus += (int(ADJ[0]))
            AA25 += int(ADJ[0])
           # print(f"{specbonus =}, {AA25=}")
    

#ITEM INVENTORY SHITE

def NewItem():
    NewInvWin = tk.Tk()
    NewInvWin.configure(bg=brown)

    def CloseInvWin():
        with open("inventory.txt", "a") as f:
            f.write(f"\n[{Item.get()},{Amount.get()},{Value.get()}]")
        Update()
        NewInvWin.destroy()

    LabelPerk = tk.Label(master=NewInvWin, bg=brown, fg="yellow",
                          relief="groove", text="New Item", font="Gothic 10")
    LabelPerk.grid(row=0, column=0)

    Colframe = tk.Frame(master=NewInvWin, bg=brown)
    Colframe.grid(row=1, column=0)

    ItemFrame = tk.Frame(master=Colframe, bg="black",
                          borderwidth=5, relief="sunken")
    ItemFrame.grid(row=0, column=0)

    AmountFrame = tk.Frame(master=Colframe, bg="black",
                          borderwidth=5, relief="sunken")
    AmountFrame.grid(row=0, column=1)
    
    ValueFrame = tk.Frame(master=Colframe, bg="black",
                          borderwidth=5, relief="sunken")
    ValueFrame.grid(row=0, column=2)

    ExitButton = tk.Button(master=NewInvWin, bg=brown, fg="yellow",
                            relief="groove", text="Save", font="Gothic 10", command=CloseInvWin)
    ExitButton.grid(row=2, column=0)

    ItemLabel = tk.Label(master=ItemFrame, bg="black", fg="lime", text="Item")
    ItemLabel.grid(row=0, column=0)

    AmountLabel = tk.Label(master=AmountFrame, bg="black",
                          fg="lime", text="Amount")
    AmountLabel.grid(row=0, column=0)
    
    ValueLabel = tk.Label(master=ValueFrame, bg="black",
                          fg="lime", text="Value")
    ValueLabel.grid(row=0, column=0)

    Item = tk.StringVar(master=NewInvWin)
    Amount = tk.StringVar(master=NewInvWin)
    Value = tk.StringVar(master=NewInvWin)

    ItemEntry = tk.Entry(master=ItemFrame, textvariable=Item)
    ItemEntry.grid(row=1, column=0)

    AmountEntry = tk.Entry(master=AmountFrame, textvariable=Amount)
    AmountEntry.grid(row=1, column=0)        
    
    ValueEntry = tk.Entry(master=ValueFrame, textvariable=Value)
    ValueEntry.grid(row=1, column=0)     

AllInvShit = tk.Frame(master=window, bg=brown, borderwidth=5)
AllInvShit.grid(row=1,column=0, sticky="w")
InvFrame = tk.Frame(master=AllInvShit, bg="black", borderwidth=10, relief="sunken")
InvFrame.grid(row=2, column=0, sticky="w")
InvLabel = tk.Button(master=AllInvShit, text="Inventory", bg=brown, fg="yellow", relief="raised", font="Gothic 20", borderwidth=5, command = NewItem)
InvLabel.grid(row=1,column=0,sticky="w")
Items = tk.Frame(master=InvFrame,bg="black",borderwidth = 5)
Items.grid(row=0,column=0,sticky="nsew")
Amount = tk.Frame(master=InvFrame,bg="black",borderwidth = 5)
Amount.grid(row=0,column=1,sticky="nsew")
Value = tk.Frame(master=InvFrame,bg="black",borderwidth = 5)
Value.grid(row=0,column=2,sticky="nsew")
InvFList = (Items,Amount,Value)
InvButtonIDs=[]

def GenerateInventoryScreen():
    InvButtonIDs.clear()
    for frame in InvFrame.winfo_children():   
       for widget in frame.winfo_children():
           widget.destroy()
    with open("inventory.txt") as f:
        inventory = f.read()
    InvList = inventory.split("\n")
    InvList = [i.strip('][').split(',') for i in InvList]
    
    label=tk.Label(text="Item", master = Items , bg="black", fg="lime", font="Gothic 10", justify="center")
    label.grid(row=0,column=1)
    
    label=tk.Label(text="Amount", master = Amount , bg="black", fg="lime", font="Gothic 10", justify="center")
    label.grid(row=0,column=1)
    
    label=tk.Label(text="Value", master = Value , bg="black", fg="lime", font="Gothic 10", justify="center")
    label.grid(row=0,column=1)
    
    for i in range(len(InvList)):
        for j in InvList[i]:
            label = tk.Label(text = j, master = InvFList[InvList[i].index(j)], bg="black", fg="lime", font="Gothic 10", justify="center")
            label.grid(row=(i+1),column=1)
        button = tk.Button(font="Gothic 8", text="+", master = Amount, bg="black", fg="lime")
        button.bind("<Button-1>", InvClick)
        button.grid(row=(i+1),column=2)
        InvButtonIDs.append(button.winfo_id())
        button = tk.Button(font="Gothic 8", text="-", master = Amount, bg="black", fg="lime")
        button.bind("<Button-1>", InvClick)
        button.grid(row=(i+1),column=0)
        InvButtonIDs.append(button.winfo_id())
            
def InvClick(event):
    widget_id = event.widget.winfo_id()
    WhichButton = InvButtonIDs.index(widget_id)
    ItemCount = WhichButton//2
    NewInventory = []
    with open("inventory.txt") as f:
        inventory = f.read()
    InvList = inventory.split("\n")
    InvList = [i.strip('][').split(',') for i in InvList]
    InvList[ItemCount][1] = int(InvList[ItemCount][1])
    if WhichButton % 2 == 0:
        InvList[ItemCount][1] += 1 
    else:
        InvList[ItemCount][1] -= 1 
    
    InvList = [str(i) for i in InvList]
    NewInventory = "\n".join(InvList)
    NewInventory = NewInventory.replace('"','')
    NewInventory = NewInventory.replace("'",'')
    NewInventory = NewInventory.replace(" ","")
    with open("inventory.txt","w") as f:
        f.write(NewInventory)
    Update()
        


def Update():
    GenerateResistancesFrame()
    PerkCheck()
    updatespecial("0 0")
    
    PerksFrameGen()
    SkillsFrame()
    GenerateHPFrame()
    GenerateInventoryScreen()
    

remainingframe = tk.Frame(master=topleft, bg=brown)
remainingframe.grid(row=1, column=0)
label = tk.Button(master=remainingframe, bg=brown, fg="yellow",
                 relief="groove", text="Points \n Available", font="Gothic 10", command=Update)
label.grid(row=0, column=0, sticky="W")
label = tk.Label(master=remainingframe, bg="black", fg="lime",  borderwidth=5,
                 relief="sunken", text=RemSpecPoints, font="Gothic 10", width=2, height=1)
label.grid(row=0, column=1)


Update()
PerkCheck()
SkillsFrame()
def on_closing():
    global specSkills
    global Skilluseffectsresults
    global levelstuff
    global skillvalues
    global AvailablePoints
    global ArmourWorn
    Skilluseffectsresults = [int(i) for i in Skilluseffectsresults]
    InfoList = [specSkills, Skilluseffectsresults, levelstuff, skillallocated, ([0,]*18), [AvailablePoints], ArmourWorn]
    for i in InfoList:
        i = [str(j) for j in i]
    
    InfoList = [str(mylist) for mylist in InfoList ]
    Output = "\n".join(InfoList)
    
    with open("stats.txt","w") as f:
    
        f.write(Output)
    print("Wrote to stats.txt")    
    window.destroy()
    
    
window.protocol("WM_DELETE_WINDOW", on_closing)

window.mainloop()
