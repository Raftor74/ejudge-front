from __future__ import unicode_literals
from django.db import models

"""Модели для работы с пользователями в системе Ejudge"""


# Модель данных для входа пользователей
class Logins(models.Model):
    user_id = models.AutoField(primary_key=True)
    login = models.CharField(unique=True, max_length=64)
    email = models.CharField(max_length=128, blank=True, null=True)
    pwdmethod = models.IntegerField(default=2)
    password = models.CharField(max_length=128, blank=True, null=True)
    privileged = models.IntegerField(default=0)
    invisible = models.IntegerField(default=0)
    banned = models.IntegerField(default=0)
    locked = models.IntegerField(default=0)
    readonly = models.IntegerField(default=0)
    neverclean = models.IntegerField(default=0)
    simplereg = models.IntegerField(default=0)
    regtime = models.DateTimeField(auto_now_add=True, blank=True)
    logintime = models.DateTimeField(auto_now_add=True, blank=True)
    pwdtime = models.DateTimeField(auto_now_add=True, blank=True)
    changetime = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        db_table = 'logins'
        ordering = ['user_id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


# Модель данных о пользователях
class Users(models.Model):
    user = models.ForeignKey('Logins', models.CASCADE, primary_key=True)
    contest_id = models.IntegerField()
    cnts_read_only = models.IntegerField()
    instnum = models.IntegerField(blank=True, null=True)
    username = models.CharField(max_length=512, blank=True, null=True)
    pwdmethod = models.IntegerField()
    password = models.CharField(max_length=128, blank=True, null=True)
    pwdtime = models.DateTimeField()
    createtime = models.DateTimeField()
    changetime = models.DateTimeField()
    logintime = models.DateTimeField()
    inst = models.CharField(max_length=512, blank=True, null=True)
    inst_en = models.CharField(max_length=512, blank=True, null=True)
    instshort = models.CharField(max_length=512, blank=True, null=True)
    instshort_en = models.CharField(max_length=512, blank=True, null=True)
    fac = models.CharField(max_length=512, blank=True, null=True)
    fac_en = models.CharField(max_length=512, blank=True, null=True)
    facshort = models.CharField(max_length=512, blank=True, null=True)
    facshort_en = models.CharField(max_length=512, blank=True, null=True)
    homepage = models.CharField(max_length=512, blank=True, null=True)
    phone = models.CharField(max_length=512, blank=True, null=True)
    city = models.CharField(max_length=512, blank=True, null=True)
    city_en = models.CharField(max_length=512, blank=True, null=True)
    region = models.CharField(max_length=512, blank=True, null=True)
    area = models.CharField(max_length=512, blank=True, null=True)
    zip = models.CharField(max_length=512, blank=True, null=True)
    street = models.CharField(max_length=512, blank=True, null=True)
    country = models.CharField(max_length=512, blank=True, null=True)
    country_en = models.CharField(max_length=512, blank=True, null=True)
    location = models.CharField(max_length=512, blank=True, null=True)
    spelling = models.CharField(max_length=512, blank=True, null=True)
    printer = models.CharField(max_length=512, blank=True, null=True)
    languages = models.CharField(max_length=512, blank=True, null=True)
    exam_id = models.CharField(max_length=512, blank=True, null=True)
    exam_cypher = models.CharField(max_length=512, blank=True, null=True)
    field0 = models.CharField(max_length=512, blank=True, null=True)
    field1 = models.CharField(max_length=512, blank=True, null=True)
    field2 = models.CharField(max_length=512, blank=True, null=True)
    field3 = models.CharField(max_length=512, blank=True, null=True)
    field4 = models.CharField(max_length=512, blank=True, null=True)
    field5 = models.CharField(max_length=512, blank=True, null=True)
    field6 = models.CharField(max_length=512, blank=True, null=True)
    field7 = models.CharField(max_length=512, blank=True, null=True)
    field8 = models.CharField(max_length=512, blank=True, null=True)
    field9 = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        db_table = 'users'
        unique_together = (('user', 'contest_id'),)


# Информация о членах команды или личная информация индив. участников
class Members(models.Model):
    serial = models.AutoField(primary_key=True)
    user = models.ForeignKey('Logins', models.CASCADE)
    contest_id = models.IntegerField()
    role_id = models.IntegerField()
    createtime = models.DateTimeField()
    changetime = models.DateTimeField()
    firstname = models.CharField(max_length=512, blank=True, null=True)
    firstname_en = models.CharField(max_length=512, blank=True, null=True)
    middlename = models.CharField(max_length=512, blank=True, null=True)
    middlename_en = models.CharField(max_length=512, blank=True, null=True)
    surname = models.CharField(max_length=512, blank=True, null=True)
    surname_en = models.CharField(max_length=512, blank=True, null=True)
    status = models.IntegerField()
    gender = models.IntegerField()
    grade = models.IntegerField()
    grp = models.CharField(max_length=512, blank=True, null=True)
    grp_en = models.CharField(max_length=512, blank=True, null=True)
    occupation = models.CharField(max_length=512, blank=True, null=True)
    occupation_en = models.CharField(max_length=512, blank=True, null=True)
    discipline = models.CharField(max_length=512, blank=True, null=True)
    email = models.CharField(max_length=512, blank=True, null=True)
    homepage = models.CharField(max_length=512, blank=True, null=True)
    phone = models.CharField(max_length=512, blank=True, null=True)
    inst = models.CharField(max_length=512, blank=True, null=True)
    inst_en = models.CharField(max_length=512, blank=True, null=True)
    instshort = models.CharField(max_length=512, blank=True, null=True)
    instshort_en = models.CharField(max_length=512, blank=True, null=True)
    fac = models.CharField(max_length=512, blank=True, null=True)
    fac_en = models.CharField(max_length=512, blank=True, null=True)
    facshort = models.CharField(max_length=512, blank=True, null=True)
    facshort_en = models.CharField(max_length=512, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    entry_date = models.DateField(blank=True, null=True)
    graduation_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'members'


# Модель связка - группа - пользователь
class Groupmembers(models.Model):
    group = models.ForeignKey('Groups', models.CASCADE, primary_key=True)
    user = models.ForeignKey('Logins', models.CASCADE)
    rights = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        db_table = 'groupmembers'
        unique_together = (('group', 'user'),)


# Модель для групп пользователей
class Groups(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(unique=True, max_length=128)
    description = models.CharField(max_length=512, blank=True, null=True)
    created_by = models.ForeignKey('Logins', models.DO_NOTHING, db_column='created_by')
    create_time = models.DateTimeField()
    last_change_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'groups'


"""Модели для работы с контестами в системе Ejduge"""


class Clars(models.Model):
    clar_id = models.IntegerField(primary_key=True)
    uuid = models.CharField(unique=True, max_length=40)
    contest_id = models.IntegerField()
    size = models.IntegerField()
    create_time = models.DateTimeField()
    nsec = models.IntegerField()
    user_from = models.IntegerField()
    user_to = models.IntegerField()
    j_from = models.IntegerField()
    flags = models.IntegerField()
    ip_version = models.IntegerField()
    hide_flag = models.IntegerField()
    ssl_flag = models.IntegerField()
    appeal_flag = models.IntegerField()
    ip = models.CharField(max_length=64)
    locale_id = models.IntegerField()
    in_reply_to = models.IntegerField()
    in_reply_uuid = models.CharField(max_length=40, blank=True, null=True)
    run_id = models.IntegerField()
    run_uuid = models.CharField(max_length=40, blank=True, null=True)
    old_run_status = models.IntegerField()
    new_run_status = models.IntegerField()
    clar_charset = models.CharField(max_length=32, blank=True, null=True)
    subj = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'clars'
        unique_together = (('clar_id', 'contest_id'),)


class Clartexts(models.Model):
    clar_id = models.IntegerField(primary_key=True)
    contest_id = models.IntegerField()
    uuid = models.CharField(unique=True, max_length=40)
    clar_text = models.CharField(max_length=4096, blank=True, null=True)

    class Meta:
        db_table = 'clartexts'
        unique_together = (('clar_id', 'contest_id'),)


# Регистрация на контесты
class Cntsregs(models.Model):
    user = models.ForeignKey('Logins', on_delete=models.CASCADE, primary_key=True)
    contest_id = models.IntegerField()
    status = models.IntegerField(default=0)
    banned = models.IntegerField(default=0)
    invisible = models.IntegerField(default=0)
    locked = models.IntegerField(default=0)
    incomplete = models.IntegerField(default=0)
    disqualified = models.IntegerField(default=0)
    createtime = models.DateTimeField(auto_now_add=True, blank=True)
    changetime = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = 'cntsregs'
        unique_together = (('user', 'contest_id'),)


# Конфигурационные данные
class Config(models.Model):
    config_key = models.CharField(primary_key=True, max_length=64)
    config_val = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        db_table = 'config'


# Куки
class Cookies(models.Model):
    cookie = models.CharField(primary_key=True, max_length=64)
    user = models.ForeignKey('Logins', models.DO_NOTHING)
    contest_id = models.IntegerField()
    priv_level = models.IntegerField()
    role_id = models.IntegerField()
    ip_version = models.IntegerField()
    locale_id = models.IntegerField()
    recovery = models.IntegerField()
    team_login = models.IntegerField()
    ip = models.CharField(max_length=64)
    ssl_flag = models.IntegerField()
    expire = models.DateTimeField()

    class Meta:
        db_table = 'cookies'


# Запущенные контесты
class Runheaders(models.Model):
    contest_id = models.IntegerField(primary_key=True)
    start_time = models.DateTimeField()
    sched_time = models.DateTimeField()
    duration = models.IntegerField(blank=True, null=True)
    stop_time = models.DateTimeField()
    finish_time = models.DateTimeField()
    saved_duration = models.IntegerField(blank=True, null=True)
    saved_stop_time = models.DateTimeField()
    saved_finish_time = models.DateTimeField()
    last_change_time = models.DateTimeField()
    last_change_nsec = models.IntegerField()
    next_run_id = models.IntegerField()

    class Meta:
        db_table = 'runheaders'


# Информация о пользователях в запущенном контесте
class Runs(models.Model):
    run_id = models.IntegerField(primary_key=True)
    contest_id = models.IntegerField()
    size = models.IntegerField()
    create_time = models.DateTimeField()
    create_nsec = models.IntegerField()
    user_id = models.IntegerField()
    prob_id = models.IntegerField()
    lang_id = models.IntegerField()
    status = models.IntegerField()
    ssl_flag = models.IntegerField()
    ip_version = models.IntegerField()
    ip = models.CharField(max_length=64)
    hash = models.CharField(max_length=128, blank=True, null=True)
    run_uuid = models.CharField(max_length=40, blank=True, null=True)
    score = models.IntegerField()
    test_num = models.IntegerField()
    score_adj = models.IntegerField()
    locale_id = models.IntegerField()
    judge_id = models.IntegerField()
    variant = models.IntegerField()
    pages = models.IntegerField()
    is_imported = models.IntegerField()
    is_hidden = models.IntegerField()
    is_readonly = models.IntegerField()
    is_examinable = models.IntegerField()
    mime_type = models.CharField(max_length=64, blank=True, null=True)
    examiners0 = models.IntegerField()
    examiners1 = models.IntegerField()
    examiners2 = models.IntegerField()
    exam_score0 = models.IntegerField()
    exam_score1 = models.IntegerField()
    exam_score2 = models.IntegerField()
    last_change_time = models.DateTimeField()
    last_change_nsec = models.IntegerField()
    is_marked = models.IntegerField()
    is_saved = models.IntegerField()
    saved_status = models.IntegerField()
    saved_score = models.IntegerField()
    saved_test = models.IntegerField()
    passed_mode = models.IntegerField()
    eoln_type = models.IntegerField()
    store_flags = models.IntegerField()
    token_flags = models.IntegerField()
    token_count = models.IntegerField()

    class Meta:
        db_table = 'runs'
        unique_together = (('run_id', 'contest_id'),)