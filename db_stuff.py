import sqlite3 as db
import os
import re





class DataBase_Client():
    
    def __init__(self):
        pass
    

    def check_user_exists(self, client):
        try:
            conn = db.connect('db_test.db')
            cur = conn.cursor()
            cur.execute( """SELECT full_name FROM client WHERE full_name = ?""", client)
           
            row = cur.fetchall()
            return row
        except db.Error as er:
            msg = {'op': 'insert', 'status': 'unsuccessful'}
            print('SQLite error: %s' % (' '.join(er.args)))
        finally:
             conn.close()



    def update_client(self, records):
        try:
            conn = db.connect('db_test.db')
            cur = conn.cursor()
            cur.execute( """UPDATE client SET full_name = ?, first_phone = ?, second_phone = ?, address = ? WHERE id = ?""", records)
            conn.commit()
            row = cur.fetchall()
            return row
        except db.Error as er:
            msg = {'op': 'insert', 'status': 'unsuccessful'}
            print('SQLite error: %s' % (' '.join(er.args)))
        finally:
             conn.close()



    def update_display(self, cliend_id):
        try:
            conn = db.connect('db_test.db')
            cur = conn.cursor()
            cur.execute( """SELECT id, full_name, first_phone,second_phone, address FROM client WHERE id = ?""", cliend_id)
            row = cur.fetchall()
            return row
        except db.Error as er:
            msg = {'op': 'insert', 'status': 'unsuccessful'}
            print('SQLite error: %s' % (' '.join(er.args)))
        finally:
             conn.close()



    def insert_user(self, record):
        conn = db.connect("db_test.db")
        cursor = conn.cursor()
        sql = """INSERT INTO client VALUES (?,?,?,?,?,?,?)"""
        cursor.execute(sql, record)
        conn.commit()
        cursor.close()
        conn.close()
   

    def get_user_id(self, full_name):
        conn = db.connect('db_test.db')
        cursor = conn.cursor()
        
        cursor.execute(f"""SELECT id FROM client WHERE full_name = '{full_name}'""")
        row = cursor.fetchone()
        return row
    


    def get_full_name(self, full_name):
        try:
            conn = db.connect('db_test.db')
            cur = conn.cursor()

            cur.execute(f"""SELECT id, client.full_name
            FROM client WHERE client.full_name = '{full_name}'""")

            row = cur.fetchall()
            return row
        except db.Error as er:
            msg = {'op': 'insert', 'status': 'unsuccessful'}
            print('SQLite error: %s' % (' '.join(er.args)))
        finally:
             conn.close()


    def display_table(self, full_name):
        try:
            conn = db.connect('db_test.db')
            cur = conn.cursor()

            cur.execute(f"""SELECT client.full_name, client.age, results.file_name
            FROM client
            INNER JOIN results ON client.id = results.client_id
            WHERE client.full_name = '{full_name}'""")

            all_rows = cur.fetchall()
            return all_rows
        except db.Error as er:
            msg = {'op': 'insert', 'status': 'unsuccessful'}
            print('SQLite error: %s' % (' '.join(er.args)))
        finally:
             conn.close()


    def get_client_id(self, full_name):
        try:
            conn = db.connect('db_test.db')
            cur = conn.cursor()

            cur.execute(f"""SELECT client.id
            FROM client
            INNER JOIN results ON client.id = results.client_id
            WHERE client.full_name = '{full_name}'""")

            all_rows = cur.fetchone()
            return all_rows
        except db.Error as er:
            msg = {'op': 'insert', 'status': 'unsuccessful'}
            print('SQLite error: %s' % (' '.join(er.args)))
        finally:
             conn.close()


  
    def get_tables(self):
        conn = db.connect('db_test.db')
        cur = conn.cursor()
        try:
            cur.execute("""SELECT client.id, phone.phone_id, address.address_id, results.client_id
            FROM client, phone, address, results""")
            all_rows = cur.fetchall()
            
            return all_rows
        except db.Error as er:
            print('SQLite eror: %s' % (' '.join(er.args)))
        finally:
            conn.close()


    def delete_from_client(self, client_id):

        conn = db.connect('db_test.db')
        cur = conn.cursor()
        sql = """DELETE FROM client WHERE id = ?"""

        cur.execute(sql, client_id)
        conn.commit()


    def delete_from_results(self, client_id):
        conn = db.connect('db_test.db')
        cur = conn.cursor()
        sql = """DELETE FROM results WHERE client_id = ?"""
        cur.execute(sql, client_id)
        conn.commit()

        conn.close()

# =============Admin Dababase============================
    def _get_user_credentials(self):
        conn = db.connect('db_test.db')
        cur = conn.cursor()
        try:
            in_sql = """SELECT name, password FROM admin"""
            cur.execute(in_sql)
            conn.commit()
            row = cur.fetchall()
            
            return row
        except db.Error as er:
            print('SQLite eror: %s' % (' '.join(er.args)))
        finally:
            conn.close()

    
    def check_user_credentials(self, get_name, get_pw):
        credentials = self._get_user_credentials()
        for i in credentials:
            name, pw = i
            if name == get_name and pw == get_pw:
                return True
            else:
                return False

    def get_id_from_db(self, id):

        try:
            conn = db.connect('db_test.db')
            cur = conn.cursor()
            sql = """SELECT id FROM client WHERE id = ?"""
            cur.execute(sql, id)

            row = cur.fetchone()
           
            if row:
                return True
            
            else:
                return False
            
            
        except db.Error as er:
            msg = {'op': 'insert', 'status': 'unsuccessful'}
            print('SQLite error: %s' % (' '.join(er.args)))
        finally:
             conn.close()
            



class File_Master:
    def __init__(self):
        self.file_name = []

    
    def load_directory(self, path="E:\E_Documents\Documents\Project Carlos\media"):
        
        for x in os.listdir(path):
            self.file_name.append(x)

        return self.file_name
    


    def get_file(self, file, c_id):

        for x in self.load_directory():
            # print(x + 'this is x in the for')
            # id = obj.get_user_id(full_name)
            if file in x:
                with open(f"E:\E_Documents\Documents\Project Carlos\media\{x}", "rb") as f:
                    
                    data = f.read()
                    self.insert_file(file_name=x, file_data=data, client_id=c_id)
                    print("{} Added to data base".format(x))
            
                    return x

    def insert_file(self, file_name, file_data, client_id):
        
        conn = db.connect("db_test.db")
        cursor = conn.cursor()

        cursor.execute(f""" INSERT INTO results 
        (file_name, file_data, client_id) VALUES (?,?,?)""", ( file_name, file_data, client_id))

        conn.commit()
        cursor.close()
        conn.close()


    def read_file(self, file):
        for x in self.load_directory():

            if file in x:
                with open(x, 'rb') as f:
                    data = f.read()
                    self.insert_file(name=x, file=data)
        pass


class Clean_Format:

    def __init__(self):
        pass

    def phone_format(self, phone):
        first_trhee = phone[:3]
        last_numbers = phone[3:]
        full_number = f"{first_trhee}-{last_numbers}"
        return full_number




# def main():
#     obj = DataBase_Client()
#     os.chdir('E:\E_Documents\Documents\Project Carlos')

#     for x in obj.load_directory():
#         # print(x + 'this is x in the for')
#         if ".csv" in x:
#             # print(x)
#             with open(x, "rb") as f:
#                 data = f.read()
#                 obj.insert_file(name=x, file=data)
#                 print("{} Added to data base".format(x))

# This program uses the programmer-defined Rectangle class.

# Do NOT modify this program. Write your code in Rectangle.py,
# # then select this file and click "Run Code".


# name = 'felipe'
# pas = 'felipe35_lab'

# pas = pas.encode('utf-8')
# pas = hashlib.sha1(pas).hexdigest() 

# print(pas)
# admin = ['felipe', '60f73abe0d52e5f9faed0119415549df0055b26e']
# obj = DataBase_Client()
# check = obj.check_user_credentials()
