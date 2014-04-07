from abc import *
import sqlite3

from ...MDL.nodes import *

class QueryDatabase(object):

    def __init__(self, system, file=":memory:", table_handlers=[]):
        self._system = system
        self._file=file
        self._conn = None
        self._table_handlers = table_handlers

    @property
    def connection(self):
        return self._conn

    def start(self):
        """open databse connection"""
        
        self._conn = sqlite3.connect(self._file, check_same_thread=False)
        
            
    def index(self):
        """Reindex plugins from system"""
        if self._conn == None:
            raise RuntimeError("Databse not Open. Call start first")

        for table in self._table_handlers:
            table.drop(self._conn)
            table.create(self._conn)
            table.populate(self._conn, self._system)
            self._conn.commit()


    def shutdown(self):
        """Close Database Connection"""
        if not self._conn is None:
            self._conn.close()


class ITableHandler(metaclass=ABCMeta):
    """Base Class for a Table to hold data about madz"""
    
    @property
    @abstractmethod
    def create_query(self):
        pass
    
    @property
    @abstractmethod
    def drop_query(self):
        pass

    def populate(self, connection, system):
        """Fill this table with madz data"""

    def create(self, connection):
        connection.execute(self.create_query)

    def drop(self, connection):
        try:
            connection.execute(self.drop_query)
        except:
            return

class ITableQueryHandler(metaclass=ABCMeta):
    """Base Class for Queries"""

    @abstractmethod
    def query(self, connection, query_type, **kwags):
        """Perform Query
        
        query_type : string one of none, likeleft likeright likeboth
        """
        pass


class MdlTypeTable(ITableHandler):
    
    @property
    def create_query(self):
        return \
"""
CREATE TABLE TypeTable(
    namespace TEXT,
    name TEXT,
    signature TEXT,
    doc TEXT
)
"""
    
    @property
    def drop_query(self):
        return "DROP TABLE TypeTable"

    def populate(self, connection, system):
        """Fill this table with madz data"""
        plugins = list(system.all_plugins())
        for plugin in plugins:
            for declaration in plugin.description.declarations():
                doc_attr = declaration.get_attribute(DocumentationAttribute)
                
                connection.execute("INSERT INTO TypeTable VALUES(?, ?, ?, ?)", (
                    plugin.id.namespace,
                    declaration.name,
                    "", # TODO find a a way to generate MDL from Parse tree
                    str(None if doc_attr is None else doc_attr.documentation)))


class MdlVarTable(ITableHandler):
    
    @property
    def create_query(self):
        return \
"""
CREATE TABLE VarTable(
    namespace TEXT,
    name TEXT,
    signature TEXT,
    doc TEXT
)
"""
    
    @property
    def drop_query(self):
        return "DROP TABLE VarTable"

    def populate(self, connection, system):
        """Fill this table with madz data"""
        plugins = list(system.all_plugins())
        for plugin in plugins:
            for definition in plugin.description.definitions():
                doc_attr = definition.get_attribute(DocumentationAttribute)
                
                connection.execute("INSERT INTO VarTable VALUES(?, ?, ?, ?)", (
                    plugin.id.namespace,
                    definition.name,
                    "", # TODO find a a way to generate MDL from Parse tree
                    str(None if doc_attr is None else doc_attr.documentation)))


class MdlTypeTableQueryManager(ITableQueryHandler):

    def query(self, connection, query_type="none", **kwags):
        """Return list of tuples matching query

        kwargs:{
           namespace : plugin name,
           name : variable name,
           signature : variable type,
           doc : variable documentation, 
        }
        """
        op={
            "none" : "=",
            "likeleft" : "LIKE",
            "likeright" : "LIKE",
            "likeboth" : "LIKE",
        }

        def like_val(val):
            if query_type ==  "none":
                return val
            if query_type == "likeleft":
                return "%{}".format(val)
            if query_type == "likeright":
                return "{}%".format(val)
            if query_type == "likeboth":
                return "%{}%".format(val)

        if len(kwags) == 0:
            q = "SELECT * from TypeTable"
        else:
            q = "SELECT * FROM TypeTable where {}".format(
                " and ".join(
                    ["{} {} {}".format(key, op[query_type], like_val(val)) for key, val in kwargs]))

        cur = connection.cursor()
        cur.execute(q)
        
        return cur.fetchall()


class MdlVarTableQueryManager(ITableQueryHandler):

    def query(self, connection, query_type="none", **kwags):
        """Return list of tuples matching query

        kwargs:{
           namespace : plugin name,
           name : variable name,
           signature : variable type,
           doc : variable documentation, 
        }
        """
        op={
            "none" : "=",
            "likeleft" : "LIKE",
            "likeright" : "LIKE",
            "likeboth" : "LIKE",
        }

        def like_val(val):
            if query_type ==  "none":
                return val
            if query_type == "likeleft":
                return "%{}".format(val)
            if query_type == "likeright":
                return "{}%".format(val)
            if query_type == "likeboth":
                return "%{}%".format(val)
        if len(kwags) == 0:
            q = "SELECT * FROM VarTable"
        else:
            q = "SELECT * FROM VarTable where {}".format(
                " and ".join(
                    ["{} {} {}".format(key, op[query_type], like_val(val)) for key, val in kwargs]))

        cur = connection.cursor()
        cur.execute(q)
        
        return cur.fetchall()