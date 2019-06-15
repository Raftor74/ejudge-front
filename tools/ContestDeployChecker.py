from tools import FileManager


class ContestDeployChecker(FileManager):

    def __init__(self, contest):
        self.instance = contest

    def get_ejudge_link(self):
        if not len(self.instance.ejudge_id):
            return ''
        ejudge_id = str(int(self.instance.ejudge_id))

        return "/cgi-bin/new-client?contest_id={}&locale_id=1".format(ejudge_id)

    def is_deployed(self):
        if not len(self.instance.ejudge_id):
            return True

        contest_dir = self.instance.contest_dir
        contest_problems_dir = self.instance.problems_dir
        config_file_path = self.instance.config_path
        description_file_path = self.instance.xml_config
        contest_dir_exist = self.is_dir_exist(contest_dir)
        contest_problems_dir_exist = self.is_dir_exist(contest_problems_dir)
        config_file_path_exist = self.is_file_exist(config_file_path)
        description_file_path_exist = self.is_file_exist(description_file_path)
        return contest_dir_exist and\
               contest_problems_dir_exist and\
               config_file_path_exist and\
               description_file_path_exist


