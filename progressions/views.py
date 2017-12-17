from django.shortcuts import render
from .models import LvlPro
from django.db.models import Max

import simpleaudio as sa
import random
import time
import datetime

sub_level_cap = 13
module_name = 'Chord Progressions'
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

p1 = 'button_prog p1'
p2 = 'button_prog p2'
p3 = 'button_prog p3'
p4 = 'button_prog p4'
p5 = 'button_prog p5'
p6 = 'button_prog p6'
p7 = 'button_prog p7'
p8 = 'button_prog p8'
p9 = 'button_prog p9'

p11 = 'button_prog p11'
p12 = 'button_prog p12'
p13 = 'button_prog p13'
p14 = 'button_prog p14'
p15 = 'button_prog p15'
p16 = 'button_prog p16'
p17 = 'button_prog p17'
p18 = 'button_prog p18'
p19 = 'button_prog p19'

p21 = 'button_prog p21'
p22 = 'button_prog p22'
p23 = 'button_prog p23'
p24 = 'button_prog p24'
p25 = 'button_prog p25'
p26 = 'button_prog p26'
p27 = 'button_prog p27'
p28 = 'button_prog p28'
p29 = 'button_prog p29'

p31 = 'button_prog p31'
p32 = 'button_prog p32'
p33 = 'button_prog p33'
p34 = 'button_prog p34'
p35 = 'button_prog p35'
p36 = 'button_prog p36'
p37 = 'button_prog p37'
p38 = 'button_prog p38'
p39 = 'button_prog p39'

p41 = 'button_prog p41'
p42 = 'button_prog p42'
p43 = 'button_prog p43'
p44 = 'button_prog p44'
p45 = 'button_prog p45'
p46 = 'button_prog p46'
p47 = 'button_prog p47'
p48 = 'button_prog p48'
p49 = 'button_prog p49'

p51 = 'button_prog p51'
p52 = 'button_prog p52'
p53 = 'button_prog p53'
p54 = 'button_prog p54'
p55 = 'button_prog p55'
p56 = 'button_prog p56'
p57 = 'button_prog p57'
p58 = 'button_prog p58'
p59 = 'button_prog p59'
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
        a = a + int(LvlPro.objects.filter(lvl=level,
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
    select_lvl = int(LvlPro.objects.filter(user=current_user).aggregate(Max('lvl'))['lvl__max'] or 1)
    sub_level = int(LvlPro.objects.filter(lvl=select_lvl,
                                          user=current_user).aggregate(Max('max_sub_lvl'))['max_sub_lvl__max'] or 0)
    max_hi_score = int(LvlPro.objects.filter(lvl=select_lvl, user=current_user,
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
        if sol == 'I':
            root = notes[dice]
            interval_1 = notes[dice + 4]
            interval_2 = notes[dice + 7]
        elif sol == 'I 1st':
            root = notes[dice + 4]
            interval_1 = notes[dice + 7]
            interval_2 = notes[dice + 12]
        elif sol == 'I 2nd':
            root = notes[dice + 7]
            interval_1 = notes[dice + 12]
            interval_2 = notes[dice + 16]

        elif sol == 'ii':
            root = notes[dice + 2]
            interval_1 = notes[dice + 5]
            interval_2 = notes[dice + 9]
        elif sol == 'ii 1st':
            root = notes[dice + 5]
            interval_1 = notes[dice + 9]
            interval_2 = notes[dice + 14]
        elif sol == 'ii 2nd':
            root = notes[dice - 3]
            interval_1 = notes[dice + 2]
            interval_2 = notes[dice + 5]

        elif sol == 'bIII':
            root = notes[dice + 3]
            interval_1 = notes[dice + 7]
            interval_2 = notes[dice + 10]
        elif sol == 'bIII 1st':
            root = notes[dice + 7]
            interval_1 = notes[dice + 10]
            interval_2 = notes[dice + 16]
        elif sol == 'bIII 2nd':
            root = notes[dice - 2]
            interval_1 = notes[dice + 3]
            interval_2 = notes[dice + 7]

        elif sol == 'iii':
            root = notes[dice + 4]
            interval_1 = notes[dice + 7]
            interval_2 = notes[dice + 11]
        elif sol == 'iii 1st':
            root = notes[dice + 7]
            interval_1 = notes[dice + 11]
            interval_2 = notes[dice + 16]
        elif sol == 'iii 2nd':
            root = notes[dice - 1]
            interval_1 = notes[dice + 4]
            interval_2 = notes[dice + 7]

        elif sol == 'IV':
            root = notes[dice + 5]
            interval_1 = notes[dice + 9]
            interval_2 = notes[dice + 12]
        elif sol == 'IV 1st':
            root = notes[dice - 3]
            interval_1 = notes[dice + 0]
            interval_2 = notes[dice + 5]
        elif sol == 'IV 2nd':
            root = notes[dice + 0]
            interval_1 = notes[dice + 5]
            interval_2 = notes[dice + 9]

        elif sol == 'V':
            root = notes[dice + 7]
            interval_1 = notes[dice + 11]
            interval_2 = notes[dice + 14]
        elif sol == 'V 1st':
            root = notes[dice - 1]
            interval_1 = notes[dice + 2]
            interval_2 = notes[dice + 7]
        elif sol == 'V 2nd':
            root = notes[dice + 2]
            interval_1 = notes[dice + 7]
            interval_2 = notes[dice + 11]

        elif sol == 'bVI':
            root = notes[dice - 4]
            interval_1 = notes[dice + 0]
            interval_2 = notes[dice + 3]
        elif sol == 'bVI 1st':
            root = notes[dice - 0]
            interval_1 = notes[dice + 3]
            interval_2 = notes[dice + 8]
        elif sol == 'bVI 2nd':
            root = notes[dice + 3]
            interval_1 = notes[dice + 8]
            interval_2 = notes[dice + 12]

        elif sol == 'vi':
            root = notes[dice - 3]
            interval_1 = notes[dice + 0]
            interval_2 = notes[dice + 4]
        elif sol == 'vi 1st':
            root = notes[dice - 0]
            interval_1 = notes[dice + 4]
            interval_2 = notes[dice + 9]
        elif sol == 'vi 2nd':
            root = notes[dice + 4]
            interval_1 = notes[dice + 9]
            interval_2 = notes[dice + 12]

        elif sol == 'bVII':
            root = notes[dice - 2]
            interval_1 = notes[dice + 2]
            interval_2 = notes[dice + 5]
        elif sol == 'bVII 1st':
            root = notes[dice + 2]
            interval_1 = notes[dice + 5]
            interval_2 = notes[dice + 10]
        elif sol == 'bVII 2nd':
            root = notes[dice + 2]
            interval_1 = notes[dice + 10]
            interval_2 = notes[dice + 14]

        elif sol == 'i':
            root = notes[dice + 0]
            interval_1 = notes[dice + 3]
            interval_2 = notes[dice + 7]
        elif sol == 'i 1st':
            root = notes[dice + 3]
            interval_1 = notes[dice + 7]
            interval_2 = notes[dice + 12]
        elif sol == 'i 2nd':
            root = notes[dice + 7]
            interval_1 = notes[dice + 12]
            interval_2 = notes[dice + 15]

        elif sol == 'bII':
            root = notes[dice + 1]
            interval_1 = notes[dice + 5]
            interval_2 = notes[dice + 8]
        elif sol == 'bII 1st':
            root = notes[dice + 5]
            interval_1 = notes[dice + 8]
            interval_2 = notes[dice + 13]
        elif sol == 'bII 2nd':
            root = notes[dice - 4]
            interval_1 = notes[dice + 1]
            interval_2 = notes[dice + 5]

        elif sol == 'III':
            root = notes[dice + 3]
            interval_1 = notes[dice + 7]
            interval_2 = notes[dice + 10]
        elif sol == 'III 1st':
            root = notes[dice - 5]
            interval_1 = notes[dice - 2]
            interval_2 = notes[dice + 2]
        elif sol == 'III 2nd':
            root = notes[dice - 2]
            interval_1 = notes[dice + 2]
            interval_2 = notes[dice + 7]

        elif sol == 'iv':
            root = notes[dice + 5]
            interval_1 = notes[dice + 8]
            interval_2 = notes[dice + 12]
        elif sol == 'iv 1st':
            root = notes[dice - 4]
            interval_1 = notes[dice + 0]
            interval_2 = notes[dice + 5]
        elif sol == 'iv 2nd':
            root = notes[dice + 0]
            interval_1 = notes[dice + 5]
            interval_2 = notes[dice + 12]

        elif sol == 'IV':
            root = notes[dice + 5]
            interval_1 = notes[dice + 9]
            interval_2 = notes[dice + 12]
        elif sol == 'IV 1st':
            root = notes[dice - 3]
            interval_1 = notes[dice + 0]
            interval_2 = notes[dice + 5]
        elif sol == 'IV 2nd':
            root = notes[dice + 0]
            interval_1 = notes[dice + 5]
            interval_2 = notes[dice + 9]

        elif sol == 'v':
            root = notes[dice + 7]
            interval_1 = notes[dice + 10]
            interval_2 = notes[dice + 14]
        elif sol == 'v 1st':
            root = notes[dice - 2]
            interval_1 = notes[dice + 2]
            interval_2 = notes[dice + 7]
        elif sol == 'v 2nd':
            root = notes[dice + 2]
            interval_1 = notes[dice + 7]
            interval_2 = notes[dice + 10]

        elif sol == 'V':
            root = notes[dice + 7]
            interval_1 = notes[dice + 11]
            interval_2 = notes[dice + 14]
        elif sol == 'V 1st':
            root = notes[dice - 1]
            interval_1 = notes[dice + 2]
            interval_2 = notes[dice + 7]
        elif sol == 'V 2nd':
            root = notes[dice + 2]
            interval_1 = notes[dice + 7]
            interval_2 = notes[dice + 11]

        elif sol == 'VI':
            root = notes[dice - 4]
            interval_1 = notes[dice + 0]
            interval_2 = notes[dice + 3]
        elif sol == 'VI 1st':
            root = notes[dice - 0]
            interval_1 = notes[dice + 3]
            interval_2 = notes[dice + 8]
        elif sol == 'VI 2nd':
            root = notes[dice + 3]
            interval_1 = notes[dice + 8]
            interval_2 = notes[dice + 12]

        elif sol == 'VII':
            root = notes[dice - 2]
            interval_1 = notes[dice + 2]
            interval_2 = notes[dice + 5]
        elif sol == 'VII 1st':
            root = notes[dice + 2]
            interval_1 = notes[dice + 5]
            interval_2 = notes[dice + 10]
        elif sol == 'VII 2nd':
            root = notes[dice + 5]
            interval_1 = notes[dice + 10]
            interval_2 = notes[dice + 14]

        def play():
            root.play()
            interval_1.play()
            interval_2.play()

        play()

    def unique_sol(sol_prev):
        solu = random.choices(q_sub_lvl, k=1)[0]
        while solu == sol_prev:
            solu = random.choices(q_sub_lvl, k=1)[0]
        return solu

    if sub_level % 2 == 0:
        sol_1 = 'I'
    else:
        sol_1 = 'i'

    sol_2 = unique_sol(sol_1)
    sol_3 = unique_sol(sol_2)
    sol_4 = unique_sol(sol_3)
    sol_5 = unique_sol(sol_4)

    chords(sol_1)
    time.sleep(1.5)
    chords(sol_2)
    time.sleep(1.5)
    chords(sol_3)
    time.sleep(1.5)
    chords(sol_4)
    time.sleep(1.5)
    chords(sol_5)
    time.sleep(1.1)

    solution = [sol_1, sol_2, sol_3, sol_4, sol_5]
    answer = []

    ans_class = 'pro_ans'

    for i in range(80):
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

    b = LvlPro()
    b.user = current_user
    try:
        b.hi_score = LvlPro.objects.filter(lvl=q_level, user=current_user)[0].hi_score
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
                b = LvlPro()
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


def progressions(request):
    global question_count
    global practice_modus
    global module_name
    global p11
    global p12
    global p13
    global p14
    global p15
    global p16
    global p17
    global p18
    global p19
    global p21
    global p22
    global p23
    global p24
    global p25
    global p26
    global p27
    global p28
    global p29
    global p41
    global p42
    global p43
    global p44
    global p45
    global p46
    global p47
    global p48
    global p49
    global p51
    global p52
    global p53
    global p54
    global p55
    global p56
    global p57
    global p58
    global p59

    if select_level()[0] < 2:
        p21 = 'hide'
        p22 = 'hide'
        p23 = 'hide'
        p24 = 'hide'
        p25 = 'hide'
        p26 = 'hide'
        p27 = 'hide'
        p28 = 'hide'
        p29 = 'hide'
        p51 = 'hide'
        p52 = 'hide'
        p53 = 'hide'
        p54 = 'hide'
        p55 = 'hide'
        p56 = 'hide'
        p57 = 'hide'
        p58 = 'hide'
        p59 = 'hide'
        p11 = 'hide'
        p12 = 'hide'
        p13 = 'hide'
        p14 = 'hide'
        p15 = 'hide'
        p16 = 'hide'
        p17 = 'hide'
        p18 = 'hide'
        p19 = 'hide'
        p41 = 'hide'
        p42 = 'hide'
        p43 = 'hide'
        p44 = 'hide'
        p45 = 'hide'
        p46 = 'hide'
        p47 = 'hide'
        p48 = 'hide'
        p49 = 'hide'
    elif select_level()[0] < 3:
        p11 = 'hide'
        p12 = 'hide'
        p13 = 'hide'
        p14 = 'hide'
        p15 = 'hide'
        p16 = 'hide'
        p17 = 'hide'
        p18 = 'hide'
        p19 = 'hide'
        p41 = 'hide'
        p42 = 'hide'
        p43 = 'hide'
        p44 = 'hide'
        p45 = 'hide'
        p46 = 'hide'
        p47 = 'hide'
        p48 = 'hide'
        p49 = 'hide'

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

    return render(request, 'prac_pro.html', {
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
        "visibility_major": visibility(select_level()[1])[0],
        "visibility_minor": visibility(select_level()[1])[1],
        "p1": p1,
        "p2": p2,
        "p3": p3,
        "p4": p4,
        "p5": p5,
        "p6": p6,
        "p7": p7,
        "p8": p8,
        "p9": p9,
        "p11": p11,
        "p12": p12,
        "p13": p13,
        "p14": p14,
        "p15": p15,
        "p16": p16,
        "p17": p17,
        "p18": p18,
        "p19": p19,
        "p21": p21,
        "p22": p22,
        "p23": p23,
        "p24": p24,
        "p25": p25,
        "p26": p26,
        "p27": p27,
        "p28": p28,
        "p29": p29,
        "p31": p31,
        "p32": p32,
        "p33": p33,
        "p34": p34,
        "p35": p35,
        "p36": p36,
        "p37": p37,
        "p38": p38,
        "p39": p39,
        "p41": p41,
        "p42": p42,
        "p43": p43,
        "p44": p44,
        "p45": p45,
        "p46": p46,
        "p47": p47,
        "p48": p48,
        "p49": p49,
        "p51": p51,
        "p52": p52,
        "p53": p53,
        "p54": p54,
        "p55": p55,
        "p56": p56,
        "p57": p57,
        "p58": p58,
        "p59": p59,
        "ans_1": ans_1,
        "ans_2": ans_2,
        "ans_3": ans_3,
        "ans_4": ans_4,
        "ans_5": ans_5,
        "ans_class_1": pro_ans_class()[0],
        "ans_class_2": pro_ans_class()[1],
        "ans_class_3": pro_ans_class()[2],
        "ans_class_4": pro_ans_class()[3],
        "ans_class_5": pro_ans_class()[4]
    })


def left_column_pro(request):
    return render(request, 'pro/left_column_pro.html', {
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
            question_count = (LvlPro.objects.filter(user=current_user).order_by('-id')[0]).hi_score
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


def table_pro(request):
    global p11
    global p12
    global p13
    global p14
    global p15
    global p16
    global p17
    global p18
    global p19
    global p21
    global p22
    global p23
    global p24
    global p25
    global p26
    global p27
    global p28
    global p29
    global p41
    global p42
    global p43
    global p44
    global p45
    global p46
    global p47
    global p48
    global p49
    global p51
    global p52
    global p53
    global p54
    global p55
    global p56
    global p57
    global p58
    global p59

    if select_level()[0] < 2:
        p21 = 'hide'
        p22 = 'hide'
        p23 = 'hide'
        p24 = 'hide'
        p25 = 'hide'
        p26 = 'hide'
        p27 = 'hide'
        p28 = 'hide'
        p29 = 'hide'
        p51 = 'hide'
        p52 = 'hide'
        p53 = 'hide'
        p54 = 'hide'
        p55 = 'hide'
        p56 = 'hide'
        p57 = 'hide'
        p58 = 'hide'
        p59 = 'hide'
        p11 = 'hide'
        p12 = 'hide'
        p13 = 'hide'
        p14 = 'hide'
        p15 = 'hide'
        p16 = 'hide'
        p17 = 'hide'
        p18 = 'hide'
        p19 = 'hide'
        p41 = 'hide'
        p42 = 'hide'
        p43 = 'hide'
        p44 = 'hide'
        p45 = 'hide'
        p46 = 'hide'
        p47 = 'hide'
        p48 = 'hide'
        p49 = 'hide'
    elif select_level()[0] < 3:
        p11 = 'hide'
        p12 = 'hide'
        p13 = 'hide'
        p14 = 'hide'
        p15 = 'hide'
        p16 = 'hide'
        p17 = 'hide'
        p18 = 'hide'
        p19 = 'hide'
        p41 = 'hide'
        p42 = 'hide'
        p43 = 'hide'
        p44 = 'hide'
        p45 = 'hide'
        p46 = 'hide'
        p47 = 'hide'
        p48 = 'hide'
        p49 = 'hide'

    sub_lvl_int()

    return render(request, 'pro/table_pro.html', {
        "visibility_major": visibility(select_level()[1])[0],
        "visibility_minor": visibility(select_level()[1])[1],
        "p1": p1,
        "p2": p2,
        "p3": p3,
        "p4": p4,
        "p5": p5,
        "p6": p6,
        "p7": p7,
        "p8": p8,
        "p9": p9,
        "p11": p11,
        "p12": p12,
        "p13": p13,
        "p14": p14,
        "p15": p15,
        "p16": p16,
        "p17": p17,
        "p18": p18,
        "p19": p19,
        "p21": p21,
        "p22": p22,
        "p23": p23,
        "p24": p24,
        "p25": p25,
        "p26": p26,
        "p27": p27,
        "p28": p28,
        "p29": p29,
        "p31": p31,
        "p32": p32,
        "p33": p33,
        "p34": p34,
        "p35": p35,
        "p36": p36,
        "p37": p37,
        "p38": p38,
        "p39": p39,
        "p41": p41,
        "p42": p42,
        "p43": p43,
        "p44": p44,
        "p45": p45,
        "p46": p46,
        "p47": p47,
        "p48": p48,
        "p49": p49,
        "p51": p51,
        "p52": p52,
        "p53": p53,
        "p54": p54,
        "p55": p55,
        "p56": p56,
        "p57": p57,
        "p58": p58,
        "p59": p59,
        "ans_1": ans_1,
        "ans_2": ans_2,
        "ans_3": ans_3,
        "ans_4": ans_4,
        "ans_5": ans_5,
        "ans_class_1": pro_ans_class()[0],
        "ans_class_2": pro_ans_class()[1],
        "ans_class_3": pro_ans_class()[2],
        "ans_class_4": pro_ans_class()[3],
        "ans_class_5": pro_ans_class()[4]
    })


def pro_ans_class():
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


def table_pro_ans(request):
    return render(request, 'pro/table_pro_ans.html', {
        "ans_1": ans_1,
        "ans_2": ans_2,
        "ans_3": ans_3,
        "ans_4": ans_4,
        "ans_5": ans_5,
        "ans_class_1": pro_ans_class()[0],
        "ans_class_2": pro_ans_class()[1],
        "ans_class_3": pro_ans_class()[2],
        "ans_class_4": pro_ans_class()[3],
        "ans_class_5": pro_ans_class()[4]
    })


def sub_lvl_int():
    global p1
    global p2
    global p3
    global p4
    global p5
    global p6
    global p7
    global p8
    global p9
    global p11
    global p12
    global p13
    global p14
    global p15
    global p16
    global p17
    global p18
    global p19
    global p21
    global p22
    global p23
    global p24
    global p25
    global p26
    global p27
    global p28
    global p29
    global p31
    global p32
    global p33
    global p34
    global p35
    global p36
    global p37
    global p38
    global p39
    global p41
    global p42
    global p43
    global p44
    global p45
    global p46
    global p47
    global p48
    global p49
    global p51
    global p52
    global p53
    global p54
    global p55
    global p56
    global p57
    global p58
    global p59

    if select_level()[1] <= 0:
        p8 = 'button_prog p8 na'
        p18 = 'button_prog p18 na'
        p28 = 'button_prog p28 na'
    else:
        p8 = 'button_prog p8'
        p18 = 'button_prog p18'
        p28 = 'button_prog p28'
    if select_level()[1] <= 2:
        p4 = 'button_prog p4 na'
        p14 = 'button_prog p14 na'
        p24 = 'button_prog p24 na'
    else:
        p4 = 'button_prog p4'
        p14 = 'button_prog p14'
        p24 = 'button_prog p24'
    if select_level()[1] <= 4:
        p3 = 'button_prog p3 na'
        p13 = 'button_prog p13 na'
        p23 = 'button_prog p23 na'
    else:
        p3 = 'button_prog p3'
        p13 = 'button_prog p13'
        p23 = 'button_prog p23'
    if select_level()[1] <= 6:
        p7 = 'button_prog p7 na'
        p17 = 'button_prog p17 na'
        p27 = 'button_prog p27 na'
    else:
        p7 = 'button_prog p7'
        p17 = 'button_prog p17'
        p27 = 'button_prog p27'
    if select_level()[1] <= 8:
        p9 = 'button_prog p9 na'
        p19 = 'button_prog p19 na'
        p29 = 'button_prog p29 na'
    else:
        p9 = 'button_prog p9'
        p19 = 'button_prog p19'
        p29 = 'button_prog p29'
    if select_level()[1] <= 10:
        p2 = 'button_prog p2 na'
        p12 = 'button_prog p12 na'
        p22 = 'button_prog p22 na'
    else:
        p2 = 'button_prog p2'
        p12 = 'button_prog p12'
        p22 = 'button_prog p22'




    if select_level()[1] <= 1:
        p35 = 'button_prog p35 na'
        p45 = 'button_prog p45 na'
        p55 = 'button_prog p55 na'
    else:
        p35 = 'button_prog p35'
        p45 = 'button_prog p45'
        p55 = 'button_prog p55'
    if select_level()[1] <= 3:
        p38 = 'button_prog p38 na'
        p48 = 'button_prog p48 na'
        p58 = 'button_prog p58 na'
    else:
        p38 = 'button_prog p38'
        p48 = 'button_prog p48'
        p58 = 'button_prog p58'
    if select_level()[1] <= 5:
        p33 = 'button_prog p33 na'
        p43 = 'button_prog p43 na'
        p53 = 'button_prog p53 na'
    else:
        p33 = 'button_prog p33'
        p43 = 'button_prog p43'
        p53 = 'button_prog p53'
    if select_level()[1] <= 7:
        p39 = 'button_prog p39 na'
        p49 = 'button_prog p49 na'
        p59 = 'button_prog p59 na'
    else:
        p39 = 'button_prog p39'
        p49 = 'button_prog p49'
        p59 = 'button_prog p59'
    if select_level()[1] <= 9:
        p36 = 'button_prog p36 na'
        p46 = 'button_prog p46 na'
        p56 = 'button_prog p56 na'
    else:
        p36 = 'button_prog p36'
        p46 = 'button_prog p46'
        p56 = 'button_prog p56'
    if select_level()[1] <= 11:
        p32 = 'button_prog p32 na'
        p42 = 'button_prog p42 na'
        p52 = 'button_prog p52 na'
    else:
        p32 = 'button_prog p32'
        p42 = 'button_prog p42'
        p52 = 'button_prog p52'

    if select_level()[0] < 2:
        p21 = 'hide'
        p22 = 'hide'
        p23 = 'hide'
        p24 = 'hide'
        p25 = 'hide'
        p26 = 'hide'
        p27 = 'hide'
        p28 = 'hide'
        p29 = 'hide'
        p51 = 'hide'
        p52 = 'hide'
        p53 = 'hide'
        p54 = 'hide'
        p55 = 'hide'
        p56 = 'hide'
        p57 = 'hide'
        p58 = 'hide'
        p59 = 'hide'
        p11 = 'hide'
        p12 = 'hide'
        p13 = 'hide'
        p14 = 'hide'
        p15 = 'hide'
        p16 = 'hide'
        p17 = 'hide'
        p18 = 'hide'
        p19 = 'hide'
        p41 = 'hide'
        p42 = 'hide'
        p43 = 'hide'
        p44 = 'hide'
        p45 = 'hide'
        p46 = 'hide'
        p47 = 'hide'
        p48 = 'hide'
        p49 = 'hide'
    elif select_level()[0] < 3:
        p11 = 'hide'
        p12 = 'hide'
        p13 = 'hide'
        p14 = 'hide'
        p15 = 'hide'
        p16 = 'hide'
        p17 = 'hide'
        p18 = 'hide'
        p19 = 'hide'
        p41 = 'hide'
        p42 = 'hide'
        p43 = 'hide'
        p44 = 'hide'
        p45 = 'hide'
        p46 = 'hide'
        p47 = 'hide'
        p48 = 'hide'
        p49 = 'hide'

def all_lvls(request):
    global p11
    global p12
    global p13
    global p14
    global p15
    global p16
    global p17
    global p18
    global p19
    global p21
    global p22
    global p23
    global p24
    global p25
    global p26
    global p27
    global p28
    global p29
    global p41
    global p42
    global p43
    global p44
    global p45
    global p46
    global p47
    global p48
    global p49
    global p51
    global p52
    global p53
    global p54
    global p55
    global p56
    global p57
    global p58
    global p59

    if select_level()[0] < 2:
        p21 = 'hide'
        p22 = 'hide'
        p23 = 'hide'
        p24 = 'hide'
        p25 = 'hide'
        p26 = 'hide'
        p27 = 'hide'
        p28 = 'hide'
        p29 = 'hide'
        p51 = 'hide'
        p52 = 'hide'
        p53 = 'hide'
        p54 = 'hide'
        p55 = 'hide'
        p56 = 'hide'
        p57 = 'hide'
        p58 = 'hide'
        p59 = 'hide'
        p11 = 'hide'
        p12 = 'hide'
        p13 = 'hide'
        p14 = 'hide'
        p15 = 'hide'
        p16 = 'hide'
        p17 = 'hide'
        p18 = 'hide'
        p19 = 'hide'
        p41 = 'hide'
        p42 = 'hide'
        p43 = 'hide'
        p44 = 'hide'
        p45 = 'hide'
        p46 = 'hide'
        p47 = 'hide'
        p48 = 'hide'
        p49 = 'hide'
    elif select_level()[0] < 3:
        p11 = 'hide'
        p12 = 'hide'
        p13 = 'hide'
        p14 = 'hide'
        p15 = 'hide'
        p16 = 'hide'
        p17 = 'hide'
        p18 = 'hide'
        p19 = 'hide'
        p41 = 'hide'
        p42 = 'hide'
        p43 = 'hide'
        p44 = 'hide'
        p45 = 'hide'
        p46 = 'hide'
        p47 = 'hide'
        p48 = 'hide'
        p49 = 'hide'

    global question_count
    global practice_modus
    return render(request, 'pro/lvl_pro.html', {
        "lvl": 'Level ' + str(int(select_level()[0])),
        "sub_lvl": str(int(select_level()[1]) + 1),
        "sub_level_cap": '/' + str(sub_level_cap + 1),
        "max_hi_score": select_level()[2],
        "prog_count_int": question_count / 10,
        "prog_count": question_count,
        "practice_modus": practice_modus,
        "visibility_major": visibility(select_level()[1])[0],
        "visibility_minor": visibility(select_level()[1])[1],
        "p1": p1,
        "p2": p2,
        "p3": p3,
        "p4": p4,
        "p5": p5,
        "p6": p6,
        "p7": p7,
        "p8": p8,
        "p9": p9,
        "p11": p11,
        "p12": p12,
        "p13": p13,
        "p14": p14,
        "p15": p15,
        "p16": p16,
        "p17": p17,
        "p18": p18,
        "p19": p19,
        "p21": p21,
        "p22": p22,
        "p23": p23,
        "p24": p24,
        "p25": p25,
        "p26": p26,
        "p27": p27,
        "p28": p28,
        "p29": p29,
        "p31": p31,
        "p32": p32,
        "p33": p33,
        "p34": p34,
        "p35": p35,
        "p36": p36,
        "p37": p37,
        "p38": p38,
        "p39": p39,
        "p41": p41,
        "p42": p42,
        "p43": p43,
        "p44": p44,
        "p45": p45,
        "p46": p46,
        "p47": p47,
        "p48": p48,
        "p49": p49,
        "p51": p51,
        "p52": p52,
        "p53": p53,
        "p54": p54,
        "p55": p55,
        "p56": p56,
        "p57": p57,
        "p58": p58,
        "p59": p59,
        "ans_1": ans_1,
        "ans_2": ans_2,
        "ans_3": ans_3,
        "ans_4": ans_4,
        "ans_5": ans_5,
        "ans_class_1": pro_ans_class()[0],
        "ans_class_2": pro_ans_class()[1],
        "ans_class_3": pro_ans_class()[2],
        "ans_class_4": pro_ans_class()[3],
        "ans_class_5": pro_ans_class()[4]
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

pro_sub_1 = ['I', 'IV', 'V']
pro_sub_2 = ['i', 'iv', 'V']
pro_sub_3 = ['I', 'IV', 'V', 'vi']
pro_sub_4 = ['i', 'iv', 'IV', 'V']
pro_sub_5 = ['I', 'iii', 'IV', 'V', 'vi']
pro_sub_6 = ['i', 'iv', 'IV', 'V', 'VI']
pro_sub_7 = ['I', 'bIII', 'iii', 'IV', 'V', 'vi']
pro_sub_8 = ['i', 'III', 'iv', 'IV', 'V', 'VI']
pro_sub_9 = ['I', 'bIII', 'iii', 'IV', 'V', 'bVI', 'vi']
pro_sub_10 = ['i', 'III', 'iv', 'IV', 'V', 'VI', 'VII']
pro_sub_11 = ['I', 'vIII', 'iii', 'IV', 'V', 'bVI', 'vi', 'bVII']
pro_sub_12 = ['i', 'III', 'iv', 'IV', 'v', 'V', 'VI', 'VII']
pro_sub_13 = ['I', 'ii', 'bIII', 'iii', 'IV', 'V', 'bVI', 'vi', 'bVII']
pro_sub_14 = ['i', 'IIb', 'III', 'iv', 'IV', 'v', 'V', 'VI', 'VII']

sub_levels = [
    pro_sub_1,
    pro_sub_2,
    pro_sub_3,
    pro_sub_4,
    pro_sub_5,
    pro_sub_6,
    pro_sub_7,
    pro_sub_8,
    pro_sub_9,
    pro_sub_10,
    pro_sub_11,
    pro_sub_12,
    pro_sub_13,
    pro_sub_14]







