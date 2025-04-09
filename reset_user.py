from util.db import MariaDB
import sys

user = sys.argv[1]

db = MariaDB()

db.reset_user(user)
db.get_user(user)