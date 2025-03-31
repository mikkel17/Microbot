import mariadb
import sys
import os
from dotenv import load_dotenv

class MariaDB:
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
        FROM job_types;
        '''
        return self.fetch_all(query)
    
    def get_skill_job_types(self):
        query = '''
        SELECT 
        *
        FROM job_types
        WHERE purpose = 'skill';
        '''
        return self.fetch_all(query)
    
    def job_started(self, job_id):
        query = f'''
        UPDATE queue
        SET state = 'started'
        WHERE job_id = {job_id};
        '''
        self.execute(query)
        return
       

if __name__ == "__main__":
    with MariaDB() as db:
        result = db.fetch_all("SELECT * FROM accounts")
        print(result)