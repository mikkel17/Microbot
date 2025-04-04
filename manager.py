from util.db import MariaDB
from util.logger import SimpleLogger
import time
import subprocess
from datetime import datetime


class manager():
    def __init__(self):
        self.db = MariaDB()
        self.logger = SimpleLogger()


    def start_new_jvm(self, user):
        self.logger.info('Manager', f'Starting new JVM. [\'/bin/sh\', \'start_jvm.sh\', \'{user}\']')
        subprocess.Popen(['/bin/sh', 'start_jvm.sh', f'{user}'])
        print(['/bin/sh', 'start_jvm.sh', f'{user}'])

    def main_loop(self):
        self.logger.info('Manager', f'Starting main_loop')
        prev_users = ''
        while True:
            users = self.db.get_user_status_stopped()
            if users != prev_users:
                self.logger.info('Manager', f'Users status=stopped: {users}')
            
            for user in users:
                self.start_new_jvm(user['os_user'])
                print(f'{datetime.now()} start_new_jvm({user['os_user']})')
            time.sleep(300)

            prev_users = users


if __name__ == "__main__":
    man = manager()
    man.main_loop()