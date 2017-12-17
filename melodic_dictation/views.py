from django.shortcuts import render
from .models import LvlMel
from django.db.models import Max

import simpleaudio as sa
import random
import time
import datetime

sub_level_cap = 12
module_name = 'Melodic Dictation'
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

ans_class = 'pro_ans semi_hide'

ans_1 = ''
ans_2 = ''
ans_3 = ''
ans_4 = ''
ans_5 = ''
sol_1 = ''
sol_2 = ''
sol_3 = ''
sol_4 = ''
sol_5 = ''


def visibility(sub_level):
    if sub_level % 2 == 0:
        visibility_major = 'show'
        visibility_minor = 'hide'
    else:
        visibility_major = 'hide'
        visibility_minor = 'show'
    return visibility_major, visibility_minor


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
        a = a + int(LvlMel.objects.filter(lvl=level,
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
    select_lvl = int(LvlMel.objects.filter(user=current_user).aggregate(Max('lvl'))['lvl__max'] or 1)
    sub_level = int(LvlMel.objects.filter(lvl=select_lvl,
                                          user=current_user).aggregate(Max('max_sub_lvl'))['max_sub_lvl__max'] or 0)
    max_hi_score = int(LvlMel.objects.filter(lvl=select_lvl, user=current_user,
                                             sub_lvl=sub_level).aggregate(Max('hi_score'))['hi_score__max'] or 0)
    return select_lvl, sub_level, max_hi_score


def question(q_root_note, q_mode, q_level, q_sub_lvl):
    global counting_ans
    global counting_ans_retry
    global question_count
    global solution
    global volume
    global dice
    global ans
    global ans_1
    global ans_2
    global ans_3
    global ans_4
    global ans_5
    global sol_1
    global sol_2
    global sol_3
    global sol_4
    global sol_5
    global ans_class

    sub_level = select_level()[1]

    ans_class = 'pro_ans semi_hide'
    ans_1 = ''
    ans_2 = ''
    ans_3 = ''
    ans_4 = ''
    ans_5 = ''

    if q_root_note == 'static':
        dice = 12
    elif q_root_note == 'dynamic':
        dice = random.randint(1, 17)

    time.sleep(0.5)

    def chords(sol):
        if sol == '1':
            root = notes[dice]
        elif sol == 'b2':
            root = notes[dice + 1]
        elif sol == '2':
            root = notes[dice + 2]
        elif sol == 'b3':
            root = notes[dice + 3]
        elif sol == '3':
            root = notes[dice + 4]
        elif sol == '4':
            root = notes[dice + 5]
        elif sol == 'b5':
            root = notes[dice + 6]
        elif sol == '5':
            root = notes[dice + 7]
        elif sol == 'b6':
            root = notes[dice + 8]
        elif sol == '6':
            root = notes[dice + 9]
        elif sol == 'b7':
            root = notes[dice + 10]
        elif sol == '7':
            root = notes[dice + 11]
        elif sol == '8':
            root = notes[dice + 12]

        root.play()

    def unique_sol(sol_prev):
        solu = random.choices(q_sub_lvl, k=1)[0]
        while solu == sol_prev:
            solu = random.choices(q_sub_lvl, k=1)[0]
        return solu

    sol_1 = '1'
    sol_2 = unique_sol(sol_1)
    sol_3 = unique_sol(sol_2)
    sol_4 = unique_sol(sol_3)
    sol_5 = unique_sol(sol_4)

    chords(sol_1)
    time.sleep(0.5)
    chords(sol_2)
    time.sleep(0.5)
    chords(sol_3)
    time.sleep(0.5)
    chords(sol_4)
    time.sleep(0.5)
    chords(sol_5)
    time.sleep(0.5)

    solution = [sol_1, sol_2, sol_3, sol_4, sol_5]
    answer = []

    ans_class = 'pro_ans'

    for i in range(70):
        if ans is not None and ans != 120:
            try:
                ans_1 = (answer[0])
            except IndexError:
                pass
            try:
                ans_2 = (answer[1])
            except IndexError:
                pass
            try:
                ans_3 = (answer[2])
            except IndexError:
                pass
            try:
                ans_4 = (answer[3])
            except IndexError:
                pass
            try:
                ans_5 = (answer[4])
            except IndexError:
                pass

            try:
                if ans != answer[-1]:
                    answer.append(ans)
            except IndexError:
                answer.append(ans)
        time.sleep(0.1)

    b = LvlMel()
    b.user = current_user

    try:
        b.hi_score = LvlMel.objects.filter(lvl=q_level, user=current_user)[0].hi_score
    except IndexError:
        b.hi_score = 0

    b.lvl = q_level
    b.sub_lvl = sub_level
    b.time = datetime.datetime.now()
    b.question = solution
    b.answer = answer

    print('ans2 =', answer)
    print('sol =', solution)

    if answer == solution:
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
            question(q_root_note, q_mode, q_level, sub_levels[sub_level])
        else:
            start = 'stop'
            if counting_ans == 120:
                question_count = 0
                counting_ans = 0
            else:
                question_count = 100
                b = LvlMel()
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


def melodic_dictation(request):
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

    visibility_major = visibility(select_level()[1])[0]
    visibility_minor = visibility(select_level()[1])[1]

    return render(request, 'prac_mel.html', {
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
        "visibility_major": visibility_major,
        "visibility_minor": visibility_minor,
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
        "na_12": na_12,
        "ans_1": ans_1,
        "ans_2": ans_2,
        "ans_3": ans_3,
        "ans_4": ans_4,
        "ans_5": ans_5,
        "ans_class_1": mel_ans_class()[0],
        "ans_class_2": mel_ans_class()[1],
        "ans_class_3": mel_ans_class()[2],
        "ans_class_4": mel_ans_class()[3],
        "ans_class_5": mel_ans_class()[4]
    })


def left_column_mel(request):
    return render(request, 'mel/left_column_mel.html', {
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
            question_count = (LvlMel.objects.filter(user=current_user).order_by('-id')[0]).hi_score
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


def table_mel(request):
    sub_lvl_int()
    return render(request, 'mel/table_mel.html', {
        "visibility_major": visibility(select_level()[1])[0],
        "visibility_minor": visibility(select_level()[1])[1],
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
        "na_12": na_12,
        "ans_1": ans_1,
        "ans_2": ans_2,
        "ans_3": ans_3,
        "ans_4": ans_4,
        "ans_5": ans_5,
        "ans_class_1": mel_ans_class()[0],
        "ans_class_2": mel_ans_class()[1],
        "ans_class_3": mel_ans_class()[2],
        "ans_class_4": mel_ans_class()[3],
        "ans_class_5": mel_ans_class()[4]
    })


def mel_ans_class():
    if ans_class == 'pro_ans semi_hide':
        ans_class_1 = 'pro_ans semi_hide'
    elif ans_1 == sol_1:
        ans_class_1 = 'ans_cor'
    elif ans_1 == '':
        ans_class_1 = 'pro_ans'
    else:
        ans_class_1 = 'ans_wro'

    if ans_class == 'pro_ans semi_hide':
        ans_class_2 = 'pro_ans semi_hide'
    elif ans_2 == sol_2:
        ans_class_2 = 'ans_cor'
    elif ans_2 == '':
        ans_class_2 = 'pro_ans'
    else:
        ans_class_2 = 'ans_wro'

    if ans_class == 'pro_ans semi_hide':
        ans_class_3 = 'pro_ans semi_hide'
    elif ans_3 == sol_3:
        ans_class_3 = 'ans_cor'
    elif ans_3 == '':
        ans_class_3 = 'pro_ans'
    else:
        ans_class_3 = 'ans_wro'

    if ans_class == 'pro_ans semi_hide':
        ans_class_4 = 'pro_ans semi_hide'
    elif ans_4 == sol_4:
        ans_class_4 = 'ans_cor'
    elif ans_4 == '':
        ans_class_4 = 'pro_ans'
    else:
        ans_class_4 = 'ans_wro'

    if ans_class == 'pro_ans semi_hide':
        ans_class_5 = 'pro_ans semi_hide'
    elif ans_5 == sol_5:
        ans_class_5 = 'ans_cor'
    elif ans_5 == '':
        ans_class_5 = 'pro_ans'
    else:
        ans_class_5 = 'ans_wro'
    return ans_class_1, ans_class_2, ans_class_3, ans_class_4, ans_class_5


def table_mel_ans(request):
    return render(request, 'mel/table_mel_ans.html', {
        "ans_1": ans_1,
        "ans_2": ans_2,
        "ans_3": ans_3,
        "ans_4": ans_4,
        "ans_5": ans_5,
        "ans_class_1": mel_ans_class()[0],
        "ans_class_2": mel_ans_class()[1],
        "ans_class_3": mel_ans_class()[2],
        "ans_class_4": mel_ans_class()[3],
        "ans_class_5": mel_ans_class()[4]
    })


def sub_lvl_int():
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
    na_12 = 'button a12'

    if select_level()[1] == 0:
        na_1 = 'button a1 na'
        na_2 = 'button a2 na'
        na_3 = 'button a3 na'
        na_4 = 'button a4'
        na_5 = 'button a5 na'
        na_6 = 'button a6 na'
        na_7 = 'button a7'
        na_8 = 'button a8 na'
        na_9 = 'button a9 na'
        na_10 = 'button a10 na'
        na_11 = 'button a11 na'
    elif select_level()[1] == 1:
        na_1 = 'button a1 na'
        na_2 = 'button a2'
        na_3 = 'button a3 na'
        na_4 = 'button a4'
        na_5 = 'button a5 na'
        na_6 = 'button a6 na'
        na_7 = 'button a7'
        na_8 = 'button a8 na'
        na_9 = 'button a9'
        na_10 = 'button a10 na'
        na_11 = 'button a11 na'
    elif select_level()[1] == 2:
        na_1 = 'button a1 na'
        na_2 = 'button a2 na'
        na_3 = 'button a3'
        na_4 = 'button a4 na'
        na_5 = 'button a5'
        na_6 = 'button a6 na'
        na_7 = 'button a7'
        na_8 = 'button a8 na'
        na_9 = 'button a9 na'
        na_10 = 'button a10'
        na_11 = 'button a11 na'
    elif select_level()[1] == 3:
        na_1 = 'button a1 na'
        na_2 = 'button a2'
        na_3 = 'button a3 na'
        na_4 = 'button a4'
        na_5 = 'button a5'
        na_6 = 'button a6 na'
        na_7 = 'button a7'
        na_8 = 'button a8 na'
        na_9 = 'button a9'
        na_10 = 'button a10 na'
        na_11 = 'button a11'
    elif select_level()[1] == 4:
        na_1 = 'button a1 na'
        na_2 = 'button a2'
        na_3 = 'button a3'
        na_4 = 'button a4 na'
        na_5 = 'button a5'
        na_6 = 'button a6 na'
        na_7 = 'button a7'
        na_8 = 'button a8'
        na_9 = 'button a9 na'
        na_10 = 'button a10'
        na_11 = 'button a11 na'
    elif select_level()[1] == 5:
        na_1 = 'button a1 na'
        na_2 = 'button a2'
        na_3 = 'button a3 na'
        na_4 = 'button a4'
        na_5 = 'button a5 na'
        na_6 = 'button a6'
        na_7 = 'button a7'
        na_8 = 'button a8 na'
        na_9 = 'button a9'
        na_10 = 'button a10 na'
        na_11 = 'button a11'
    elif select_level()[1] == 6:
        na_1 = 'button a1 na'
        na_2 = 'button a2'
        na_3 = 'button a3 na'
        na_4 = 'button a4'
        na_5 = 'button a5'
        na_6 = 'button a6 na'
        na_7 = 'button a7'
        na_8 = 'button a8 na'
        na_9 = 'button a9'
        na_10 = 'button a10'
        na_11 = 'button a11 na'
    elif select_level()[1] == 7:
        na_1 = 'button a1 na'
        na_2 = 'button a2'
        na_3 = 'button a3'
        na_4 = 'button a4 na'
        na_5 = 'button a5'
        na_6 = 'button a6 na'
        na_7 = 'button a7'
        na_8 = 'button a8 na'
        na_9 = 'button a9'
        na_10 = 'button a10'
        na_11 = 'button a11 na'
    elif select_level()[1] == 8:
        na_1 = 'button a1'
        na_2 = 'button a2 na'
        na_3 = 'button a3'
        na_4 = 'button a4 na'
        na_5 = 'button a5'
        na_6 = 'button a6 na'
        na_7 = 'button a7'
        na_8 = 'button a8'
        na_9 = 'button a9 na'
        na_10 = 'button a10'
        na_11 = 'button a11 na'
    elif select_level()[1] == 9:
        na_1 = 'button a1'
        na_2 = 'button a2 na'
        na_3 = 'button a3 na'
        na_4 = 'button a4'
        na_5 = 'button a5'
        na_6 = 'button a6'
        na_7 = 'button a7 na'
        na_8 = 'button a8'
        na_9 = 'button a9 na'
        na_10 = 'button a10'
        na_11 = 'button a11 na'
    elif select_level()[1] == 10:
        na_1 = 'button a1 na'
        na_2 = 'button a2 na'
        na_3 = 'button a3'
        na_4 = 'button a4 na'
        na_5 = 'button a5'
        na_6 = 'button a6'
        na_7 = 'button a7'
        na_8 = 'button a8 na'
        na_9 = 'button a9 na'
        na_10 = 'button a10'
        na_11 = 'button a11 na'
    elif select_level()[1] == 11:
        na_1 = 'button a1 na'
        na_2 = 'button a2'
        na_3 = 'button a3'
        na_4 = 'button a4 na'
        na_5 = 'button a5'
        na_6 = 'button a6 na'
        na_7 = 'button a7'
        na_8 = 'button a8'
        na_9 = 'button a9 na'
        na_10 = 'button a10 na'
        na_11 = 'button a11'
    elif select_level()[1] == 12:
        na_1 = 'button a1 na'
        na_2 = 'button a2'
        na_3 = 'button a3'
        na_4 = 'button a4 na'
        na_5 = 'button a5'
        na_6 = 'button a6 na'
        na_7 = 'button a7'
        na_8 = 'button a8 na'
        na_9 = 'button a9'
        na_10 = 'button a10 na'
        na_11 = 'button a11'


def all_lvls(request):
    global question_count
    global practice_modus
    return render(request, 'mel/lvl_mel.html', {
        "lvl": 'Level ' + str(int(select_level()[0])),
        "sub_lvl": str(int(select_level()[1]) + 1),
        "sub_level_cap": '/' + str(sub_level_cap + 1),
        "max_hi_score": select_level()[2],
        "prog_count_int": question_count / 10,
        "prog_count": question_count,
        "practice_modus": practice_modus,
        "visibility_major": visibility(select_level()[1])[0],
        "visibility_minor": visibility(select_level()[1])[1],
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
        "na_12": na_12,
        "ans_1": ans_1,
        "ans_2": ans_2,
        "ans_3": ans_3,
        "ans_4": ans_4,
        "ans_5": ans_5,
        "ans_class_1": mel_ans_class()[0],
        "ans_class_2": mel_ans_class()[1],
        "ans_class_3": mel_ans_class()[2],
        "ans_class_4": mel_ans_class()[3],
        "ans_class_5": mel_ans_class()[4]
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

int_sub_1 = ['1', '3', '5', '8']
int_sub_2 = ['1', '2', '3', '5', '6', '8']
int_sub_3 = ['1', 'b3', '4', '5', 'b7', '8']
int_sub_4 = ['1', '2', '3', '4', '5', '6', '7', '8']
int_sub_5 = ['1', '2', 'b3', '4', '5', 'b6', 'b7', '8']
int_sub_6 = ['1', '2', '3', 'b5', '5', '6', '7', '8']
int_sub_7 = ['1', '2', '3', '4', '5', '6', 'b7', '8']
int_sub_8 = ['1', '2', 'b3', '4', '5', '6', 'b7', '8']
int_sub_9 = ['1', 'b2', 'b3', '4', '5', 'b6', 'b7', '8']
int_sub_10 = ['1', 'b2', '3', '4', 'b5', 'b6', 'b7', '8']
int_sub_11 = ['1', 'b3', '4', 'b5', '5', 'b7', '8']
int_sub_12 = ['1', '2', 'b3', '4', '5', 'b6', '7', '8']
int_sub_13 = ['1', '2', 'b3', '4', '5', '6', '7', '8']

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
    int_sub_12,
    int_sub_13
]
