from datetime import datetime
from models.db import BulkDatabase

# GERER LES TENTATIVES D'APPELS
class Attempts(BulkDatabase):
    def __init__(self) -> None:
        self.__table="attempts"
        super().__init__()
        
    def add(self, caller:str, receiver:str, status:str) -> None:
        self._get_cursor().execute(f"INSERT INTO {self.__table}(attempt_date, detail_date, caller, called, status) VALUES(?,?,?,?,?)",(datetime.utcnow().strftime("%Y-%m-%d"), datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), caller, receiver, status))
        self._get_connection().commit()
        
    def get_all(self) -> dict|None:
        query = self._get_cursor().execute(f"SELECT * FROM {self.__table}")
        return query.fetchall()

# GERER LE CDR
class Cdr(BulkDatabase):
    def __init__(self) -> None:
        self.__table="cdr"
        super().__init__()
        
    def add(self,caller:str,called:str,start_time:str,answer_time:str,end_time:str,duration:str,billable_sec:str,disposition:str,unique_id:str) -> None:
        self._get_cursor().execute(f"INSERT INTO {self.__table}(caller,called,start_time,answer_time,end_time,duration,billable_sec,disposition,unique_id) VALUES(?,?,?,?,?,?,?,?,?)",(caller,called,start_time,answer_time,end_time,duration,billable_sec,disposition,unique_id))
        self._get_connection().commit()

# GERER LES STATISTIQUES DE L'APPELANT       
class CallerStat(BulkDatabase):
    def __init__(self) -> None:
        self.__table="caller_stats"
        super().__init__()
        
    def add(self, caller:str) -> None:
        self._get_cursor().execute(f"INSERT INTO {self.__table}(caller) VALUES(?)",(caller,))
        self._get_connection().commit()
    
    def get_all(self) -> dict|None:
        query = self._get_cursor().execute(f"SELECT * FROM {self.__table}")
        return query.fetchall()
    
    def exist(self, caller:str):
        query = self._get_cursor().execute(f"SELECT caller FROM {self.__table} WHERE caller=?",(caller,))
        return query.fetchone()
    
    def answered(self, caller:str):
        self._get_cursor().execute(f"UPDATE {self.__table} SET days_call_answered = days_call_answered + 1 WHERE caller=?",(caller,))
        self._get_connection().commit()
        self.__update_score(caller)
        
    def unanswered(self, caller:str):
        self._get_cursor().execute(f"UPDATE {self.__table} SET days_call_unanswered = days_call_unanswered + 1 WHERE caller=?",(caller,))
        self._get_connection().commit()
        self.__update_score(caller)
    
    def __update_score(self, caller):
        self._get_cursor().execute(f"UPDATE {self.__table} SET score = days_call_answered - days_call_unanswered WHERE caller=?",(caller,))
        self._get_connection().commit()
        
# GERER LES STATISTIQUES DE L'APPELÉ      
class CalledStat(BulkDatabase):
    def __init__(self) -> None:
        self.__table="called_stats"
        super().__init__()
        
    def add(self,called:str,is_whatsapp:int) -> None:
        self._get_cursor().execute(f"INSERT INTO {self.__table}(called,is_whatsapp) VALUES(?,?)",(called,is_whatsapp))
        self._get_connection().commit()
        
    def get_all(self) -> dict|None:
        query = self._get_cursor().execute(f"SELECT * FROM {self.__table}")
        return query.fetchall()
    
    def exist(self, called:str):
        query = self._get_cursor().execute(f"SELECT called FROM {self.__table} WHERE called=?",(called,))
        return query.fetchone()

    def answered(self, called:str):
        self._get_cursor().execute(f"UPDATE {self.__table} SET days_call_answered = days_call_answered + 1 WHERE called=?",(called,))
        self._get_connection().commit()
        self.__update_score(called)
        
    def unanswered(self, called:str):
        self._get_cursor().execute(f"UPDATE {self.__table} SET days_call_unanswered = days_call_unanswered + 1 WHERE called=?",(called,))
        self._get_connection().commit()
        self.__update_score(called)
    
    def __update_score(self, called):
        self._get_cursor().execute(f"UPDATE {self.__table} SET score = days_call_answered - days_call_unanswered WHERE called=?",(called,))
        self._get_connection().commit()

# GERER LA LIAISON APPELANT-APPELÉ       
class UniqueLink(BulkDatabase):
    def __init__(self) -> None:
        self.__table="unique_link"
        super().__init__()
        
    def add(self,caller:str,called:str) -> None:
        self._get_cursor().execute(f"INSERT INTO {self.__table}(caller,called) VALUES(?,?)",(caller,called))
        self._get_connection().commit()
        
    def get_all(self) -> dict|None:
        query = self._get_cursor().execute(f"SELECT * FROM {self.__table}")
        return query.fetchall()