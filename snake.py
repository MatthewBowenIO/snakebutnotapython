import random, curses, subprocess, sys, time, datetime, os, json
from pygame import mixer

def main():
    speed = 100
    game_over = False
    mixer.init()

    data = {}
    with open('json/data.json') as ifile:
        data = json.load(ifile)
        ifile.close()

    s = curses.initscr()
    curses.curs_set(0)
    sh, sw = s.getmaxyx()
    w = curses.newwin(sh, sw, 0, 0)
    w.keypad(1)
    w.timeout(speed)

    snk_x = sw / 4
    snk_y = sh / 2
    snake = [
        [snk_y, snk_x], [snk_y, snk_x - 1], [snk_y, snk_x - 2]
    ]

    food = [sh / 2, sw / 2]
    w.addch(food[0], food[1], curses.ACS_PI)

    key = curses.KEY_RIGHT
    start = time.time()

    while game_over != True:
        try:
            next_key = w.getch()
            key = key if next_key == -1 else next_key

            if snake[0][0] in [0, sh] or snake[0][1] in [0, sw] or snake[0] in snake[1:]:
                if data.get('high_score', 0) < (len(snake) - 3):
                    data['high_score'] = len(snake) - 3
                    data['high_score_time'] = str(datetime.timedelta(seconds=int(time.time() - start)))
                    data['high_score_player'] = data.get("current_player")

                with open('json/data.json', 'w') as ofile:
                    json.dump(data, ofile)
                    ofile.close()

                game_over = True
                continue

            new_head = [snake[0][0], snake[0][1]]

            if key == curses.KEY_DOWN:
                new_head[0] += 1
                speed = 100
            if key == curses.KEY_UP:
                new_head[0] -= 1
                speed = 100
            if key == curses.KEY_LEFT:
                new_head[1] -= 1
                speed = 75
            if key == curses.KEY_RIGHT:
                new_head[1] += 1
                speed = 75

            w.timeout(speed)

            snake.insert(0, new_head)

            if snake[0] == food:
                mixer.music.load("audio/sfx_coin_double5.wav")
                mixer.music.play()
                food = None
                while food is None:
                    nf = [
                        random.randint(1, sh-1),
                        random.randint(1, sw-1)
                    ]
                    food = nf if nf not in snake else None
                w.addch(food[0], food[1], curses.ACS_PI)
            else:
                tail = snake.pop()
                w.addch(tail[0], tail[1], ' ')

            w.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)
            w.addstr(1, 1, str(len(snake) - 3))
            w.addstr(1, 90, str(datetime.timedelta(seconds=int(time.time() - start))))
        except:
            mixer.music.load("audio/sfx_sounds_error2.wav")
            mixer.music.play()
            time.sleep(1)
            os.execl('sh/gameover.sh', '')

    mixer.music.load("audio/sfx_sounds_error2.wav")
    mixer.music.play()
    time.sleep(1)
    os.execl('sh/gameover.sh', '')

if __name__ == "__main__":
    main()
