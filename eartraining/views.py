from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from pitch.models import LvlPit
from intervals.models import LvlInt
from melodic_dictation.models import LvlMel
from triads.models import LvlTri
from seventh_chords.models import LvlSev
from extended_chords.models import LvlExt
from progressions.models import LvlPro
from django.db.models import Max

current_user = ''

def calc_lvl_score(level, sub_cap, module):
    a = 0
    for i in range(0, sub_cap + 1):
        a = a + int(module.objects.filter(lvl=level, sub_lvl=i, user=current_user).aggregate(Max('hi_score'))['hi_score__max'] or 0)
    return int(float("%.2f" % round(a / (sub_cap + 1), 2)))


def calc_hi_scores(sub_cap, module):
    lvl_1_hi_score = calc_lvl_score(1, sub_cap, module)
    lvl_2_hi_score = calc_lvl_score(2, sub_cap, module)
    lvl_3_hi_score = calc_lvl_score(3, sub_cap, module)
    lvl_4_hi_score = calc_lvl_score(4, sub_cap, module)
    lvl_5_hi_score = calc_lvl_score(5, sub_cap, module)
    lvl_6_hi_score = calc_lvl_score(6, sub_cap, module)
    tot_int_score_1 = (lvl_1_hi_score + lvl_2_hi_score + lvl_3_hi_score +
                       lvl_4_hi_score + lvl_5_hi_score + lvl_6_hi_score) / 6
    tot_int_score = int(float("%.2f" % round(tot_int_score_1, 2)))

    return [lvl_1_hi_score, lvl_2_hi_score, lvl_3_hi_score,
            lvl_4_hi_score, lvl_5_hi_score, lvl_6_hi_score, tot_int_score]


def index(request):
    global current_user
    current_user = request.user
    tot_pit_score = calc_lvl_score(1, 4, LvlPit)
    tot_int_score = calc_hi_scores(10, LvlInt)[6]
    tot_mel_score = calc_hi_scores(13, LvlMel)[6]
    tot_tri_score = calc_hi_scores(4, LvlTri)[6]
    tot_sev_score = calc_hi_scores(7, LvlSev)[6]
    tot_ext_score = calc_hi_scores(11, LvlExt)[6]
    tot_pro_score = calc_hi_scores(13, LvlPro)[6]
    return render(request, 'index.html',{
        'tot_pit_score' :tot_pit_score,
        'tot_int_score' :tot_int_score,
        'tot_mel_score': tot_mel_score,
        'tot_tri_score': tot_tri_score,
        'tot_sev_score': tot_sev_score,
        'tot_ext_score': tot_ext_score,
        'tot_pro_score': tot_pro_score
    })


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def profile(request):
    tot_pit_score = calc_lvl_score(1, 4, LvlPit)
    tot_int_score = calc_hi_scores(10, LvlInt)[6]
    tot_mel_score = calc_hi_scores(13, LvlMel)[6]
    tot_tri_score = calc_hi_scores(4, LvlTri)[6]
    tot_sev_score = calc_hi_scores(7, LvlSev)[6]
    tot_ext_score = calc_hi_scores(11, LvlExt)[6]
    tot_pro_score = calc_hi_scores(13, LvlPro)[6]
    return render(request, 'user.html', {
        'tot_pit_score' :tot_pit_score,
        'tot_int_score' :tot_int_score,
        'tot_mel_score': tot_mel_score,
        'tot_tri_score': tot_tri_score,
        'tot_sev_score': tot_sev_score,
        'tot_ext_score': tot_ext_score,
        'tot_pro_score': tot_pro_score
    })

def pitch(request):
    return render(request, 'prac_pitch.html')


def melodic_dictation(request):
    return render(request, 'prac_mel_dic.html')

def triads(request):
    return render(request, 'prac_triads.html')

def seventh_chords(request):
    return render(request, 'prac_7th.html')

def extended_chords(request):
    return render(request, 'prac_extended.html')

def chord_progressions(request):
    return render(request, 'prac_progressions.html')


def practice(request):
    return render(request, 'practice.html')

from django.contrib.auth.models import User

def user_overview(request):
    users = User.objects.all()

    return render(request, 'user_overview.html', {
        'users' :users
    })
