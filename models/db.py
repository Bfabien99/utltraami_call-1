import sqlite3

class Database:
    def __init__(self):
        self.__con = sqlite3.connect("call.db")
        self.__con.row_factory = sqlite3.Row   #   add this row
        self.__cursor = self.__con.cursor()
        
        # CREATION DE TOUTE LES TABLES
        self.__create_table_attempts()
        self.__create_table_cdr()
        self.__create_table_caller_stat()
        self.__create_table_called_stat()
        self.__create_table_unique_link()
    
    # LA TABLE POUR SAUVEGARDER TOUTE TENTATIVE D'APPEL
    def __create_table_attempts(self):
        self.__cursor.execute("CREATE TABLE IF NOT EXISTS attempts(id INTEGER PRIMARY KEY, attempt_date TEXT, detail_date TEXT, caller TEXT NOT NULL, called TEXT NOT NULL, status TEXT NOT NULL)")
    
    # LA TABLE POUR SAUVEGARDER LE CDR(CALL DETAIL RECORDING)
    def __create_table_cdr(self):
        self.__cursor.execute("CREATE TABLE IF NOT EXISTS cdr(id INTEGER PRIMARY KEY, caller TEXT NOT NULL, called TEXT NOT NULL, start_time TEXT, answer_time TEXT, end_time TEXT, duration TEXT, billable_sec TEXT, disposition TEXT, unique_id TEXT)")
    
    # LA TABLE POUR SAUVEGARDER LES STATISTIQUES DE L'APPELANT
    def __create_table_caller_stat(self):
        self.__cursor.execute("CREATE TABLE IF NOT EXISTS caller_stats(id INTEGER PRIMARY KEY, caller TEXT UNIQUE NOT NULL, days_call_answered INTEGER DEFAULT 0, days_call_unanswered INTEGER DEFAULT 0, Acd TEXT DEFAULT '', score REAL DEFAULT 0.0)")
    
    # LA TABLE POUR SAUVEGARDER LES STATISTIQUES DE L'APPELÉ
    def __create_table_called_stat(self):
        self.__cursor.execute("CREATE TABLE IF NOT EXISTS called_stats(id INTEGER PRIMARY KEY, called TEXT UNIQUE NOT NULL, is_whatsapp INTEGER, days_call_answered INTEGER DEFAULT 0, days_call_unanswered INTEGER DEFAULT 0, Acd TEXT DEFAULT '', score REAL DEFAULT 0.0)")
    
    # LA TABLE POUR RELIER UN APPELANT À UN APPELER
    def __create_table_unique_link(self):
         self.__cursor.execute("CREATE TABLE IF NOT EXISTS unique_link(id INTEGER PRIMARY KEY, caller TEXT NOT NULL, called TEXT NOT NULL)")
         
    def _get_cursor(self):
        return self.__cursor
    
    def _get_connection(self):
        return self.__con