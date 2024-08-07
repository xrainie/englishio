import json

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from account.redis import _increment_learner_action, _get_user_actions_for_all_days
from .services import _get_study_word_count_for_stage, _words_for_exercises, _get_all_studywords, \
    _increment_stage, _decrement_stage
from account.models import Learner, StudyWord
from word.models import Word

@login_required
def profile(request):
    activity = _get_user_actions_for_all_days(request.user)
    study_word_count_for_stage = _get_study_word_count_for_stage(request.user)
    return render(request, 'profile/profile.html', {'user': request.user, 
                                                    'study_words': study_word_count_for_stage,
                                                    'activity': activity})

@login_required
def exercises(request):
    remaining_words = _words_for_exercises(request.user)
    return render(request, 'exercises.html', {'words': remaining_words})

@login_required
def remember_all(request):
    return render(request, 'exercises/remember_all.html')


@login_required
def biathlon(request):
    _increment_learner_action(request.user, 'start_learning_word')
    return render(request, 'exercises/biathlon.html')

def all_study_words(request):
    """Выгружает все слова, которые нужно сегодня повторить """
    user = request.user
    words_data = _get_all_studywords(user)
    return JsonResponse({'data': words_data}, content_type='application/json', safe=False)

# -----------

@csrf_exempt
def create_study_word(request):
    """Добавить к пользователю изучаемое слово"""
    user = request.user
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        word = data['word']
    new_word = StudyWord.objects.create(learner=Learner.objects.get(user=user), word=Word.objects.get(name=word))
    new_word.save()
    _increment_learner_action(user, 'start_learning_word')
    return JsonResponse({'message': 'Данные успешно получены и обработаны.'})


@csrf_exempt
def is_study_word(request):
    """Проверить слово, изучается ли пользователем"""
    user = request.user
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        word = data['word']
    try:
        message = {'message': 'yes'}
        obj = StudyWord.objects.get(learner=Learner.objects.get(user=user), word=Word.objects.get(name=word))
        message['learning'] = 'yes' if obj.stage_learning_word == 'Learned' else 'no'
        return JsonResponse(message)
    except StudyWord.DoesNotExist:
        message = {'message': 'no'}
        return JsonResponse(message)


@csrf_exempt
def change_level_word(request):
    """Изменить этап изучаемого слово на один"""
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        word = StudyWord.objects.get(word__name=data['word'])
        if data['level'] == 'up':
            next_stage = _increment_stage(word.stage_learning_word)
            word.stage_learning_word = next_stage
            word.save()
            _increment_learner_action(request.user, f'up to {next_stage}')
        elif data['level'] == 'down':
            prev_stage = _decrement_stage(word.stage_learning_word)
            word.stage_learning_word = prev_stage
            word.save()
        return JsonResponse({'message': 'Данные успешно получены и обработаны.'})
    else:
        return JsonResponse({'message': 'Метод не поддерживается.'}, status=405)