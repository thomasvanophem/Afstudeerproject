"""
Implements a simple database class using a sqlite database.

Author: Thomas van Ophem, thomas.vanophem@student.uva.nl
Date: 26-04-2015
"""
import sqlite3
import sys
import time

import logger

class Database:
    def __init__(self, db_name):
        self.db = self.open_database(db_name)
    
    # Opens a connection to the database with name 
    # <db_name>.
    # Returns a connection object or None.
    def open_database(self, db_name):
        """
        Opens a connection to the database.
        
        db_name:    name of database
        """
        try:
            logger.log("busy", "Connecting to database <" + db_name + ">", time.strftime("%c"))
            conn = sqlite3.connect(db_name)
            conn.enable_load_extension(True)
            conn.load_extension("./libsqlitefunctions.so")
            conn.enable_load_extension(False)
            logger.log("ok", "Connected to database <" + db_name + ">", time.strftime("%c"))
            return conn
        except:
            logger.log("error", str(sys.exc_info()[0]), time.strftime("%c"))
            return None

    def create_table(self, table_name, fields):
        """
        Creates a new table.
        
        table_name:     name of table
        fields:         list [] of fields (names and properties)
        """
        
        # Construct the SQL query.
        sql = "CREATE TABLE " + table_name + " (" 
        
        sql += ", ".join(fields) + ");"
        
        # Run the SQL query.
        try:
            logger.log("busy", "Creating table <" + table_name + ">", time.strftime("%c"))
            self.db.execute(sql)
            logger.log("ok", "Created table <" + table_name + ">", time.strftime("%c"))
        except sqlite3.OperationalError as e:
            logger.log("info", str(e), time.strftime("%c"))
    
    def insert(self, table_name, fields, values):
        """
        Inserts a new record.
        
        table_name:     name of table
        fields:         list [] of fields to insert
        values:         list [] of values
        """     
        
        # Construct the SQL query.
        val = ", ".join(["?"] * len(values))
        data = ", ".join(fields)
        
        sql = "INSERT INTO " + table_name + " (" + data + ") VALUES (" + val + ");"

        # Run the SQL query.
        try:
            logger.log("busy", "Running query :: " + sql, time.strftime("%c"))
            self.db.execute(sql, tuple(values))
            self.db.commit()
            logger.log("ok", "Insert successful", time.strftime("%c"))
        except sqlite3.OperationalError as e:
            logger.log("error", "Insert failed :: " + str(e) + " :: " + sql, time.strftime("%c"))
        except sqlite3.InterfaceError as e:
            logger.log("error", "Insert failed :: " + str(e) + " :: " + sql, time.strftime("%c"))
    def select(self, table_name, fields, where = "", order = "",  ad = "ASC"):
        """
        Selects records from the database.
        
        table_name: name of table
        fields:     list [] of fields to select
        where:      where clause
        order:      order by clause
        ad:         ASC/DESC
        """
        
        # Construct the SQL query.
        data = ", ".join(fields)
        
        rows = []
        
        sql = "SELECT " + data + " fROM " + table_name 
        
        if where != "" and order != "":
            sql += " WHERE " + where + " ORDER BY " + order + " " + ad
        elif where != "" and order == "":
            sql += " WHERE " + where
        elif where == "" and order != "":
            sql += " ORDER BY " + order + " " + ad
            
        sql += ";"
        
        # Run the SQL query.
        try:
            logger.log("busy", "Running query :: " + sql, time.strftime("%c"))
            rows = self.db.execute(sql)
            logger.log("ok", "Selection successful", time.strftime("%c"))
            return rows
        except:
            logger.log("error", "Selection failed :: " + str(sys.exc_info()[0]) + " :: " + sql, time.strftime("%c"))
            return []
    
    def update(self, table_name, fields, values, where):
        """
        Updates a record in the database.
        
        table_name:     name of table
        fields:         list [] of fields which you are going to update
        values:         list [] of values
        where:          where clause 
        """
        
        # Construct the SQL query.
        data = ""
        val = ()
        
        data = " = ?, ".join(fields)
        data += " = ?"
        
        val = tuple(values)
        
        sql = "UPDATE " + table_name + " SET " + data + " WHERE " + where + ";"
        
        # Run the SQL query.
        try:
            logger.log("busy", "Running query :: " + sql, time.strftime("%c"))
            self.db.execute(sql, val)
            self.db.commit()
            logger.log("ok", "Update successful", time.strftime("%c"))
        except:
            logger.log("error", "Update failed :: " + str(sys.exc_info()[0]) + " :: " + sql, time.strftime("%c"))
            
    def delete(self, table_name, where):
        """
        Deletes record from the database.
        
        table_name:     name of table
        where:          where clause
        """
        
        # Construct the SQL query.
        sql = "DELETE FROM " + table_name + " WHERE " + where + ";"
        
        # Run the SQL query.
        try:
            logger.log("busy", "Running query :: " + sql, time.strftime("%c"))
            self.db.execute(sql)
            self.db.commit()
            logger.log("ok", "Record was deleted", time.strftime("%c"))
        except:
            logger.log("error", "Delete failed :: " + str(sys.exc_info()[0]) + " :: " + sql, time.strftime("%c"))
    
    def close(self):
        """
        Closes the database connection.
        """
        
        try:
            logger.log("busy", "Closing connection to database", time.strftime("%c"))
            self.db.close()
            logger.log("ok", "Closed connection to database", time.strftime("%c"))
        except:
            logger.log("error", str(sys.exc_info()[0]), time.strftime("%c"))
        
if __name__ == "__main__":
    test = Database("test.db")
    test.create_table("test", ["ID INTEGER PRIMARY KEY ASC", "NAME TEXT NOT NULL"])
    test.insert("test", ["NAME"], ["Thomassss"])
    #for i in range(0, 200):
    #    test.insert("test", "NAME", (i,))
    rows = test.select("test", ["*"], order="ID", ad="DESC")
    test.update("test", ["NAME"], ["PIET"], "ID = 3")

    test.close()
