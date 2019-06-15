from problems.models import Problems


class ProblemBase(object):

    def __init__(self):
        self.id = ''
        self.title = ''
        self.description = ''
        self.epsilon = ''
        self.max_vm_size = ''
        self.max_exec_time = ''
        self.tests_examples = ''
        self.tests = ''
        self.comparison = ''
        self.owner = None
        self.is_visible = False
        self.last_error = ''


class ProblemValidator(ProblemBase):

    def __init__(self):
        super().__init__()
        self.validation_error = ''

    def validate_on_not_empty_string(self, string):
        return len(string) > 0

    def validate_on_int(self, value):
        try:
            parse_success = int(value)
        except ValueError:
            return False

        return True

    def validate_title(self):
        if not self.validate_on_not_empty_string(self.title):
            raise Exception("Не указано название задачи")
        return self

    def validate_description(self):
        if not self.validate_on_not_empty_string(self.description):
            raise Exception("Не указано описание задачи")
        return self

    def validate_max_vm_size(self):
        if not self.validate_on_int(self.max_vm_size):
            raise Exception("Неверный формат для ограничения по памяти")

        if not int(self.max_vm_size) > 0:
            raise Exception("Не указано ограничение по памяти")

        return self

    def validate_max_exec_time(self):
        if not self.validate_on_int(self.max_exec_time):
            raise Exception("Неверный формат для ограничения по времени")

        if not int(self.max_exec_time) > 0:
            raise Exception("Не указано ограничение по времени")

        return self

    def validate_comparison(self):
        if not self.validate_on_not_empty_string(self.comparison):
            raise Exception("Не указан тип сравнения ответов")

        return self

    def validate_on_problem_exist(self):
        try:
            problem = Problems.objects.get(pk=self.id)
        except Problems.DoesNotExist:
            raise Exception("Задача не существует")

        return self

    def validate_on_create(self):
        try:
            self.validate_title()\
                .validate_description()\
                .validate_max_vm_size()\
                .validate_max_exec_time()\
                .validate_comparison()
        except Exception as e:
            self.validation_error = str(e)
            return False

        return True

    def validate_on_update(self):
        try:
            self.validate_on_problem_exist()\
                .validate_title() \
                .validate_description() \
                .validate_max_vm_size() \
                .validate_max_exec_time() \
                .validate_comparison()
        except Exception as e:
            self.validation_error = str(e)
            return False

        return True


class ProblemCreate(ProblemValidator):

    def __init__(self, post_request, owner=None):
        super().__init__()
        self.owner = owner
        self.title = post_request.get('title', '')
        self.description = post_request.get('description', '')
        self.epsilon = post_request.get('epsilon', '')
        self.max_vm_size = post_request.get('max_vm_size', '')
        self.max_exec_time = post_request.get('max_exec_time', '')
        self.comparison = post_request.get('checker', '')
        self.is_visible = post_request.get('is_visible', False)
        self.tests_examples = post_request.get('tests_examples', '')
        self.tests = post_request.get('tests', '')

    def create_problem(self):
        if not self.validate_on_create():
            self.last_error = self.validation_error
            return False

        problem = Problems.objects.create(
            title=self.title,
            description=self.description,
            epsilon=self.epsilon,
            max_vm_size=int(self.max_vm_size),
            max_exec_time=int(self.max_exec_time),
            comparison=self.comparison,
            is_visible=bool(self.is_visible),
            tests_examples=self.tests_examples,
            tests=self.tests,
            owner=self.owner
        )

        return problem


class ProblemUpdate(ProblemCreate):

    def __init__(self, problem_id, post_request):
        super().__init__(post_request, None)
        self.id = problem_id

    def update_problem(self):
        if not self.validate_on_update():
            self.last_error = self.validation_error
            return False

        problem = Problems.objects.get(pk=self.id)
        problem.title = self.title
        problem.description = self.description
        problem.epsilon = self.epsilon
        problem.max_vm_size = int(self.max_vm_size)
        problem.max_exec_time=int(self.max_exec_time)
        problem.comparison = self.comparison
        problem.is_visible = bool(self.is_visible)
        problem.tests_examples = self.tests_examples
        problem.tests = self.tests
        problem.save()

        return problem
