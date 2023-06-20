from datetime import datetime
from models.db import Database

# GERER LES TENTATIVES D'APPELS
class Attempts(Database):
    def __init__(self) -> None:
        super().__init__()
        
    def add(self, caller:str, receiver:str, status:str) -> None:
        self._get_cursor().execute("INSERT INTO attempts(attempt_date, detail_date, caller, called, status) VALUES(?,?,?,?,?)",(datetime.utcnow().strftime("%Y-%m-%d"), datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), caller, receiver, status))
        self._get_connection().commit()
        
    def get_all(self) -> dict|None:
        query = self._get_cursor().execute("SELECT * FROM attempts")
        return query.fetchall()

# GERER LE CDR
class Cdr(Database):
    def __init__(self) -> None:
        super().__init__()
        
    def add(self,caller:str,called:str,start_time:str,answer_time:str,end_time:str,duration:str,billable_sec:str,disposition:str,unique_id:str) -> None:
        self._get_cursor().execute("INSERT INTO cdr(caller,called,start_time,answer_time,end_time,duration,billable_sec,disposition,unique_id) VALUES(?,?,?,?,?,?,?,?,?)",(caller,called,start_time,answer_time,end_time,duration,billable_sec,disposition,unique_id))
        self._get_connection().commit()

# GERER LES STATISTIQUES DE L'APPELANT       
class CallerStat(Database):
    def __init__(self) -> None:
        super().__init__()
        
    def add(self, caller:str) -> None:
        self._get_cursor().execute("INSERT INTO caller_stats(caller) VALUES(?)",(caller,))
        self._get_connection().commit()
    
    def get_all(self) -> dict|None:
        query = self._get_cursor().execute("SELECT * FROM caller_stats")
        return query.fetchall()

# GERER LES STATISTIQUES DE L'APPELÉ      
class CalledStat(Database):
    def __init__(self) -> None:
        super().__init__()
        
    def add(self,called:str,is_whatsapp:bool) -> None:
        self._get_cursor().execute("INSERT INTO called_stats(called,is_whatsapp) VALUES(?,?)",(called,is_whatsapp))
        self._get_connection().commit()
        
    def get_all(self) -> dict|None:
        query = self._get_cursor().execute("SELECT * FROM called_stats")
        return query.fetchall()

# GERER LA LIAISON APPELANT-APPELÉ       
class UniqueLink(Database):
    def __init__(self) -> None:
        super().__init__()
        
    def add(self,caller:str,called:str) -> None:
        self._get_cursor().execute("INSERT INTO unique_link(caller,called) VALUES(?,?)",(caller,called))
        self._get_connection().commit()
        
    def get_all(self) -> dict|None:
        query = self._get_cursor().execute("SELECT * FROM unique_link")
        return query.fetchall()