import MySQLdb

from pyarch.config import GlobalConst


class MySQLDatabase():
    """Manage Access to/from MySQL Database"""
    MYSQLOPS = GlobalConst.MYSQLOPS
    TABLES = []
    
    def __init__(self):
        self.MYSQL_CONNECTION = MySQLdb.connect(self.MYSQLOPS['host'], self.MYSQLOPS['user'], self.MYSQLOPS['pass'], self.MYSQLOPS['db'], use_unicode=True, charset='utf8')
        
        
    def query(self, sql: str ="", multiple: bool = True, write: bool = False) -> dict:
        """ Query the database. """
        
        cursor = self.MYSQL_CONNECTION.cursor()
        result = cursor.execute(sql)
        field_names = [i[0] for i in cursor.description]
        if write:
            self.MYSQL_CONNECTION.commit()
            return cursor.lastrowid
        elif multiple:
            
            return self._to_list(field_names, cursor.fetchall())
        else:
            return self._to_dict(field_names,cursor.fetchone())

    def get_row_by_id(self, table: str, id_: int) -> dict:
        """Retrieve a single row of a table"""
        sql = "Select * from "+ table + " where id=" + str(id_) +";"
        dict_ = self.query(sql,False)
        if self._table_has_i18n(table):
            dict_["i18n"] = self.get_rows_by_key(table+"_i18n", "id", id_)
        return dict_
        
    def get_rows_by_key(self, table: str, key_: str, value_: any) -> list:
        sql = "Select * from " + table + " where " + key_ + "=" + str(value_) + ";"
        return self.query(sql)
    
    def _table_has_i18n(self, table: str) -> bool:
        """Ask if a table with i18n exists"""
        if self.TABLES == []:
            sql= "show tables;"
            self.TABLES = self.query(sql)
        if table + "_i18n" in self.TABLES:
            return True
        else:
            return False
    
    def _to_dict(self, field_names: list, tuple_: tuple) -> dict:
        """Transform the query result from tuple to dict"""
        return {field_names[i]: tuple_[i] for i in range(len(field_names))} 
    
    def _to_list (self, field_names: list, tuples_: tuple) -> list:
        """Transform the query result in list"""
        if len(field_names) == 1:
            return self._to_list_of_values(tuples_)
        else:
            return self._to_list_of_dicts(field_names, tuples_)
    
    def _to_list_of_dicts(self, field_names: list, tuples_: tuple) -> list:
        """ Trasform the multi column query result into list of dict"""
        list_=[]
        for tuple_ in tuples_:
            list_.append(self._to_dict(field_names, tuple_))
        return list_ 
    
    def _to_list_of_values(self, tuples_: tuple) -> list:
        """Transform the one column query result to list"""
        return [tuple_[0] for tuple_ in tuples_]
