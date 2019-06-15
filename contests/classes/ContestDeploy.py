import string
from django.conf import settings
from pytz import timezone
from tools import FileManager, ProblemDeploy
from django.template.loader import render_to_string


class ContestDeploy(FileManager):

    CONTEST_SCHED_TIME_FORMAT = '%Y/%m/%d %H:%M:00'

    def __init__(self, contest):
        self.instance = contest
        self.problems_config_list = list()

    def is_deployed(self):
        if not len(self.instance.ejudge_id):
            return False

        contest_dir = self.instance.contest_dir
        contest_problems_dir = self.instance.problems_dir
        config_file_path = self.instance.config_path
        description_file_path = self.instance.xml_config
        contest_dir_exist = self.is_dir_exist(contest_dir)
        contest_problems_dir_exist = self.is_dir_exist(contest_problems_dir)
        config_file_path_exist = self.is_file_exist(config_file_path)
        description_file_path_exist = self.is_file_exist(description_file_path)
        return contest_dir_exist and contest_problems_dir_exist and config_file_path_exist and description_file_path_exist

    def get_contest_deploy_status(self):
        contest_dir = self.instance.contest_dir
        contest_problems_dir = self.instance.problems_dir
        config_file_path = self.instance.config_path
        description_file_path = self.instance.xml_config

        status = [
            {
                "name": "Основная директория турнира",
                "path": contest_dir,
                "exist": self.is_dir_exist(contest_dir)
            },
            {
                "name": "Директория задач турнира",
                "path": contest_problems_dir,
                "exist": self.is_dir_exist(contest_problems_dir)
            },
            {
                "name": "Файл конфигурации турнира",
                "path": config_file_path,
                "exist": self.is_file_exist(config_file_path)
            },
            {
                "name": "XML файл описания турнира",
                "path": description_file_path,
                "exist": self.is_file_exist(description_file_path)
            },
        ]
        return status


    def remove_contest_dirs(self):
        contest_dir = self.instance.contest_dir
        self.remove_directory_tree(contest_dir)
        return self

    def create_contest_included_var_dirs(self):
        included_dirs = self.instance.included_var_dirs
        for var_dir in included_dirs:
            self.create_directory_tree(var_dir)
        return self

    def create_contest_var_dir(self):
        var_dir = self.instance.var_dir
        self.create_directory_tree(var_dir)
        return self

    def create_contest_dir(self):
        contest_dir = self.instance.contest_dir
        self.create_directory_tree(contest_dir)
        return self

    def create_contest_problem_dir(self):
        contest_problems_dir = self.instance.problems_dir
        self.create_directory_tree(contest_problems_dir)
        return self

    def create_contest_config_dir(self):
        contest_config_dir = self.instance.config_dir
        self.create_directory_tree(contest_config_dir)
        return self

    def get_problem_short_id_list(self):
        return list(string.ascii_uppercase)

    def create_contest_dirs(self):
        self.create_contest_dir()\
            .create_contest_problem_dir()\
            .create_contest_config_dir()\
            .create_contest_var_dir()\
            .create_contest_included_var_dirs()
        return self

    def get_problems_config_string(self):
        problems_config_string = ''
        for problem_config in self.problems_config_list:
            problems_config_string += problem_config + self.EOF
        return problems_config_string

    def deploy_contest_problems(self):
        contest_problems = self.instance.problems.all()
        contest_problems_dir = self.instance.problems_dir
        short_id_list = self.get_problem_short_id_list()
        max_size = len(short_id_list)
        i = 0

        for problem in contest_problems:
            if i > max_size:
                break

            short_id = short_id_list[i]
            provider = ProblemDeploy(deploy_path=contest_problems_dir, short_id=short_id, problem=problem)
            provider.deploy()
            self.problems_config_list.append(provider.problem_config)
            i += 1
        return self

    def get_contest_start_time(self):
        current_timezone = timezone(settings.TIME_ZONE)
        time_format = self.CONTEST_SCHED_TIME_FORMAT
        return self.instance.start_time.astimezone(current_timezone).strftime(time_format)


    def create_contest_config_file(self):
        config_template_path = settings.EJUDGE_CONTEST_CONFIG_TEMPLATE_FILE_LOCAL_PATH
        config_file_path = self.instance.config_path
        contest_id = int(self.instance.ejudge_id)
        contest_ejudge_id = self.instance.ejudge_id
        problems_config_string = self.get_problems_config_string()

        context = {
            'id': contest_id,
            'ejudge_id' : contest_ejudge_id,
            'duration': self.instance.duration,
            'scope_system': self.instance.scope_system,
            'problems': problems_config_string
        }

        config_string = render_to_string(template_name=config_template_path, context=context)
        self.save_file(config_file_path, config_string)
        return self

    def create_contest_description_file(self):
        description_template_path = settings.EJUDGE_CONTEST_DESCRIPTION_TEMPLATE_FILE_LOCAL_PATH
        description_file_path = self.instance.xml_config
        contest_id = int(self.instance.ejudge_id)
        contest_ejudge_id = self.instance.ejudge_id
        contest_sched_time = self.get_contest_start_time()

        context = {
            'id': contest_id,
            'ejudge_id': contest_ejudge_id,
            'sched_time': contest_sched_time,
            'name': self.instance.name
        }

        description_string = render_to_string(template_name=description_template_path, context=context)
        self.save_file(description_file_path, description_string)
        return self

    def remove_contest_description_file(self):
        description_file_path = self.instance.xml_config
        self.remove_file(description_file_path)
        return self

    def remove(self):
        self.remove_contest_dirs()
        self.remove_contest_description_file()
        return True

    # Создание всех директорий
    # Развёртывание задач
    # Создание конфигурационного файла контеста
    # Создание XML файла контеста
    def deploy(self):
        self.create_contest_dirs()
        self.deploy_contest_problems()
        self.create_contest_config_file()
        self.create_contest_description_file()
        return True