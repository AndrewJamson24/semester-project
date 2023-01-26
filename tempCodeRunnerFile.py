def bot():
    """bot is coming..."""
    global website
    if website=="detect automatically(slower)":
        websites=[]
        if "images" in os.listdir():
            websites += os.listdir("images")
        im = pyautogui.screenshot()
        for site in websites:
            with open("images/"+site+"/pixel.txt", "r") as f:
                f.readline()
                pixel2=eval(f.readline())
                f.close()
            try:
                for y in range(im.size[1]):
                    for x in range(im.size[0]):
                        rgb = im.getpixel((x, y))
                        if rgb in pixel2:
                            website=site
                            print(website)
                            raise TypeError
            except:
                break
    try:
        t=time.time()
        coord_board1=find_first_pixel(website)
        print(coord_board1)
        coord_board2 = find_last_pixel(website)
        print(coord_board2)
        print(time.time()-t)
        t=time.time()
        
    except:  # if not found with image recognition, use the mouse to detect the corners
        nsec = 4
        sec = nsec
        Draw(player2)
        while sec>0:
            w.create_text(320, 320, text=str(sec)+"s for the mouse to be in the\ntop left-hand\ncorner of the board", fill="red", font="Times 20", tag="recognition")
            tk.update()
            sleep(1)
            sec-=1
            w.itemconfigure("recognition", state="hidden")
        coord_board1 = get_mouse_board()
        sec = nsec
        while sec>0:
            w.create_text(320, 320, text=str(sec)+"s for the mouse to be in the\nlower right-hand\ncorner of the board", fill="red", font="Times 20", tag="recognition")
            tk.update()
            sleep(1)
            sec-=1
            w.itemconfigure("recognition", state="hidden")
        coord_board2 = get_mouse_board()
    coord_board = coord_board1+coord_board2
    if player2 == "white":
        if engine == "chess-engine":
            play_white(coord, lvl, book)
        else:
            play_engine(coord, engine, book, time2think, time_is_depth)
        Draw(player)
        if write:
            write_move(str(coord.move_stack[-1]))
        else:
            play_mouse(str(coord.move_stack[-1]), coord_board, player2=="black")
    while True:
        if coord.is_checkmate():
            break
        if (coord.turn and player == "white") or (not coord.turn and player == "black"):  # player's turn
            move0 = get_move(coord_board1, coord_board2, player2, website)
            move1 = move0[0]+move0[1]  # e2e4 ?
            move2 = move0[1]+move0[0]  # or e4e2 ?
            l = list(map(str, coord.legal_moves))
            if (move1 in l) or (move1+"q" in l):
                move = move1
            elif (move2 in l) or (move2+"q" in l):
                move = move2
            elif "e1a1" in [move1, move2] and "e1c1" in l:
                move="e1c1"
            elif "e8a8" in [move1, move2] and "e8c8" in l:
                move="e8c8"
            elif "e1h1" in [move1, move2] and "e1g1" in l:
                move="e1g1"
            elif "e8h8" in [move1, move2] and "e8g8" in l:
                move="e8g8"
            else:
                move = "nothing"
            if move == "nothing":
                pass#-(sleep(time2think-0.1)
            else:
                play_human(move)
                play_human(move+"q")
                Draw(player2)
        else:  # bot's turn
            if engine == "chess-engine":
                if player2 == "white":
                    play_white(coord, lvl, book)
                else:
                    play_black(coord, lvl, book)
            else:
                play_engine(coord, engine, book, time2think, time_is_depth)
            if write:
                write_move(str(coord.move_stack[-1]))
                Draw(player2)
            else:
                play_mouse(str(coord.move_stack[-1]), coord_board, player2=="black")
                Draw(player2)
