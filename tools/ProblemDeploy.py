import json
import os
import shutil
from django.conf import settings
from django.template.loader import render_to_string


class ProblemDeploy(object):

    EOF = "\n"
    DESCRIPTION_FILENAME = "statement.xml"
    INPUT_TEST_FILE_EXTENSION = '.dat'
    OUTPUT_TEST_FILE_EXTENSION = '.ans'

    def __init__(self, deploy_path, short_id, problem):
        self.deploy_path = deploy_path
        self.short_id = short_id
        self.problem = problem
        self.problem_dir = os.path.join(deploy_path, short_id)
        self.tests_dir = os.path.join(self.problem_dir, 'tests')

    def create_directory(self, dir_path):
        try:
            os.mkdir(dir_path)
        except FileExistsError:
            pass

        return True

    def save_file(self, file_name, file_content):
        with open(file_name, mode="w", encoding="utf-8") as _file:
            _file.write(file_content)

    def normalize_test_number(self, number):
        normalized_number = str(number)
        while(len(normalized_number) != 3):
            normalized_number = '0' + normalized_number
        return normalized_number

    def wrap_input_output_in_tags(self, input, output):
        return self.wrap_input_string_in_tag(input) + self.EOF + self.wrap_output_string_in_tag(output)

    def wrap_input_string_in_tag(self, text):
        return "<input>" + str(text) + "</input>"

    def wrap_output_string_in_tag(self, text):
        return "<output>" + str(text) + "</output>"

    def wrap_string_in_example_tag(self, string):
        return "<example>" + self.EOF + string + self.EOF + "</example>"

    def parse_json_to_list(self, _json):
        try:
            _list = json.loads(_json)
        except json.JSONDecodeError:
            _list = list()
        return _list

    def get_problem_examples_string(self):
        example_tests = self.parse_json_to_list(self.problem.tests_examples)
        examples_string = ''

        for test in example_tests:
            input_output_string = self.wrap_input_output_in_tags(test["input"], test["output"])
            wrapped_input_output_string = self.wrap_string_in_example_tag(input_output_string)
            examples_string += wrapped_input_output_string + self.EOF
        return examples_string

    def remove_directory_tree(self, dir_path):
        shutil.rmtree(dir_path, True)
        return True

    def create_problem_dir(self):
        self.create_directory(self.problem_dir)
        return self

    def create_tests_dir(self):
        self.create_directory(self.tests_dir)
        return self

    def create_problem_dirs(self):
        return self.create_problem_dir().create_tests_dir()

    def create_problem_tests(self):
        problem_tests = self.parse_json_to_list(self.problem.tests)
        test_number = 1
        for test in problem_tests:
            normalized_test_number = self.normalize_test_number(test_number)
            input_data = test['input']
            output_data = test['output']
            input_test_file_name = normalized_test_number + self.INPUT_TEST_FILE_EXTENSION
            output_test_file_name = normalized_test_number + self.OUTPUT_TEST_FILE_EXTENSION
            input_test_file_path = os.path.join(self.tests_dir, input_test_file_name)
            output_test_file_path = os.path.join(self.tests_dir, output_test_file_name)
            self.save_file(input_test_file_path, input_data)
            self.save_file(output_test_file_path, output_data)
            test_number += 1
        return True


    def create_problem_description_file(self):
        problem_description_file_path = os.path.join(self.problem_dir, self.DESCRIPTION_FILENAME)
        template = settings.EJUDGE_PROBLEM_DESCRIPTION_TEMPLATE_FILE_LOCAL_PATH
        context = {
            'short_id': str(self.short_id),
            'title': str(self.problem.title),
            'description': str(self.problem.description),
            'examples': str(self.get_problem_examples_string())
        }
        problem_description_string = render_to_string(template_name=template, context=context)
        self.save_file(problem_description_file_path, problem_description_string)
        return self

    def deploy(self):
        self.create_problem_dirs()
        self.create_problem_description_file()
        self.create_problem_tests()
        pass

    def remove(self):
        return self.remove_directory_tree(self.problem_dir)