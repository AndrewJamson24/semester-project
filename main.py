from chess_engine import *
from tkinter import *
from time import sleep, time
from tools import *
import sys
import pyttsx3


option_sound = True
voice = pyttsx3.init()


def speak(text):
    global engine
    if option_sound:
        voice.say(text)
        voice.runAndWait()


def verification():
    """verify if there is a checkmate, a draw..."""
    global phase
    if coord.is_checkmate():
        phase = 0
        w.create_text(320, 360, text="checkmate", font="Times 30", fill="red")
        if engine not in [None, "chess-engine"]:
            try:
                engine.quit()
            except:
                pass
        if music:
            try:
                os.system("endgame.mp3")
            except:
                pass
    elif coord.is_stalemate():
        phase = 0
        w.create_text(320, 320, text="DRAW", font="Times 30", fill="orange")
        if engine not in [None, "chess-engine"]:
            try:
                engine.quit()
            except:
                pass
        if music:
            try:
                os.system("endgame.mp3")
            except:
                pass
        Btn = Button(tk, text="Back to the menu", command=main)
        Btn.pack()
    elif coord.can_claim_draw():
        w.create_text(320, 320, text="DRAW?", font="Times 30", fill="orange", tag="pieces")


def Draw(turn):
    """'drawing' the board"""
    global last_move
    if engine==None:
        tk.title("Chess: "+mode+" mode")
    else:
        if coord.move_stack!=[]:
            tk.title("Chess: "+mode+" "+Engine+" "+str(coord.move_stack[-1]))
        else:
            tk.title("Chess: "+mode+" "+Engine)
    tk.attributes("-topmost", -1)
    w.itemconfigure("pieces", state="hidden")
    d = string_coord(coord)  # from chess_engine.py
    if turn != "white":
        d = d[::-1]
    for i in range(8):
        for j in range(8):
            D=d[i*8+j]
            if D == D.lower():
                w.create_text((j+0.5) * 80,
                              (i + 0.5) * 80,
                              text={
                                  ".":" ", "k":chr(9818),
                                  "q":chr(9819),
                                  "r":chr(9820), "b":chr(9821),
                                  "n":chr(9822),
                                  "p":chr(9823)
                                  }[d[i*8+j]],
                              font="Times 40",
                              tag="pieces")
            else:
                w.create_text((j+0.5) * 80,
                              (i + 0.5) * 80,
                              text={
                                  ".":" ",
                                  "k":chr(9818),
                                  "q":chr(9819),
                                  "r":chr(9820),
                                  "b":chr(9821),
                                  "n":chr(9822),
                                  "p":chr(9823)
                                  }[d[i*8+j].lower()],
                              font="Times 40",
                              fill="#666666",
                              tag="pieces")
    verification()
    if coord.move_stack!=[] and last_move!=coord.move_stack[-1] and music:
        speak(coord.move_stack[-1])
        last_move=coord.move_stack[-1]
    tk.update()


def select0():
    """in all cases"""
    global Btn1, Btn2, click_move, music_opt, music
    Btn1.destroy()
    Btn2.destroy()
    Draw(player)
    click_move = ""
    try:
        music = MusicOption.get()=="on"  # boolean
        music_opt.destroy()
    except:
        pass


def select1():
    """human vs human"""
    global mode, ok
    ok=True
    Btn = Button(tk, text="Back to the menu", command=main)
    Btn.pack()
    mode = "normal"
    select0()


def select2():
    """using AI"""
    global btn, variable, opt
    select0()
    w.create_rectangle(0, 0, 640, 640, fill="black", tag="pieces")
    w.create_text(320, 320, text="Choose the chess engine", font="Times 20", fill="green", tag="pieces")
    variable = StringVar()
    variable.set("")
    engines = ["chess-engine"]
    if "engines" in os.listdir():
        list_engines = []
        for file in os.listdir("engines/"+sys.platform):
            if (".dll" in file) or (".pb" in file):
                pass
            else:
                list_engines.append(file)
        engines += list_engines
    opt = OptionMenu(tk, variable, *engines)
    opt.pack()
    btn = Button(tk, text="Next", command=select3)
    btn.pack()


def select3():
    """using AI -> Next"""
    global btn, engine, opt, Btn1, Btn2, Btn3, level, Engine, time_thinking, engine_opt, EngineOption
    btn.destroy()
    opt.destroy()
    Draw(player)
    w.create_rectangle(0, 0, 640, 640, fill="black", tag="pieces")
    Engine = variable.get()
    if Engine == "chess-engine":
        engine="chess-engine"
        level = Scale(tk, orient="horizontal",
                      from_=0,
                      to=3,
                      resolution=1,
                      tickinterval=10,
                      length=100,
                      label="level(depth)")
        level.pack()
        level.set(2)
    else:
        EngineOption = StringVar()
        engine_opt = Checkbutton(tk,
                            text="play by depth instead of time",
                            variable=EngineOption,
                            onvalue="on",
                            offvalue="off")
        EngineOption.set("on")
        engine_opt.pack()
        if time_is_depth:
            time_thinking = Scale(tk, orient="horizontal", from_=1, to=50, resolution=1, tickinterval=5, length=500, label="depth")
            time_thinking.set(5)
            time_thinking.pack()
        else:
            time_thinking = Scale(tk, orient="horizontal", from_=0.1, to=10, resolution=0.1, tickinterval=1, length=400, label="time thinking")
            time_thinking.set(1)
            time_thinking.pack()
        name = "engines/"+sys.platform+"/"
        engine = chess.engine.SimpleEngine.popen_uci(name+Engine)
    w.create_text(320, 320, text="About the chess engine...", font="Times 20", fill="green", tag="pieces")
    Btn1 = Button(tk, text="Play", command=select3p)
    Btn1.pack()

    if engine!="chess-engine":
        Btn3 = Button(tk, text="chess board analysis", command=select3a)
        Btn3.pack()


def select3p():
    """using AI -> Next -> play"""
    global mode
    mode = "play"
    print(1)
    select4()


def select3a():
    """using AI -> ok -> analysis"""
    global mode, Btn3, ok
    ok = True
    mode = "analysis"
    Btn3.destroy()
    select4()
    Undo = Button(tk, text="undo", command=undo)
    Undo.pack()
    Analyse = Button(tk, text="analyse", command=analyse)
    Analyse.pack()


def select4():
    """using AI -> ok -> bot or play"""
    global Btn1, Btn2, Btn3, level, lvl, opt, variable, time_thinking, time2think, engine_opt
    if engine!="chess-engine":
        time2think = time_thinking.get()
        time_thinking.destroy()
        engine_opt.destroy()
        engine_opt = None
    try:
        lvl = level.get()
        level.destroy()
    except:
        Btn3.destroy()
    select0()
    print(2)
    if mode =="bot" or mode == "play":
        w.create_rectangle(0, 0, 640, 640, fill="black", tag="pieces")
        w.create_text(320, 320, text="Choose who do you want to play", font="Times 20", fill="green", tag="pieces")
        
    if mode != "analysis":
        Btn1 = Button(tk, text="For white", command=select4b)
        Btn1.pack()
        Btn2 = Button(tk, text="For black", command=select4w)
        Btn2.pack()


def select4w():
    """using AI -> ok -> bot or play -> white"""
    global player, book, opt, variable
    book = variable.get()
    opt.destroy()
    player="black"
    select5()


def select4b():
    """using AI -> ok -> bot or play -> black"""
    global player, book, opt, variable
    book = variable.get()
    opt.destroy()
    player="white"
    select5()


def select5():
    """using AI -> ok -> play or bot -> white or black"""
    global Engine, btn, opt, book, variable, WriteOption, write_opt, ok
    book = variable.get()
    opt.destroy()
    select0()
    w.create_text(320, 320, text="Double-Click anywhere to start", font="Times 20", fill="green", tag="pieces")
    Undo = Button(tk, text="undo", command=undo)
    Undo.pack()
    ok=True
    Btn = Button(tk, text="Back to the menu", command=main)
    Btn.pack()


def undo():
    if coord.move_stack!=[]:
        coord.pop()
        if mode=="play" and coord.move_stack!=[]:
            coord.pop()
        Draw(player)


def analyse():
    board = coord.copy()
    play_engine(board, engine, "Nothing", time2think, time_is_depth)
    best = board.move_stack[-1]
    best = engine.play(coord, chess.engine.Limit(time2think)).move
    print(best)
    moves = analyse_position(coord, engine, time2think, time_is_depth)["moves"]
    if best not in moves:
        moves = [best]+moves
    best = str(best)
    w.itemconfigure("analyse", state="hidden")
    for Move in moves:
        if Move in coord.legal_moves:
            move = str(Move)
            x0 = "abcdefgh".find(move[0])*80+40
            x1 = "abcdefgh".find(move[2])*80+40
            y0 = 640-int(move[1])*80+40
            y1 = 640-int(move[3])*80+40
            color = ["blue", "red"][not coord.turn]
            if move == best:
                color = "green"
            w.create_line(x0, y0, x1, y1, fill=color, tag="analyse")
            board = coord.copy()
            board.push_san(move)
            try:
                #if time_is_depth:
                w.create_text(x1, y1, text=str(analyse_position(board, engine, time2think, time_is_depth)["score"].pov(True)), fill=color, font="Times 22", tag="analyse")
                #else:
                #    w.create_text(x1, y1, text=str(analyse_position(board, engine, 0.1, time_is_depth)["score"].pov(True)), fill=color, font="Times 22", tag="analyse")
            except:
                pass
            tk.update()


def click(event):
    """getting the position of the click and moving pieces"""
    global click_move, player, time_is_depth, time_thinking, last_choice
    print(time_is_depth)
    if engine_opt!=None:
        if EngineOption.get()!=last_choice:
            print(last_choice, EngineOption.get())
            last_choice=EngineOption.get()
            time_is_depth = EngineOption.get()=="off"
            tk.update()
            print(time_is_depth, EngineOption.get())
            time_thinking.destroy()
            if time_is_depth:
                time_thinking = Scale(tk, orient="horizontal", from_=1, to=50, resolution=1, tickinterval=5, length=500, label="depth")
                time_thinking.set(5)
                time_thinking.pack()
            else:
                time_thinking = Scale(tk, orient="horizontal", from_=0.1, to=10, resolution=0.1, tickinterval=1, length=400, label="time thinking")
                time_thinking.set(1)
                time_thinking.pack()
    elif mode != "start" and ok:
        if player == "white":
            x = "abcdefgh"[event.x // 80]  # converting the position of the mouse in the square
            y = str(8 - event.y // 80)
        else:
            x = "abcdefgh"[::-1][event.x // 80]
            y = str(-(-event.y // 80))
        click_move += x + str(y)  # adding the new square
        if len(click_move) == 4:  # like 'e2e4' and not just 'e2'
            play_human(click_move)
            play_human(click_move+"q")  # promoting by default the queen for the player
            click_move = ""  # avoiding the situation 'e2e4e7'
            Draw(player)
            if mode == "normal" or mode == "analysis":
                if coord.turn and mode == "normal":  #switching the point of view
                    player = "white"
                if not coord.turn and mode == "normal":
                    player = "black"
                if mode == "analysis":
                    pass
                else:
                    Draw(player)
            elif mode == "play":
                if player == "white" and not coord.turn:
                    if engine == "chess-engine":
                        play_black(coord, lvl, book)
                    else:
                        play_engine(coord, engine, book, time2think, time_is_depth)
                if player == "black" and coord.turn:
                    if engine == "chess-engine":
                        play_white(coord, lvl, book)
                    else:
                        play_engine(coord, engine, book, time2think, time_is_depth)
                verification()
                Draw(player)
        else:
            if player == "white":
                x = "abcdefgh".find(x) * 80  # find the position where the oval can be drawed
                y = (8-int(y)) * 80
            else:
                x = "abcdefgh"[::-1].find(x) * 80
                y = (int(y)-1) * 80
            w.create_oval(x+35, y+35, x+45, y+45, fill="red", tag="pieces")
            tk.update()


def main():
    global engine_opt, time_is_depth, ok, last_move, time2think, MusicOption, music_opt, Btn1, Btn2, tk, w, mode, click_move, player, engine, book, coord, last_choice
    while len(coord.move_stack)>0:
            coord.pop()
    try:
        tk.destroy()
        engine.quit()
    except:
        pass

    last_choice = "off"
    engine_opt = None #widget for engine option
    ok = False  # if we can activate the function Draw
    time2think = 1.0  # time thinking or depth, it depends of the boolean time_is_depth
    last_move = ""  # explicit
    time_is_depth = True  #the variable "time2think" is depth, not time
    mode = "start"  # start: nothing, normal: human vs human, play: AI vs human, bot: AI/you vs another person, analysis: explicit
    click_move = ""  # the squares where you click
    player = "white"
    engine = None  # 'None' in the normal mode
    book = "Nothing"  # name of the polyglot opening book choosen
    
    tk = Tk()
    tk.title("Chess")
    tk.configure(cursor = "hand2")
    w = Canvas(tk,
               width=640,
               height=640,
               bg="#"+str(hex(238))[2:]+str(hex(216)[2:]+str(hex(181))[2:]))
    w.pack()
    for i in range(1, 9, 2):  # the squares of the board
        for j in range(1, 9, 2):
            w.create_rectangle(i*80,
                               (j-1)*80,
                               (i+1)*80,
                               j*80,
                               fill="#"+str(hex(181))[2:]+str(hex(136))[2:]+str(hex(99))[2:])
    
    for i in range(0, 9, 2):
        for j in range(0, 9, 2):
            w.create_rectangle(i*80,
                               (j-1)*80,
                               (i+1)*80,
                               j*80,
                               fill="#"+str(hex(181))[2:]+str(hex(136))[2:]+str(hex(99))[2:])
    w.create_rectangle(0, 0, 640, 640, fill="black", tag="pieces")
    w.create_text(320,
                  320,
                  text="Simple chess engine"+chr(9818)+chr(9819)+chr(9820)+chr(9821)+chr(9822)+chr(9823),
                  font="Times 20",
                  fill="red",
                  tag="pieces")
    MusicOption = StringVar()
    music_opt = Checkbutton(tk,
                            text="music option (tells the moves, and plays a song when it is the end of the game)",
                            variable=MusicOption,
                            onvalue="on",
                            offvalue="off")
    MusicOption.set("off")
    music_opt.pack()
    Btn1 = Button(tk, text="human vs human", overrelief="ridge", command=select1)
    Btn1.pack()
    Btn2 = Button(tk, text="against AI", overrelief="ridge", command=select2)
    Btn2.pack()
    w.bind_all("<Button-1>", click)
    tk.mainloop()


if __name__ == "__main__":
    main()

