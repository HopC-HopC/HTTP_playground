import sqlite3


class DBManager:
    uri = str

    def __init__(self, uri: str):
        """
        :param uri: define database path
        """
        self.uri = uri

    def connect(self):
        """
        :return: returns connection object
        """
        connection = None
        try:
            connection = sqlite3.connect(self.uri)
        except sqlite3.Error as e:
            print(e)
        return connection

    def create_tables(self, models: dict):
        """
        :param models: include dict of models for which to create tables.
                        {'model name': model}
        """
        for model, attributes_raw in models.items():
            attributes_raw = [s for s in dir(attributes_raw) if '_' not in s and s.islower()]
            connection = self.connect()
            table = f''' CREATE TABLE IF NOT EXISTS {model} ( id INTEGER PRIMARY KEY AUTOINCREMENT, '''
            for attribute in attributes_raw:
                if attribute == 'age' or 'int' in attribute:
                    table += f'{attribute} INTEGER NOT NULL, '
                elif attribute == 'id':
                    continue
                else:
                    table += f'{attribute} CHAR(255) NOT NULL, '
            table = table[:-2] + '); '
            print(table)
            cursor = connection.cursor()
            cursor.execute(table)
            connection.close()

    def save_person(self, person: object):
        """

        :param person: pass the person object that you want to save or update
        :return: returns updated person object via DBManager.get_by_id()
        """
        connection = self.connect()
        cursor = connection.cursor()
        if person.id == 0:
            cursor.execute(f'''  INSERT INTO Person ('name', 'age', 'role')
                                VALUES ('{person.name}', '{person.age}', '{person.role}') ''')
            id_ = cursor.execute(f''' SELECT max(id) FROM Person ''').fetchone()
            print(id_)
            person.id = int(id_[0])
        else:
            cursor.execute(f''' UPDATE Person SET name = '{person.name}', age = {person.age}, role = '{person.role}' 
                                WHERE id = {person.id}    ''')
        connection.commit()
        connection.close()
        return self.get_by_id(person.id)

    def get_by_id(self, id_: int):
        """

        :param id_: pass id of person object you would like to get
        :return: returns person object if found, or empty person object otherwise
        """
        if not str(id_).isdigit():
            return 401, 'id must be integer'
        from web import Person
        connection = self.connect()
        cursor = connection.cursor()
        try:
            entry = cursor.execute(f''' SELECT * FROM Person WHERE id = {id_}   ''').fetchone()
            person = Person(id = entry[0], age = entry[1], name = entry[2], role = entry[3])
        except sqlite3.Error:
            person = Person('Error')
        connection.close()
        return person

    def get_all(self):
        """

        :return: returns all entries of Person objects
        """
        connection = self.connect()
        cursor = connection.cursor()
        entries = cursor.execute(f''' SELECT * FROM Person    ''').fetchall()
        connection.close()
        return entries

    def delete_entry(self, id_: int):
        """

        :param id_: pass id of Person object to delete from database
        :return: return error code if id_ is not integer
        """
        if not str(id_).isdigit():
            return 401, 'id must be integer'
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(f''' DELETE FROM Person WHERE id = {id_}   ''')
        connection.commit()
        connection.close()
