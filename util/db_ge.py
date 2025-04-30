import mariadb
import sys
import os
from dotenv import load_dotenv
from datetime import datetime

class MariaDB_ge:
    def __init__(self):
        """Load database credentials from .env file"""
        load_dotenv()  # Load environment variables from .env file
        
        self.config = {
            "host": os.getenv("DB_HOST"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "database": os.getenv("DB_NAME"),
            "port": int(os.getenv("DB_PORT", 3306))  # Default port 3306 if not set
        }
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish connection to the database"""
        try:
            self.conn = mariadb.connect(**self.config)
            self.cursor = self.conn.cursor(dictionary=True)
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB: {e}")
            sys.exit(1)

    def close(self):
        """Closes the database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def fetch_one(self, query, params=None):
        """Fetch a single record from a query"""
        self.cursor.execute(query, params or ())
        return self.cursor.fetchone()

    def fetch_all(self, query, params=None):
        self.connect()
        """Fetch all records from a query"""
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

    def execute(self, query, params=None, commit=True):
        self.connect()
        """Execute INSERT, UPDATE, DELETE queries"""
        try:
            self.cursor.execute(query, params or ())
            if commit:
                self.conn.commit()
            return self.cursor.rowcount  # Number of affected rows
        except mariadb.Error as e:
            print(f"Error executing query: {e}")
            return None


    def __enter__(self):
        """Enables use of 'with' statement"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Closes connection when leaving 'with' block"""
        self.close()


    def buy_offer(self, osrs_user, item, price, quantity):
        now = datetime.now()
        query = f'''
        INSERT INTO
        ge_offers
        (osrs_user, offer, item, quantity, state, bid, time_orginal_bid, time_update_bid)
        VALUES
        ('{osrs_user}', 'BUY', '{item}', {quantity}, 'waiting', {price}, '{now}', '{now}')
        '''
        self.execute(query)

    def sell_offer(self, osrs_user, item, price, quantity):
        now = datetime.now()
        query = f'''
        INSERT INTO
        ge_offers
        (osrs_user, offer, item, quantity, state, bid, time_orginal_bid, time_update_bid)
        VALUES
        ('{osrs_user}', 'SELL', '{item}', {quantity}, 'waiting', {price}, '{now}', '{now}')
        '''
        self.execute(query)

    def existing_offer(self, osrs_user):
        query = '''
        SELECT
        osrs_user
        FROM ge_offers
        '''
        if len(self.fetch_all(query)) > 0:
            return True
        else:
            return False


    def get_pending_jobs(self):
        query = '''
        SELECT 
        accounts.ip, 
        job_types.command,
        queue.job_id
        FROM queue
        JOIN accounts ON queue.account_id = accounts.account_id
        JOIN job_types ON queue.job_type_id = job_types.type_id
        WHERE queue.state = 'pending';
        '''
        return self.fetch_all(query)
    
    def get_all_job_types(self):
        query = '''
        SELECT 
        *
        FROM job_types
        WHERE state = 'PROD';
        '''
        return self.fetch_all(query)
    
    def get_skill_job_types(self):
        query = '''
        SELECT 
        *
        FROM job_types
        WHERE purpose = 'skill' AND state = 'PROD';
        '''
        return self.fetch_all(query)

    def get_user(self, user):
        query = f'''
        SELECT 
        *
        FROM users
        WHERE os_user = '{user}'
        AND (account_status = 'ready' or account_status = 'trial');
        '''
        return self.fetch_all(query)

    def get_user_status_working(self, host):
        query = f'''
        SELECT 
        *
        FROM users
        WHERE host = '{host}' 
        AND (account_status = 'ready' OR account_status = 'trial')
        AND status = 'working';
        '''
        return self.fetch_all(query)

    def get_user_status_stopped(self, host, amount):
        now = datetime.now()
        query = f'''
        SELECT 
        *
        FROM users
        WHERE host = '{host}' 
        AND (account_status = 'ready' OR account_status = 'trial')
        AND status = 'stopped' 
        AND played_today < playtime 
        AND (last_played IS NULL OR last_played < DATE_SUB('{now}', INTERVAL 15 MINUTE))
        LIMIT {amount};
        '''
        return self.fetch_all(query)
    
    def reset_playtime(self, date):
        query = f'''
        UPDATE users
        SET played_today = 0, last_reset = '{date}'
        WHERE last_reset < '{date}';
        '''
        self.execute(query)
    
    def set_user_status(self, user, status):
        query = f'''
        UPDATE users
        SET status = '{status}'
        WHERE osrs_user = '{user}' AND (account_status = 'ready' OR account_status = 'trial');
        '''
        self.execute(query)

    def set_account_status(self, user, status):
        query = f'''
        UPDATE users
        SET account_status = '{status}'
        WHERE osrs_user = '{user}';
        '''
        self.execute(query)

    def upgrade_accounts_to_ready(self):
        query = f'''
        UPDATE users
        SET account_status = 'ready'
        WHERE total_playtime > 72000 AND account_status = 'trial';
        '''
        self.execute(query)

    def upgrade_accounts_to_trial(self):
        query = f'''
        UPDATE users
        SET account_status = 'trial'
        WHERE account_status = 'soon'
        AND last_reset >= DATE_ADD(creation_date, INTERVAL 3 DAY);
        '''
        self.execute(query)

    def reset_user(self, user):
        query = f'''
        UPDATE users
        SET status = 'stopped', played_today = 0, last_played = NULL
        WHERE os_user = '{user}';
        '''
        self.execute(query)
    
    def update_time_played_today(self, user, duration, total_duration):
        now = datetime.now()
        query = f'''
        UPDATE users
        SET played_today = '{duration}', total_playtime = '{total_duration}', last_played = '{now}'
        WHERE osrs_user = '{user}';
        '''
        self.execute(query)
    
    def update_playtime(self, seconds, osrs_user):
        query = f'''
        UPDATE users
        SET playtime = '{seconds}'
        WHERE osrs_user = '{osrs_user}';
        '''
        self.execute(query)
    
    def update_exp(self, osrs_user, total, earned):
        query = f'''
        UPDATE users
        SET exp_total = '{total}', exp_latest = '{earned}'
        WHERE osrs_user = '{osrs_user}';
        '''
        self.execute(query)
    
    
  

if __name__ == "__main__":
    with MariaDB_ge() as db:
        result = db.fetch_all("SELECT * FROM accounts")
        print(result)