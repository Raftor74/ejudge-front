class ContestSerializer(object):

    def __init__(self, instance):
        self.instance = instance

    def get_dict(self):
        problems_list = list()
        problems = self.instance.problems.all()

        for problem in problems:
            problems_list.append({
                'id': problem.id,
                'title': problem.title
            })
        start_time = self.instance.start_time.strftime('%d.%m.%Y %H:%M')

        return {
            'name': self.instance.name,
            'duration': self.instance.duration,
            'scope_system': self.instance.scope_system,
            'start_time': start_time,
            'is_closed': self.instance.is_closed,
            'is_visible': self.instance.is_visible,
            'secret_word': self.instance.secret_word,
            'problems': problems_list
        }
