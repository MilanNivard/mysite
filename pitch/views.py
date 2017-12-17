from django.shortcuts import render
from .models import LvlPit
from django.db.models import Max

import simpleaudio as sa
import random
import time
import datetime

sub_level_cap = 4
module_name = 'Pitch'
level_cap = 1

counting_ans_retry = 0
practice_modus = 'exprt_expl'
question_count = 0
current_user = ''
counting_ans = 0
solution = ''
volume = 0.25
start = 'stop'
ans = 120

p_1 = 'button_chords higher'
p_2 = 'button_chords lower'


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
        a = a + int(LvlPit.objects.filter(lvl=level,
                                          sub_lvl=i,
                                          user=current_user).aggregate(Max('hi_score'))['hi_score__max'] or 0)
    return int(float("%.2f" % round(a / (sub_level_cap + 1), 2)))


def select_level():
    select_lvl = int(LvlPit.objects.filter(user=current_user).aggregate(Max('lvl'))['lvl__max'] or 1)
    sub_level = int(LvlPit.objects.filter(lvl=select_lvl,
                                          user=current_user).aggregate(Max('max_sub_lvl'))['max_sub_lvl__max'] or 0)
    max_hi_score = int(LvlPit.objects.filter(lvl=select_lvl, user=current_user,
                                             sub_lvl=sub_level).aggregate(Max('hi_score'))['hi_score__max'] or 0)
    return select_lvl, sub_level, max_hi_score


def question(q_level, q_sub_lvl):
    global counting_ans
    global question_count
    global current_user
    global solution
    global volume
    global ans

    sub_level = select_level()[1]
    print('sub =', sub_level)

    if q_sub_lvl == 0:
        a_1 = random.randint(5, 7)
    elif q_sub_lvl == 1:
        a_1 = random.randint(4, 8)
    elif q_sub_lvl == 2:
        a_1 = random.randint(3, 9)
    elif q_sub_lvl == 3:
        a_1 = random.randint(2, 10)
    elif q_sub_lvl == 4:
        a_1 = random.randint(1, 11)

    a_2 = random.randint(0, 1)

    n_1 = notes[a_1]

    if a_2 == 0:
        if q_sub_lvl == 0:
            n_2 = notes[a_1 - 5]
        elif q_sub_lvl == 1:
            n_2 = notes[a_1 - 4]
        elif q_sub_lvl == 2:
            n_2 = notes[a_1 - 3]
        elif q_sub_lvl == 3:
            n_2 = notes[a_1 - 2]
        elif q_sub_lvl == 4:
            n_2 = notes[a_1 - 1]

        solution = 'lower'
    elif a_2 == 1:
        if q_sub_lvl == 0:
            n_2 = notes[a_1 + 5]
        elif q_sub_lvl == 1:
            n_2 = notes[a_1 + 4]
        elif q_sub_lvl == 2:
            n_2 = notes[a_1 + 3]
        elif q_sub_lvl == 3:
            n_2 = notes[a_1 + 2]
        elif q_sub_lvl == 4:
            n_2 = notes[a_1 + 1]

        solution = 'higher'

    time.sleep(0.5)

    def play():
        n_1.play()
        time.sleep(1.2)
        n_2.play()

    play()

    time.sleep(2.0)

    print('ans2 =', ans)
    print('sol =', solution)

    b = LvlPit()
    b.user = current_user

    try:
        b.hi_score = LvlPit.objects.filter(lvl=q_level, user=current_user)[0].hi_score
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


def int_round(request, q_level):
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
            question(q_level, sub_level)
        else:
            start = 'stop'
            if counting_ans == 120:
                question_count = 0
                counting_ans = 0
            else:
                question_count = 100
                b = LvlPit()
                b.user = current_user
                if sub_level < sub_level_cap:
                    b.max_sub_lvl = sub_level + 1
                    b.lvl = q_level
                    b.save()


def pitch(request):
    global question_count
    global practice_modus
    global module_name

    int_round(request, 1)

    return render(request, 'prac_pit.html', {
        "module_name": module_name,
        "start_button": 'playbutton_play',
        "lvl": 'Level ' + str(int(select_level()[0])),
        "sub_lvl": str(int(select_level()[1]) + 1),
        "sub_level_cap": '/' + str(sub_level_cap + 1),
        "tot_int_score": calc_lvl_score(1),
        "practice_modus": practice_modus,
        "max_hi_score": select_level()[2],
        "prog_count_int": question_count/10,
        "prog_count": question_count,
        "p_1": p_1,
        "p_2": p_2
    })


def left_column(request):
    return render(request, 'pit/left_column_pit.html', {
        "module_name": module_name,
        "tot_int_score": calc_lvl_score(1)
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
            question_count = (LvlPit.objects.filter(user=current_user).order_by('-id')[0]).hi_score
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


def all_lvls(request):
    global question_count
    global practice_modus
    return render(request, 'pit/lvl_pit.html', {
        "lvl": 'Level ' + str(int(select_level()[0])),
        "sub_lvl": str(int(select_level()[1]) + 1),
        "sub_level_cap": '/' + str(sub_level_cap + 1),
        "max_hi_score": select_level()[2],
        "prog_count_int": question_count / 10,
        "prog_count": question_count,
        "practice_modus": practice_modus,
        "p_1": p_1,
        "p_2": p_2
    })


C3_m30 = sa.WaveObject.from_wave_file("mp3\C3_m30.wav")
C3_m25 = sa.WaveObject.from_wave_file("mp3\C3_m25.wav")
C3_m20 = sa.WaveObject.from_wave_file("mp3\C3_m20.wav")
C3_m15 = sa.WaveObject.from_wave_file("mp3\C3_m15.wav")
C3_m10 = sa.WaveObject.from_wave_file("mp3\C3_m10.wav")
C3_m5 = sa.WaveObject.from_wave_file("mp3\C3_m5.wav")
C3 = sa.WaveObject.from_wave_file("mp3\C3.wav")
C3_p5 = sa.WaveObject.from_wave_file("mp3\C3_p5.wav")
C3_p10 = sa.WaveObject.from_wave_file("mp3\C3_p10.wav")
C3_p15 = sa.WaveObject.from_wave_file("mp3\C3_p15.wav")
C3_p20 = sa.WaveObject.from_wave_file("mp3\C3_p20.wav")
C3_p25 = sa.WaveObject.from_wave_file("mp3\C3_p25.wav")
C3_p30 = sa.WaveObject.from_wave_file("mp3\C3_p30.wav")

notes = [C3_m30, C3_m25, C3_m20, C3_m15, C3_m10, C3_m5, C3, C3_p5, C3_p10, C3_p15, C3_p20, C3_p25, C3_p30]
