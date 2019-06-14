class ContestBase (object):

    def __init__(self):
        self.id = ''
        self.last_error = ''


class ContestValidator(ContestBase):

    def __init__(self):
        super().__init__()
        self.validation_error = ''


class ContestCreate(ContestValidator):

    def __init__(self, post_data, owner=None):
        super().__init__()
        pass

    def create_contest(self):
        pass


class ContestUpdate(ContestCreate):

    def __init__(self, contest_id, post_data):
        super().__init__(post_data)
        pass

    def update_contest(self):
        pass

