from django.conf import settings
import psutil
import subprocess


class EjudgeSystemControl(object):
    """ Класс для управления системой Ejudge через консоль """

    def start_system(self):
        subprocess.call(str(settings.EJUDGE_CONTROL_SCRIPT_PATH) + ' start', shell=True)
        return self

    def reload_system(self):
        self.stop_system().start_system()
        return self

    def stop_system(self):
        subprocess.call(str(settings.EJUDGE_CONTROL_SCRIPT_PATH) + ' stop', shell=True)
        return self

    def get_system_processes_status(self):
        required_processes = settings.EJUDGE_SYSTEM_REQUIRED_PROCESSES
        result_list = list()
        for process in required_processes:
            proc_name, proc_description = process
            result_list.append({
                'name': str(proc_name),
                'description': str(proc_description),
                'status': self.check_if_process_is_running(proc_name)
            })
        return result_list

    def check_if_process_is_running(self, process_name):
        for proc in psutil.process_iter():
            try:
                # Check if process name contains the given name string.
                if process_name.lower() in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False