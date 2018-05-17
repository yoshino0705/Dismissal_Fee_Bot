import psycopg2

db_conn = psycopg2.connect(os.environ['DATABASE_URL'])
cur = db_conn.cursor()

class Access_Info(object):
    def __init__(self, identifier):
        self._identifier = str(identifier)
        self._insert_query = '''
        INSERT INTO "Info"(room_id, tele_plan_id, detailed_plan_id, start_date, end_date, status, keywords)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''      
        self._delete_query = '''DELETE FROM "Info" WHERE room_id = %s'''
        
        self._update_row_values()        
        self._update_identifier_list()

        self._tele_plan_id_pos = 2
        self._detailed_plan_id_pos = 3
        self._start_date_pos = 4
        self._end_date_pos = 5
        self._status_pos = 6
        self._keywords_pos = 7
        
    def _update_row_values(self):
        cur.execute('''SELECT * FROM "Info" WHERE room_id = %s''', (self._identifier,))
        self._values = cur.fetchall()
    
    def _update_identifier_list(self):
        cur.execute('''SELECT room_id FROM "Info"''')
        self._existing_identifier_list = cur.fetchall()
        self._existing_identifier_list = list(t[0] for t in self._existing_identifier_list)
        
    def delete(self):
        if self._values:
            cur.execute(self._delete_query, (self._identifier,))
            db_conn.commit()
            self._update_row_values()        
            self._update_identifier_list()
            print("delete success")
            
    def create_info(self):
        if self._identifier not in self._existing_identifier_list:
            try:
                cur.execute(self._insert_query, (self._identifier, -1, -1, "", "", 0, ""))
                db_conn.commit()
                self._update_row_values()
                self._update_identifier_list()
            except:
                db_conn.rollback()
        else:
            print("identifier already exists")
            
    def get_tele_plan_id(self):
        if self._values:
            return self._values[0][self._tele_plan_id_pos]
        else:
            return -1
        
    def set_tele_plan_id(self, tpi):
        if self._values:
            cur.execute('''UPDATE "Info" SET "tele_plan_id" = %s WHERE room_id = %s''', (tpi, self._identifier, ))
            db_conn.commit()
            self._update_row_values()
            
    def get_detailed_plan_id(self):
        if self._values:
            return self._values[0][self._detailed_plan_id_pos]
        else:
            return -1
        
    def set_detailed_plan_id(self, dpi):
        if self._values:
            cur.execute('''UPDATE "Info" SET "detailed_plan_id" = %s WHERE room_id = %s''', (dpi, self._identifier, ))
            db_conn.commit()
            self._update_row_values()
            
    def get_start_date(self):
        if self._values:
            return self._values[0][self._start_date_pos]
        else:
            return -1
        
    def set_start_date(self, sd):
        if self._values:
            cur.execute('''UPDATE "Info" SET "start_date" = %s WHERE room_id = %s''', (sd, self._identifier, ))
            db_conn.commit()
            self._update_row_values()
    
    def get_end_date(self):
        if self._values:
            return self._values[0][self._end_date_pos]
        else:
            return -1
        
    def set_end_date(self, ed):
        if self._values:
            cur.execute('''UPDATE "Info" SET "end_date" = %s WHERE room_id = %s''', (ed, self._identifier, ))
            db_conn.commit()
            self._update_row_values()
            
    def get_status(self):
        if self._values:
            return self._values[0][self._status_pos]
        else:
            return -1
        
    def set_status(self, status):
        if self._values:
            cur.execute('''UPDATE "Info" SET "status" = %s WHERE room_id = %s''', (status, self._identifier, ))
            db_conn.commit()
            self._update_row_values()
            
    def get_keywords(self):
        if self._values:
            return self._values[0][self._keywords_pos]
        else:
            return ""
        
    def set_keywords(self, keywords):
        if self._values:
            cur.execute('''UPDATE "Info" SET "keywords" = %s WHERE room_id = %s''', (keywords, self._identifier, ))
            db_conn.commit()
            self._update_row_values()
    def get_values(self):
        return self._values
