import curses, time, os, argparse, json
from pygame import mixer

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', help = 'User', required = True)
    args = parser.parse_args()

    data = {}
    with open('json/data.json') as ifile:
        data = json.load(ifile)
        ifile.close()

    if(args.user != "restart"):
        data['current_player'] = args.user

        with open('json/data.json', 'w') as ofile:
            json.dump(data, ofile)
            ofile.close()

    text = {}
    with open('json/snake.json') as ifile:
        text = json.load(ifile).get("SNAKE")
        ifile.close()

    s = curses.initscr()
    curses.curs_set(0)
    sh, sw = s.getmaxyx()

    if sh != 32 or sw != 100:
        os.execl('sh/resize.sh', '')

    w = curses.newwin(sh, sw, 0, 0)
    w.timeout(25)

    w.addstr(3, 38, "Matthew Bowen Presents")
    w.addstr(26, 42, "Player: " + str(data.get("high_score_player", data.get("current_player"))))
    w.addstr(27, 42, "High Score: " + str(data.get('high_score', "00")))
    w.addstr(28, 42, "Time: " + str(data.get("high_score_time", "00:00:00")))
    w.getch()

    try:
        for pixel in text:
            w.getch()
            w.addch(pixel[0], pixel[1], curses.ACS_BLOCK)

        mixer.init()
        mixer.music.load("audio/sfx_menu_select3.wav")
        mixer.music.play()

        time.sleep(2)
        os.execl('sh/start.sh', '')
    except:
        os.execl('sh/reset.sh', '')

if __name__ == "__main__":
    main()
