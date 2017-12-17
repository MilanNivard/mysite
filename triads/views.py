from django.shortcuts import render
from .models import LvlTri
from django.db.models import Max

import simpleaudio as sa
import random
import time
import datetime

sub_level_cap = 4
module_name = 'Triads'
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

t1 = 'button_chords t1'
t2 = 'button_chords t2'
t3 = 'button_chords t3'
t4 = 'button_chords t4'
t5 = 'button_chords t5'
t10 = 'button_chords t10'


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
        a = a + int(LvlTri.objects.filter(lvl=level,
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
    select_lvl = int(LvlTri.objects.filter(user=current_user).aggregate(Max('lvl'))['lvl__max'] or 1)
    sub_level = int(LvlTri.objects.filter(lvl=select_lvl,
                                          user=current_user).aggregate(Max('max_sub_lvl'))['max_sub_lvl__max'] or 0)
    max_hi_score = int(LvlTri.objects.filter(lvl=select_lvl, user=current_user,
                                             sub_lvl=sub_level).aggregate(Max('hi_score'))['hi_score__max'] or 0)
    return select_lvl, sub_level, max_hi_score


def question(q_root_note, q_mode, q_level, q_sub_lvl, q_prob):
    global counting_ans
    global question_count
    global current_user
    global solution
    global volume
    global dice
    global ans

    sub_level = select_level()[1]
    solution = random.choices(q_sub_lvl, q_prob, k=1)[0]

    if q_root_note == 'static':
        dice = 12
    elif q_root_note == 'dynamic':
        dice = random.randint(1, 17)

    if solution == 'major':
        root = notes[dice]
        interval_1 = notes[dice + 4]
        interval_2 = notes[dice + 7]
    elif solution == 'minor':
        root = notes[dice]
        interval_1 = notes[dice + 3]
        interval_2 = notes[dice + 7]
    elif solution == 'dim':
        root = notes[dice]
        interval_1 = notes[dice + 3]
        interval_2 = notes[dice + 6]
    elif solution == 'aug':
        root = notes[dice]
        interval_1 = notes[dice + 4]
        interval_2 = notes[dice + 8]
    elif solution == 'sus2':
        root = notes[dice]
        interval_1 = notes[dice + 2]
        interval_2 = notes[dice + 7]
    elif solution == 'sus4':
        root = notes[dice]
        interval_1 = notes[dice + 5]
        interval_2 = notes[dice + 7]

    time.sleep(0.5)

    if q_mode == 'lo_hi':
        def play():
            (root).play()
            time.sleep(0.7)
            (interval_1).play()
            time.sleep(0.7)
            (interval_2).play()

    elif q_mode == 'hi_lo':
        def play():
            (interval_2).play()
            time.sleep(0.7)
            (interval_1).play()
            time.sleep(0.7)
            (root).play()
    else:
        def play():
            (root).play()
            (interval_1).play()
            (interval_2).play()

    play()

    for i in range(35):
        if ans == solution:
            break
        time.sleep(0.1)

    print('ans2 =', ans)
    print('sol =', solution)

    b = LvlTri()
    b.user = current_user

    try:
        b.hi_score = LvlTri.objects.filter(lvl=q_level, user=current_user)[0].hi_score
    except IndexError:
        b.hi_score = 0

    b.lvl = q_level
    b.sub_lvl = sub_level
    b.time = datetime.datetime.now()
    b.question = solution
    b.answer = ans

    if ans == solution:
        counting_ans += 10
        b.result = 1
        b.hi_score = counting_ans
        b.save()
        ans = 120
    else:
        counting_ans = 120
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
                b = LvlTri()
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


def triads(request):
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

    return render(request, 'prac_tri.html', {
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
        "t1": t1,
        "t2": t2,
        "t3": t3,
        "t4": t4,
        "t5": t5,
        "t10": t10
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
            question_count = (LvlTri.objects.filter(user=current_user).order_by('-id')[0]).hi_score
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


def table_tri(request):
    sub_lvl_int()
    return render(request, 'tri/table_tri.html', {
        "t1": t1,
        "t2": t2,
        "t3": t3,
        "t4": t4,
        "t5": t5,
        "t10": t10
    })


def sub_lvl_int():
    global t1
    global t2
    global t3
    global t4
    global t5
    global t10

    t1 = 'button_chords t1'
    t2 = 'button_chords t2'

    if select_level()[1] <= 0:
        t3 = 'button_chords t3 na'
    else:
        t3 = 'button_chords t3'
    if select_level()[1] <= 1:
        t4 = 'button_chords t4 na'
    else:
        t4 = 'button_chords t4'
    if select_level()[1] <= 2:
        t5 = 'button_chords t5 na'
    else:
        t5 = 'button_chords t5'
    if select_level()[1] <= 3:
        t10 = 'button_chords t10 na'
    else:
        t10 = 'button_chords t10'


def all_lvls(request):
    global question_count
    global practice_modus
    return render(request, 'tri/lvl_tri.html', {
        "lvl": 'Level ' + str(int(select_level()[0])),
        "sub_lvl": str(int(select_level()[1]) + 1),
        "sub_level_cap": '/' + str(sub_level_cap + 1),
        "max_hi_score": select_level()[2],
        "prog_count_int": question_count / 10,
        "prog_count": question_count,
        "practice_modus": practice_modus,
        "t1": t1,
        "t2": t2,
        "t3": t3,
        "t4": t4,
        "t5": t5,
        "t10": t10
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

int_sub_1 = ['major', 'minor']
int_sub_2 = ['major', 'minor', 'dim']
int_sub_3 = ['major', 'minor', 'dim', 'aug']
int_sub_4 = ['major', 'minor', 'dim', 'aug', 'sus2']
int_sub_5 = ['major', 'minor', 'dim', 'aug', 'sus2', 'sus4']


sub_levels = [
    int_sub_1,
    int_sub_2,
    int_sub_3,
    int_sub_4,
    int_sub_5
    ]

list_of_prob = [
    [1, 1],
    [1, 1, 1.5],
    [1, 1, 1, 2],
    [1, 1, 1, 1, 2.5],
    [1, 1, 1, 1, 1, 3]]







