from util.db import MariaDB
import sys
# input is os_user
user = sys.argv[1]

db = MariaDB()

db.reset_user(user)
db.get_user(user)