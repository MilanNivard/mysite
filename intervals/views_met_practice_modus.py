from django.shortcuts import render
from .models import LvlInt
from django.db.models import Max

import random
import pygame
import time
import datetime

sub_level_cap = 10
module_name = 'Intervals'
level_cap = 6

counting_ans_retry = 0
practice_modus = 'exprt_expl'
question_count = 0
current_user = ''
counting_ans = 0
solution = ''
new_sub = ''
volume = 0.25
start = 'stop'
ans = 120

na_0 = 'button a0'
na_1 = 'button a1 na'
na_2 = 'button a2 na'
na_3 = 'button a3 na'
na_4 = 'button a4 na'
na_5 = 'button a5 na'
na_6 = 'button a6 na'
na_7 = 'button a7 na'
na_8 = 'button a8 na'
na_9 = 'button a9 na'
na_10 = 'button a10 na'
na_11 = 'button a11 na'
na_12 = 'button a12 na'


def set_volume(request):
    global volume
    if request.GET.get('new_volume') == '0':
        volume = 1
    elif request.GET.get('new_volume') == '1':
        volume = 0.5
    elif request.GET.get('new_volume') == '2':
        volume = 0.25
    elif request.GET.get('new_volume') == '3':
        volume = 0.1
    elif request.GET.get('new_volume') == '4':
        volume = 0.05


def calc_lvl_score(level):
    a = 0
    for i in range(0, sub_level_cap):
        a = a + int(LvlInt.objects.filter(lvl=level,
                                          sub_lvl=i,
                                          user=current_user).aggregate(Max('hi_score'))['hi_score__max'] or 0)
    return int(float("%.2f" % round(a / sub_level_cap, 2)))


def calc_hi_scores():
    lvl_1_hi_score = calc_lvl_score(1)
    lvl_2_hi_score = calc_lvl_score(2)
    lvl_3_hi_score = calc_lvl_score(3)
    lvl_4_hi_score = calc_lvl_score(4)
    lvl_5_hi_score = calc_lvl_score(5)
    lvl_6_hi_score = calc_lvl_score(6)
    tot_int_score_1 = (lvl_1_hi_score + lvl_2_hi_score + lvl_3_hi_score +
                       lvl_4_hi_score + lvl_5_hi_score + lvl_6_hi_score) / 6
    tot_int_score = int(float("%.2f" % round(tot_int_score_1, 2)))

    return [lvl_1_hi_score, lvl_2_hi_score, lvl_3_hi_score,
            lvl_4_hi_score, lvl_5_hi_score, lvl_6_hi_score, tot_int_score]


def select_level():
    select_lvl = int(LvlInt.objects.filter(user=current_user).aggregate(Max('lvl'))['lvl__max'] or 1)
    sub_level = int(LvlInt.objects.filter(lvl=select_lvl,
                                          user=current_user).aggregate(Max('max_sub_lvl'))['max_sub_lvl__max'] or 0)
    max_hi_score = int(LvlInt.objects.filter(lvl=select_lvl, user=current_user,
                                             sub_lvl=sub_level).aggregate(Max('hi_score'))['hi_score__max'] or 0)

    return select_lvl, sub_level, max_hi_score


def question(q_root_note, q_mode, q_level, q_sub_lvl, q_prob):
    global counting_ans
    global counting_ans_retry
    global question_count
    global current_user
    global solution
    global volume
    global ans

    sub_level = select_level()[1]

    if q_root_note == 'static':
        solution = random.choices(q_sub_lvl, q_prob, k=1)[0]
        root = notes[12]
        m_interval = notes[solution + 12]
    elif q_root_note == 'dynamic':
        dice = random.randint(1, 17)
        dice2 = dice + (random.choices(q_sub_lvl, q_prob, k=1))[0]
        solution = dice2 - dice
        root = notes[dice - 1]
        m_interval = notes[dice2 - 1]

    time.sleep(0.5)

    if q_mode == 'lo_hi':
        def play():
            pygame.mixer.Sound.play(root).set_volume(volume)
            time.sleep(1.2)
            pygame.mixer.Sound.play(m_interval).set_volume(volume)
    elif q_mode == 'hi_lo':
        def play():
            pygame.mixer.Sound.play(m_interval).set_volume(volume)
            time.sleep(1.2)
            pygame.mixer.Sound.play(root).set_volume(volume)
    else:
        def play():
            pygame.mixer.Sound.play(m_interval).set_volume(volume)
            pygame.mixer.Sound.play(root).set_volume(volume)

    play()

    for i in range(35):
        if int(ans or 110) == int(solution or 100):
            break
        time.sleep(0.1)

    print('ans2 =', ans)
    print('sol =', solution)

    b = LvlInt()
    b.user = current_user

    try:
        b.hi_score = LvlInt.objects.filter(lvl=q_level, user=current_user)[0].hi_score
    except:
        b.hi_score = 0

    b.lvl = q_level
    b.sub_lvl = sub_level
    b.time = datetime.datetime.now()
    b.question = solution
    b.answer = ans

    if int(ans or 110) == int(solution or 100):
        counting_ans += 10
        counting_ans_retry += 10
        b.result = 1
        b.hi_score = counting_ans
        b.save()
        ans = 120
    else:
        counting_ans = 120
        counting_ans_retry = 0
        b.hi_score = 0
        b.result = 0
        b.save()


def question_retry(request):
    global counting_ans_retry
    global question_count
    global practice_modus
    global new_sub
    global ans

    q_level = select_level()[0]

    if q_level < 4:
        q_root_note = 'static'
    else:
        q_root_note = 'dynamic'

    if q_level == 1 or q_level == 3:
        q_mode = 'lo_hi'
    elif q_level == 2 or q_level == 4:
        q_mode = 'hi_lo'
    else:
        q_mode = "harmony"

    new_prob = [1, 1]
    practice_modus = "prac_expl"

    question(q_root_note, q_mode, q_level, new_sub, new_prob)

    sub_lvl = ''
    sub_lvl_caps = ''
    prog_modus = 'practice level'

    sub_lvl_int_retry()

    return render(request, 'int/lvl_int.html', {
        "prog_modus": prog_modus,
        "max_hi_score": select_level()[2],
        "prog_count_int": question_count / 10,
        "prog_count": question_count,
        "sub_lvl": sub_lvl,
        "sub_level_cap": sub_lvl_caps,
        "practice_modus": practice_modus,
        "lvl": select_level()[0],
        "na_0": na_0,
        "na_1": na_1,
        "na_2": na_2,
        "na_3": na_3,
        "na_4": na_4,
        "na_5": na_5,
        "na_6": na_6,
        "na_7": na_7,
        "na_8": na_8,
        "na_9": na_9,
        "na_10": na_10,
        "na_11": na_11,
        "na_12": na_12
    })


def int_round(request, q_root_note, q_mode, q_level):
    global sub_level_cap
    global level_cap
    global ans
    global start
    global current_user

    current_user = request.user
    print('user =', current_user.id)

    ans = request.GET.get('answer')
    start = request.GET.get('play')

    sub_level = select_level()[1]
    set_volume(request)

    if start == 'go':
        global counting_ans
        global question_count
        global counting_ans_retry
        global new_sub

        counting_ans = 0

        while counting_ans < 100:
            question_count = counting_ans
            question(q_root_note, q_mode, q_level, sub_levels[sub_level], list_of_prob[sub_level])
        else:
            start = 'stop'
            if counting_ans == 120:
                counting_ans_retry = 0
                question_count = 0
                counting_ans = 0

                # if ans != 120:
                #    new_sub = [int(ans or 110),
                #               int(solution or 130)]
                #    while counting_ans_retry < 100:
                #        question_retry(request)
                #        counting_ans = counting_ans_retry
            else:
                question_count = 100
                b = LvlInt()
                b.user = current_user
                if sub_level < sub_level_cap:
                    b.max_sub_lvl = sub_level + 1
                    b.lvl = q_level
                    b.save()
                else:
                    if q_level < level_cap:
                        b.lvl = q_level + 1
                        b.save()
    sub_lvl_int(request)


def intervals(request):
    global question_count
    global practice_modus
    global module_name

    if select_level()[0] == 1:
        int_round(request, 'static', 'lo_hi', 1)
    elif select_level()[0] == 2:
        int_round(request, 'static', 'hi_lo', 2)
    elif select_level()[0] == 3:
        int_round(request, 'static', 'harmony', 3)
    elif select_level()[0] == 4:
        int_round(request, 'dynamic', 'lo_hi', 4)
    elif select_level()[0] == 5:
        int_round(request, 'dynamic', 'hi_lo', 5)
    elif select_level()[0] == 6:
        int_round(request, 'dynamic', 'harmony', 6)

    sub_lvl_int(request)
    practice_modus = "exprt_expl"
    if practice_modus == "prac_expl":
        lvl = 'Practice'
        sub_lvl = ''
        sub_lvl_caps = ''
        prog_modus = 'practice modus'
    else:
        lvl = 'Level ' + str(int(select_level()[0]))
        sub_lvl = str(int(select_level()[1]) + 1)
        sub_lvl_caps = '/' + str(sub_level_cap + 1)
        prog_modus = 'expert modus'

    return render(request, 'prac_int.html', {
        "module_name": module_name,
        "start_button": 'playbutton_play',
        "lvl": lvl,
        "prog_modus": prog_modus,
        "lvl_1_hi_score": calc_hi_scores()[0],
        "lvl_2_hi_score": calc_hi_scores()[1],
        "lvl_3_hi_score": calc_hi_scores()[2],
        "lvl_4_hi_score": calc_hi_scores()[3],
        "lvl_5_hi_score": calc_hi_scores()[4],
        "lvl_6_hi_score": calc_hi_scores()[5],
        "tot_int_score": calc_hi_scores()[6],
        "practice_modus": practice_modus,
        "max_hi_score": select_level()[2],
        "prog_count_int": question_count/10,
        "prog_count": question_count,
        "sub_lvl": sub_lvl,
        "sub_level_cap": sub_lvl_caps,
        "na_0": na_0,
        "na_1": na_1,
        "na_2": na_2,
        "na_3": na_3,
        "na_4": na_4,
        "na_5": na_5,
        "na_6": na_6,
        "na_7": na_7,
        "na_8": na_8,
        "na_9": na_9,
        "na_10": na_10,
        "na_11": na_11,
        "na_12": na_12
    })


def playbutton(request):
    global start
    if start == 'stop':
        start_button = 'playbutton_play'
    else:
        start_button = 'playbutton_pause'
    return render(request, 'includes/playbutton.html', {
        "start_button": start_button,
    })


def left_column(request):
    return render(request, 'includes/left_column.html', {
        "module_name": module_name,
        "lvl_1_hi_score": calc_hi_scores()[0],
        "lvl_2_hi_score": calc_hi_scores()[1],
        "lvl_3_hi_score": calc_hi_scores()[2],
        "lvl_4_hi_score": calc_hi_scores()[3],
        "lvl_5_hi_score": calc_hi_scores()[4],
        "lvl_6_hi_score": calc_hi_scores()[5],
        "tot_int_score": calc_hi_scores()[6]
    })


def prog_bar(request):
    global question_count
    global practice_modus
    global start

    start = request.GET.get('play')
    if start == 'go':
        question_count = 0
    else:
        try:
            question_count = (LvlInt.objects.filter(user=current_user).order_by('-id')[0]).hi_score
        except:
            question_count = 0

    if practice_modus == "prac_expl":
        lvl = 'Practice'
        sub_lvl = ''
        sub_lvl_caps = ''
        prog_modus = 'practice modus'
    else:
        lvl = 'Level ' + str(int(select_level()[0]))
        sub_lvl = str(int(select_level()[1]) + 1)
        sub_lvl_caps = '/' + str(sub_level_cap + 1)
        prog_modus = 'expert modus'

    return render(request, 'includes/prog_bar.html', {
        "lvl": lvl,
        "prog_modus": prog_modus,
        "sub_lvl": sub_lvl,
        "sub_level_cap": sub_lvl_caps,
        "practice_modus": practice_modus,
        "max_hi_score": select_level()[2],
        "prog_count_int": question_count/10,
        "prog_count": question_count
    })


def table_int(request):
    if practice_modus == "prac_expl":
        sub_lvl_int_retry()
    else:
        sub_lvl_int(request)

    return render(request, 'int/table_int.html', {
        "na_0": na_0,
        "na_1": na_1,
        "na_2": na_2,
        "na_3": na_3,
        "na_4": na_4,
        "na_5": na_5,
        "na_6": na_6,
        "na_7": na_7,
        "na_8": na_8,
        "na_9": na_9,
        "na_10": na_10,
        "na_11": na_11,
        "na_12": na_12
    })


def sub_lvl_int(request):
    global na_0
    global na_1
    global na_2
    global na_3
    global na_4
    global na_5
    global na_6
    global na_7
    global na_8
    global na_9
    global na_10
    global na_11
    global na_12

    na_0 = 'button a0'
    na_7 = 'button a7'
    na_12 = 'button a12'

    if select_level()[1] <= 0:
        na_4 = 'button a4 na'
    else:
        na_4 = 'button a4'
    if select_level()[1] <= 1:
        na_10 = 'button a10 na'
    else:
        na_10 = 'button a10'
    if select_level()[1] <= 2:
        na_1 = 'button a1 na'
    else:
        na_1 = 'button a1'
    if select_level()[1] <= 3:
        na_11 = 'button a11 na'
    else:
        na_11 = 'button a11'
    if select_level()[1] <= 4:
        na_5 = 'button a5 na'
    else:
        na_5 = 'button a5'
    if select_level()[1] <= 5:
        na_3 = 'button a3 na'
    else:
        na_3 = 'button a3'
    if select_level()[1] <= 6:
        na_8 = 'button a8 na'
    else:
        na_8 = 'button a8'
    if select_level()[1] <= 7:
        na_2 = 'button a2 na'
    else:
        na_2 = 'button a2'
    if select_level()[1] <= 8:
        na_6 = 'button a6 na'
    else:
        na_6 = 'button a6'
    if select_level()[1] <= 9:
        na_9 = 'button a9 na'
    else:
        na_9 = 'button a9'


def sub_lvl_int_retry():
    global na_0
    global na_1
    global na_2
    global na_3
    global na_4
    global na_5
    global na_6
    global na_7
    global na_8
    global na_9
    global na_10
    global na_11
    global na_12
    global new_sub

    na_0 = 'button a0 na'

    if new_sub[0] == 1 or new_sub[1] == 1:
        na_1 = 'button a1'
    else:
        na_1 = 'button a1 na'

    if new_sub[0] == 2 or new_sub[1] == 2:
        na_2 = 'button a2'
    else:
        na_2 = 'button a2 na'

    if new_sub[0] == 3 or new_sub[1] == 3:
        na_3 = 'button a3'
    else:
        na_3 = 'button a3 na'

    if new_sub[0] == 4 or new_sub[1] == 4:
        na_4 = 'button a4'
    else:
        na_4 = 'button a4 na'

    if new_sub[0] == 5 or new_sub[1] == 5:
        na_5 = 'button a5'
    else:
        na_5 = 'button a5 na'

    if new_sub[0] == 6 or new_sub[1] == 6:
        na_6 = 'button a6'
    else:
        na_6 = 'button a6 na'

    if new_sub[0] == 7 or new_sub[1] == 7:
        na_7 = 'button a7'
    else:
        na_7 = 'button a7 na'

    if new_sub[0] == 8 or new_sub[1] == 8:
        na_8 = 'button a8'
    else:
        na_8 = 'button a8 na'

    if new_sub[0] == 9 or new_sub[1] == 9:
        na_9 = 'button a9'
    else:
        na_9 = 'button a9 na'

    if new_sub[0] == 10 or new_sub[1] == 10:
        na_10 = 'button a10'
    else:
        na_10 = 'button a10 na'

    if new_sub[0] == 11 or new_sub[1] == 11:
        na_11 = 'button a11'
    else:
        na_11 = 'button a11 na'

    if new_sub[0] == 12 or new_sub[1] == 12:
        na_12 = 'button a12'
    else:
        na_12 = 'button a12 na'


def all_lvls(request):
    global question_count
    global practice_modus

    if practice_modus == "prac_expl":
        lvl = 'Practice'
        sub_lvl = ''
        sub_lvl_caps = ''
        prog_modus = 'practice modus'
    else:
        lvl = 'Level ' + str(int(select_level()[0]))
        sub_lvl = str(int(select_level()[1]) + 1)
        sub_lvl_caps = '/' + str(sub_level_cap + 1)
        prog_modus = 'expert modus'

    return render(request, 'int/lvl_int.html', {
        "lvl": lvl,
        "prog_modus": prog_modus,
        "max_hi_score": select_level()[2],
        "prog_count_int": question_count / 10,
        "prog_count": question_count,
        "sub_lvl": sub_lvl,
        "sub_level_cap": sub_lvl_caps,
        "practice_modus": practice_modus,
        "na_0": na_0,
        "na_1": na_1,
        "na_2": na_2,
        "na_3": na_3,
        "na_4": na_4,
        "na_5": na_5,
        "na_6": na_6,
        "na_7": na_7,
        "na_8": na_8,
        "na_9": na_9,
        "na_10": na_10,
        "na_11": na_11,
        "na_12": na_12
    })


pygame.mixer.init()

C2 = pygame.mixer.Sound("mp3\C2.ogg")
Cis2 = pygame.mixer.Sound("mp3\C#2.ogg")
D2 = pygame.mixer.Sound("mp3\D2.ogg")
Dis2 = pygame.mixer.Sound("mp3\D#2.ogg")
E2 = pygame.mixer.Sound("mp3\E2.ogg")
F2 = pygame.mixer.Sound("mp3\F2.ogg")
Fis2 = pygame.mixer.Sound("mp3\F#2.ogg")
G2 = pygame.mixer.Sound("mp3\G2.ogg")
Gis2 = pygame.mixer.Sound("mp3\G#2.ogg")
A2 = pygame.mixer.Sound("mp3\A2.ogg")
Ais2 = pygame.mixer.Sound("mp3\A#2.ogg")
B2 = pygame.mixer.Sound("mp3\B2.ogg")
C3 = pygame.mixer.Sound("mp3\C3.ogg")
Cis3 = pygame.mixer.Sound("mp3\C#3.ogg")
D3 = pygame.mixer.Sound("mp3\D3.ogg")
Dis3 = pygame.mixer.Sound("mp3\D#3.ogg")
E3 = pygame.mixer.Sound("mp3\E3.ogg")
F3 = pygame.mixer.Sound("mp3\F3.ogg")
Fis3 = pygame.mixer.Sound("mp3\F#3.ogg")
G3 = pygame.mixer.Sound("mp3\G3.ogg")
Gis3 = pygame.mixer.Sound("mp3\G#3.ogg")
A3 = pygame.mixer.Sound("mp3\A3.ogg")
Ais3 = pygame.mixer.Sound("mp3\A#3.ogg")
B3 = pygame.mixer.Sound("mp3\B3.ogg")
C4 = pygame.mixer.Sound("mp3\C4.ogg")
Cis4 = pygame.mixer.Sound("mp3\C#4.ogg")
D4 = pygame.mixer.Sound("mp3\D4.ogg")
Dis4 = pygame.mixer.Sound("mp3\D#4.ogg")
E4 = pygame.mixer.Sound("mp3\E4.ogg")

notes = [C2, Cis2, D2, Dis2, E2, F2, Fis2, G2, Gis2, A2, Ais2, B2,
         C3, Cis3, D3, Dis3, E3, F3, Fis3, G3, Gis3, A3, Ais3, B3,
         C4, Cis4, D4, Dis4, E4]

int_sub_1 = [7, 12]
int_sub_2 = int_sub_1 + [4]
int_sub_3 = int_sub_2 + [10]
int_sub_4 = int_sub_3 + [1]
int_sub_5 = int_sub_4 + [11]
int_sub_6 = int_sub_5 + [5]
int_sub_7 = int_sub_6 + [3]
int_sub_8 = int_sub_7 + [8]
int_sub_9 = int_sub_8 + [2]
int_sub_10 = int_sub_9 + [6]
int_sub_11 = int_sub_10 + [9]

sub_levels = [
    int_sub_1,
    int_sub_2,
    int_sub_3,
    int_sub_4,
    int_sub_5,
    int_sub_6,
    int_sub_7,
    int_sub_8,
    int_sub_9,
    int_sub_10,
    int_sub_11
]

list_of_prob = [
    [1, 1],
    [1, 1, 1.5],
    [1, 1, 1, 2],
    [1, 1, 1, 1, 2.5],
    [1, 1, 1, 1, 1, 3],
    [1, 1, 1, 1, 1, 1, 3.5],
    [1, 1, 1, 1, 1, 1, 1, 4],
    [1, 1, 1, 1, 1, 1, 1, 1, 4.5],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 5],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5.5],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6]]
