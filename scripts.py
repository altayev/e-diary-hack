import random
from datacenter.models import Chastisement, Commendation, Lesson, Mark, Schoolkid


def get_schoolkid(name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=name)
    except Schoolkid.MultipleObjectsReturned:
        print(f"Найдено несколько учеников с именем {name}.")
        return
    except Schoolkid.DoesNotExist:
        print(f"Ученика по имени {name} не существует.")
        return
    return schoolkid


def remove_chastisements(name):
    schoolkid = get_schoolkid(name)
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    for chastisement in chastisements:
        chastisement.delete()


def fix_marks(name):
    schoolkid = get_schoolkid(name)
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__lt="4")
    for mark in bad_marks:
        mark.points = 5
        mark.save()


def create_commendation(name, subject_title):
    schoolkid = get_schoolkid(name)
    commendations = [
        "Молодец!",
        "Хвалю!",
        "Отличная работа!",
        "Супер!",
        "У тебя талант!",
        "Ты сегодня прыгнул выше головы!",
        "Это как раз то, что нужно!",
        "Я тобой горжусь!",
    ]
    try:
        last_lesson = Lesson.objects.filter(year_of_study=schoolkid.year_of_study,
            group_letter=schoolkid.group_letter, subject__title=subject_title).order_by('-date')[0]
        Commendation.objects.create(text=random.choice(commendations), created=last_lesson.date,
            schoolkid=schoolkid, subject=last_lesson.subject, teacher=last_lesson.teacher)
    except AttributeError:
        return
