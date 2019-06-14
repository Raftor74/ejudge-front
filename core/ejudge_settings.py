import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Конфигурационные параметры системы Ejudge

# Полный путь к директории управления системой Ejudge
EJUDGE_CONTROL_DIR = '/home/ejudge/inst-ejudge/bin/'

# Полный путь к директории контестов системы Ejudge
EJUDGE_CONTESTS_DIR = '/home/judges/'

# Полный путь к директории описания контестов системы Ejudge
EJUDGE_CONTESTS_CONFIG_DIR = '/home/judges/data/contests/'

# Наименование скрипта управления Ejudge
EJUDGE_CONTROL_SCRIPT_NAME = 'ejudge-control'

# Полный путь к программе запуска системы Ejudge
EJUDGE_CONTROL_SCRIPT_PATH = os.path.join(EJUDGE_CONTROL_DIR, EJUDGE_CONTROL_SCRIPT_NAME)

# Название папки с шаблонами конфигурационных файлов Ejudge
EJUDGE_CONFIG_TEMPLATES_DIR_NAME = 'ejudge_templates'

# Полный путь к папке с шаблонами конфигурационных файлов Ejudge
EJUDGE_CONFIG_TEMPLATES_DIR_ABSOLUTE_PATH = os.path.join(BASE_DIR, EJUDGE_CONFIG_TEMPLATES_DIR_NAME)

# Относительный путь к папке с шаблонами конфигурационных файлов Ejudge
EJUDGE_CONFIG_TEMPLATES_DIR_LOCAL_PATH = EJUDGE_CONFIG_TEMPLATES_DIR_NAME

# Название файла шаблона конфигурации для задачи Ejudge
EJUDGE_PROBLEM_CONFIG_TEMPLATE_FILE_NAME = 'problem.cfg'

# Название файла шаблона описания для задачи Ejudge
EJUDGE_PROBLEM_DESCRIPTION_TEMPLATE_FILE_NAME = 'problem.xml'


EJUDGE_PROBLEM_CONFIG_TEMPLATE_FILE_ABSOLUTE_PATH = os.path.join(EJUDGE_CONFIG_TEMPLATES_DIR_ABSOLUTE_PATH, EJUDGE_PROBLEM_CONFIG_TEMPLATE_FILE_NAME)

EJUDGE_PROBLEM_CONFIG_TEMPLATE_FILE_LOCAL_PATH = os.path.join(EJUDGE_CONFIG_TEMPLATES_DIR_LOCAL_PATH, EJUDGE_PROBLEM_CONFIG_TEMPLATE_FILE_NAME)

EJUDGE_PROBLEM_DESCRIPTION_TEMPLATE_FILE_ABSOLUTE_PATH = os.path.join(EJUDGE_CONFIG_TEMPLATES_DIR_ABSOLUTE_PATH, EJUDGE_PROBLEM_DESCRIPTION_TEMPLATE_FILE_NAME)

EJUDGE_PROBLEM_DESCRIPTION_TEMPLATE_FILE_LOCAL_PATH = os.path.join(EJUDGE_CONFIG_TEMPLATES_DIR_LOCAL_PATH, EJUDGE_PROBLEM_DESCRIPTION_TEMPLATE_FILE_NAME)

# Название процессов для идентификации запуска Ejudge
EJUDGE_SYSTEM_REQUIRED_PROCESSES = (
    ('ej-compile', "Компиляция турниров"),
    ('ej-contests', "Обработка запросов пользователей, посылок и т.п"),
    ('ej-jobs', "Рассылка e-mail сообщений, воспроизведение звуковых записей и т. д."),
    ('ej-super-run', "Запуск решений участников"),
    ('ej-super-server', "Выполняет мониторинг активных турниров"),
    ('ej-users', "Выполняет функции сервера базы пользователей"),
)

# Типы турниров системы Ejudge
EJUDGE_CONTESTS_TYPES = (
    ('acm', 'ACM'),
)

# Проверяющие программы системы Ejudge
EJUDGE_CHECKERS_CHOICES = (
    ('cmp_file', 'Cравнение двух файлов'),
    ('cmp_file_nospace', 'Cравнение двух файлов с игнорированием повторяющихся пробелов'),
    ('cmp_bytes', 'Cравнение двух файлов байт в байт'),
    ('cmp_int', 'Cравнение двух знаковых 32-битных целых чисел'),
    ('cmp_int_seq', 'Cравнение двух последовательностей знаковых 32-битных целых чисел'),
    ('cmp_long_long', 'Cравнение двух знаковых 64-битных целых чисел'),
    ('cmp_long_long_seq', 'Сравнение двух последовательностей знаковых 64-битных целых чисел'),
    ('cmp_unsigned_int', 'Cравнение двух беззнаковых 32-битных целых чисел'),
    ('cmp_unsigned_int_seq', 'Cравнение двух последовательностей беззнаковых 32-битных целых чисел'),
    ('cmp_unsigned_long_long', 'Cравнение двух беззнаковых 64-битных целых чисел'),
    ('cmp_unsigned_long_long_seq', 'Cравнение двух последовательностей беззнаковых 64-битных целых чисел'),
    ('cmp_huge_int', 'Cравнение двух целых чисел произвольного размера'),
    ('cmp_double', 'Cравнение двух вещественных чисел двойной точности с заданной максимальной ошибкой'),
    ('cmp_double_seq', 'Cравнение двух последовательностей вещественных чисел двойной точности с заданной максимальной ошибкой'),
    ('cmp_long_double', 'Cравнение двух вещественных чисел расширенной точности с заданной максимальной ошибкой'),
    ('cmp_long_double_seq', 'Cравнение двух последовательностей вещественных чисел расширенной точности с заданной максимальной ошибкой'),
    ('cmp_sexpr', 'Cравнение двух вещественных чисел расширенной точности с заданной максимальной ошибкой'),
    ('cmp_yesno', 'Сравнение двух ответов YES или NO'),
)



