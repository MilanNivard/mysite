from django.shortcuts import render
from .models import LvlExt
from django.db.models import Max

import simpleaudio as sa
import random
import time
import datetime

sub_level_cap = 11
module_name = 'Extended Chords'
level_cap = 6

counting_ans_retry = 0
practice_modus = 'exprt_expl'
question_count = 0
current_user = ''
counting_ans = 0
solution = ''
volume = 0.25
start = 'stop'
dice = 12
ans = 120

t15 = 'button_chords t15'
t16 = 'button_chords t16'
t17 = 'button_chords t17'
t18 = 'button_chords t18'
t19 = 'button_chords t19'
t20 = 'button_chords t20'
t21 = 'button_chords t21'
t22 = 'button_chords t22'
t23 = 'button_chords t23'
t24 = 'button_chords t24'
t25 = 'button_chords t25'
t26 = 'button_chords t26'
t27 = 'button_chords t27'
t28 = 'button_chords t28'
t29 = 'button_chords t29'


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
    for i in range(0, sub_level_cap + 1):
        a = a + int(LvlExt.objects.filter(lvl=level,
                                          sub_lvl=i,
                                          user=current_user).aggregate(Max('hi_score'))['hi_score__max'] or 0)
    return int(float("%.2f" % round(a / (sub_level_cap + 1), 2)))


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
    select_lvl = int(LvlExt.objects.filter(user=current_user).aggregate(Max('lvl'))['lvl__max'] or 1)
    sub_level = int(LvlExt.objects.filter(lvl=select_lvl,
                                          user=current_user).aggregate(Max('max_sub_lvl'))['max_sub_lvl__max'] or 0)
    max_hi_score = int(LvlExt.objects.filter(lvl=select_lvl, user=current_user,
                                             sub_lvl=sub_level).aggregate(Max('hi_score'))['hi_score__max'] or 0)
    return select_lvl, sub_level, max_hi_score


def question(q_root_note, q_mode, q_level, q_sub_lvl, q_prob):
    global counting_ans
    global counting_ans_retry
    global question_count
    global solution
    global volume
    global ans
    global dice

    sub_level = select_level()[1]
    solution = random.choices(q_sub_lvl, q_prob, k=1)[0]

    if q_root_note == 'static':
        dice = 12
    elif q_root_note == 'dynamic':
        dice = random.randint(1, 14)

    if solution == 'major 7th':
        root = notes[dice]
        interval_1 = notes[dice + 4]
        interval_2 = notes[dice + 7]
        interval_3 = notes[dice + 11]
        interval_4 = notes[dice]
    elif solution == 'dominant':
        root = notes[dice]
        interval_1 = notes[dice + 4]
        interval_2 = notes[dice + 7]
        interval_3 = notes[dice + 10]
        interval_4 = notes[dice]
    elif solution == 'minor 7th':
        root = notes[dice]
        interval_1 = notes[dice + 3]
        interval_2 = notes[dice + 7]
        interval_3 = notes[dice + 10]
        interval_4 = notes[dice]
    elif solution == 'b9':
        root = notes[dice]
        interval_1 = notes[dice + 4]
        interval_2 = notes[dice + 10]
        interval_3 = notes[dice + 13]
        interval_4 = notes[dice]
    elif solution == 'maj 9':
        root = notes[dice]
        interval_1 = notes[dice + 4]
        interval_2 = notes[dice + 11]
        interval_3 = notes[dice + 14]
        interval_4 = notes[dice]
    elif solution == '9':
        root = notes[dice]
        interval_1 = notes[dice + 4]
        interval_2 = notes[dice + 10]
        interval_3 = notes[dice + 14]
        interval_4 = notes[dice]
    elif solution == 'min 9':
        root = notes[dice]
        interval_1 = notes[dice + 3]
        interval_2 = notes[dice + 10]
        interval_3 = notes[dice + 14]
        interval_4 = notes[dice]
    elif solution == '#9':
        root = notes[dice]
        interval_1 = notes[dice + 4]
        interval_2 = notes[dice + 10]
        interval_3 = notes[dice + 15]
        interval_4 = notes[dice]
    elif solution == 'maj #11':
        root = notes[dice]
        interval_1 = notes[dice + 4]
        interval_2 = notes[dice + 6]
        interval_3 = notes[dice + 11]
        interval_4 = notes[dice]
    elif solution == '#11':
        root = notes[dice]
        interval_1 = notes[dice + 4]
        interval_2 = notes[dice + 6]
        interval_3 = notes[dice + 10]
        interval_4 = notes[dice]
    elif solution == 'min 11':
        root = notes[dice]
        interval_1 = notes[dice + 3]
        interval_2 = notes[dice + 5]
        interval_3 = notes[dice + 10]
        interval_4 = notes[dice]
    elif solution == 'b9b13':
        root = notes[dice]
        interval_1 = notes[dice + 4]
        interval_2 = notes[dice + 8]
        interval_3 = notes[dice + 10]
        interval_4 = notes[dice + 13]
    elif solution == 'maj9b13':
        root = notes[dice]
        interval_1 = notes[dice + 4]
        interval_2 = notes[dice + 8]
        interval_3 = notes[dice + 11]
        interval_4 = notes[dice + 14]
    elif solution == 'b13':
        root = notes[dice]
        interval_1 = notes[dice + 4]
        interval_2 = notes[dice + 8]
        interval_3 = notes[dice + 10]
        interval_4 = notes[dice]
    elif solution == 'min 13':
        root = notes[dice]
        interval_1 = notes[dice + 3]
        interval_2 = notes[dice + 8]
        interval_3 = notes[dice + 10]
        interval_4 = notes[dice]

    time.sleep(1.0)

    if q_mode == 'lo_hi':
        (root).play()
        time.sleep(0.7)
        (interval_1).play()
        time.sleep(0.7)
        (interval_2).play()
        time.sleep(0.7)
        (interval_3).play()
        time.sleep(0.7)
        (interval_4).play()
    elif q_mode == 'hi_lo':
        (interval_4).play()
        time.sleep(0.7)
        (interval_3).play()
        time.sleep(0.7)
        (interval_2).play()
        time.sleep(0.7)
        (interval_1).play()
        time.sleep(0.7)
        (root).play()
    else:
        (root).play()
        (interval_1).play()
        (interval_2).play()
        (interval_3).play()
        (interval_4).play()

    for i in range(35):
        if ans == solution:
            break
        time.sleep(0.1)

    print('ans2 =', ans)

    b = LvlExt()
    b.user = current_user

    try:
        b.hi_score = LvlExt.objects.filter(lvl=q_level, user=current_user)[0].hi_score
    except IndexError:
        b.hi_score = 0

    b.lvl = q_level
    b.sub_lvl = sub_level
    b.time = datetime.datetime.now()
    b.question = solution
    b.answer = ans

    if ans == solution:
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


def int_round(request, q_root_note, q_mode, q_level):
    global sub_level_cap
    global current_user
    global level_cap
    global ans
    global start

    current_user = request.user
    print('user =', current_user.id)

    ans = request.GET.get('answer')
    start = request.GET.get('play')

    sub_level = select_level()[1]
    set_volume(request)

    if start == 'go':
        global counting_ans
        global question_count

        counting_ans = 0

        while counting_ans < 100:
            question_count = counting_ans
            question(q_root_note, q_mode, q_level, sub_levels[sub_level], list_of_prob[sub_level])
        else:
            start = 'stop'
            if counting_ans == 120:
                question_count = 0
                counting_ans = 0
            else:
                question_count = 100
                b = LvlExt()
                b.user = current_user
                if sub_level < sub_level_cap:
                    b.max_sub_lvl = sub_level + 1
                    b.lvl = q_level
                    b.save()
                else:
                    if q_level < level_cap:
                        b.lvl = q_level + 1
                        b.save()
    sub_lvl_int()


def extended_chords(request):
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

    sub_lvl_int()

    return render(request, 'prac_ext.html', {
        "module_name": module_name,
        "start_button": 'playbutton_play',
        "lvl": 'Level ' + str(int(select_level()[0])),
        "sub_lvl": str(int(select_level()[1]) + 1),
        "sub_level_cap": '/' + str(sub_level_cap + 1),
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
        "t15": t15,
        "t16": t16,
        "t17": t17,
        "t18": t18,
        "t19": t19,
        "t20": t20,
        "t21": t21,
        "t22": t22,
        "t23": t23,
        "t24": t24,
        "t25": t25,
        "t26": t26,
        "t27": t27,
        "t28": t28,
        "t29": t29
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
            question_count = (LvlExt.objects.filter(user=current_user).order_by('-id')[0]).hi_score
        except IndexError:
            question_count = 0

    return render(request, 'includes/prog_bar.html', {
        "lvl": 'Level ' + str(int(select_level()[0])),
        "sub_lvl": str(int(select_level()[1]) + 1),
        "sub_level_cap": '/' + str(sub_level_cap + 1),
        "max_hi_score": select_level()[2],
        "practice_modus": practice_modus,
        "prog_count_int": question_count/10,
        "prog_count": question_count
    })


def table_ext(request):
    sub_lvl_int()
    return render(request, 'ext/table_ext.html', {
        "t15": t15,
        "t16": t16,
        "t17": t17,
        "t18": t18,
        "t19": t19,
        "t20": t20,
        "t21": t21,
        "t22": t22,
        "t23": t23,
        "t24": t24,
        "t25": t25,
        "t26": t26,
        "t27": t27,
        "t28": t28,
        "t29": t29
    })


def sub_lvl_int():
    global t15
    global t16
    global t17
    global t18
    global t19
    global t20
    global t21
    global t22
    global t23
    global t24
    global t25
    global t26
    global t27
    global t28
    global t29

    t15 = 'button_chords t15'
    t16 = 'button_chords t16'
    t17 = 'button_chords t17'
    t18 = 'button_chords t18'

    if select_level()[1] <= 0:
        t19 = 'button_chords t19 na'
    else:
        t19 = 'button_chords t19'
    if select_level()[1] <= 1:
        t20 = 'button_chords t20 na'
    else:
        t20 = 'button_chords t20'
    if select_level()[1] <= 2:
        t21 = 'button_chords t21 na'
    else:
        t21 = 'button_chords t21'
    if select_level()[1] <= 3:
        t22 = 'button_chords t22 na'
    else:
        t22 = 'button_chords t22'
    if select_level()[1] <= 4:
        t23 = 'button_chords t23 na'
    else:
        t23 = 'button_chords t23'
    if select_level()[1] <= 5:
        t24 = 'button_chords t24 na'
    else:
        t24 = 'button_chords t24'
    if select_level()[1] <= 6:
        t25 = 'button_chords t25 na'
    else:
        t25 = 'button_chords t25'
    if select_level()[1] <= 7:
        t26 = 'button_chords t26 na'
    else:
        t26 = 'button_chords t26'
    if select_level()[1] <= 8:
        t27 = 'button_chords t27 na'
    else:
        t27 = 'button_chords t27'
    if select_level()[1] <= 9:
        t28 = 'button_chords t28 na'
    else:
        t28 = 'button_chords t28'
    if select_level()[1] <= 10:
        t29 = 'button_chords t29 na'
    else:
        t29 = 'button_chords t29'


def all_lvls(request):
    global question_count
    global practice_modus
    return render(request, 'ext/lvl_ext.html', {
        "lvl": 'Level ' + str(int(select_level()[0])),
        "sub_lvl": str(int(select_level()[1]) + 1),
        "sub_level_cap": '/' + str(sub_level_cap + 1),
        "max_hi_score": select_level()[2],
        "prog_count_int": question_count / 10,
        "prog_count": question_count,
        "practice_modus": practice_modus,
        "t15": t15,
        "t16": t16,
        "t17": t17,
        "t18": t18,
        "t19": t19,
        "t20": t20,
        "t21": t21,
        "t22": t22,
        "t23": t23,
        "t24": t24,
        "t25": t25,
        "t26": t26,
        "t27": t27,
        "t28": t28,
        "t29": t29
    })


C2 = sa.WaveObject.from_wave_file("mp3\C2.wav")
Cis2 = sa.WaveObject.from_wave_file("mp3\C#2.wav")
D2 = sa.WaveObject.from_wave_file("mp3\D2.wav")
Dis2 = sa.WaveObject.from_wave_file("mp3\D#2.wav")
E2 = sa.WaveObject.from_wave_file("mp3\E2.wav")
F2 = sa.WaveObject.from_wave_file("mp3\F2.wav")
Fis2 = sa.WaveObject.from_wave_file("mp3\F#2.wav")
G2 = sa.WaveObject.from_wave_file("mp3\G2.wav")
Gis2 = sa.WaveObject.from_wave_file("mp3\G#2.wav")
A2 = sa.WaveObject.from_wave_file("mp3\A2.wav")
Ais2 = sa.WaveObject.from_wave_file("mp3\A#2.wav")
B2 = sa.WaveObject.from_wave_file("mp3\B2.wav")
C3 = sa.WaveObject.from_wave_file("mp3\C3.wav")
Cis3 = sa.WaveObject.from_wave_file("mp3\C#3.wav")
D3 = sa.WaveObject.from_wave_file("mp3\D3.wav")
Dis3 = sa.WaveObject.from_wave_file("mp3\D#3.wav")
E3 = sa.WaveObject.from_wave_file("mp3\E3.wav")
F3 = sa.WaveObject.from_wave_file("mp3\F3.wav")
Fis3 = sa.WaveObject.from_wave_file("mp3\F#3.wav")
G3 = sa.WaveObject.from_wave_file("mp3\G3.wav")
Gis3 = sa.WaveObject.from_wave_file("mp3\G#3.wav")
A3 = sa.WaveObject.from_wave_file("mp3\A3.wav")
Ais3 = sa.WaveObject.from_wave_file("mp3\A#3.wav")
B3 = sa.WaveObject.from_wave_file("mp3\B3.wav")
C4 = sa.WaveObject.from_wave_file("mp3\C4.wav")
Cis4 = sa.WaveObject.from_wave_file("mp3\C#4.wav")
D4 = sa.WaveObject.from_wave_file("mp3\D4.wav")
Dis4 = sa.WaveObject.from_wave_file("mp3\D#4.wav")
E4 = sa.WaveObject.from_wave_file("mp3\E4.wav")

notes = [C2, Cis2, D2, Dis2, E2, F2, Fis2, G2, Gis2, A2, Ais2, B2,
         C3, Cis3, D3, Dis3, E3, F3, Fis3, G3, Gis3, A3, Ais3, B3,
         C4, Cis4, D4, Dis4, E4]

int_sub_1 = ['major 7th', 'dominant', 'minor 7th', 'b9']
int_sub_2 = int_sub_1 + ['maj 9']
int_sub_3 = int_sub_2 + ['9']
int_sub_4 = int_sub_3 + ['min 9']
int_sub_5 = int_sub_4 + ['#9']
int_sub_6 = int_sub_5 + ['maj #11']
int_sub_7 = int_sub_6 + ['#11']
int_sub_8 = int_sub_7 + ['min 11']
int_sub_9 = int_sub_8 + ['b9b13']
int_sub_10 = int_sub_9 + ['maj9b13']
int_sub_11 = int_sub_10 + ['b13']
int_sub_12 = int_sub_11 + ['min 13']

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
    int_sub_11,
    int_sub_12]

list_of_prob = [
    [1, 1, 1, 3],
    [1, 1, 1, 1, 4],
    [1, 1, 1, 1, 1, 5],
    [1, 1, 1, 1, 1, 1, 6],
    [1, 1, 1, 1, 1, 1, 1, 7],
    [1, 1, 1, 1, 1, 1, 1, 1, 8],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 9],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 10],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 11],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 12],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 13],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 14]]
