class ProblemSerializer(object):

    def __init__(self, instance):
        self.instance = instance

    def get_dict(self):
        return {
            'title': self.instance.title,
            'description': self.instance.description,
            'epsilon': self.instance.epsilon,
            'max_vm_size': self.instance.max_vm_size,
            'max_exec_time': self.instance.max_exec_time,
            'tests_examples': self.instance.tests_examples,
            'tests': self.instance.tests,
            'comparison': self.instance.comparison,
            'is_visible': self.instance.is_visible,
        }
