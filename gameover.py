import curses, time, os, itertools, json

def main():
    text = {}
    with open('json/gameover.json') as ifile:
        text = json.load(ifile).get("GAMEOVER")
        ifile.close()

    s = curses.initscr()
    curses.curs_set(0)
    sh, sw = s.getmaxyx()
    w = curses.newwin(sh, sw, 0, 0)
    w.timeout(25)

    try:
        for pixel in text:
            w.getch()
            w.addch(pixel[0], pixel[1], curses.ACS_BLOCK)

        time.sleep(1)
        os.execl('sh/restart.sh', '')
    except:
        os.execl('sh/reset.sh', '')

if __name__ == "__main__":
    main()
