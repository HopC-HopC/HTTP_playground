

class Person:
    id = int
    name = str
    age = int
    role = str

    def __init__(self, name='undefined', age=0, role='unemployed', id=0):
        self.name = name
        self.age = age
        self.role = role
        self.id = id

    def update_age(self, age: int):
        """

        :param age: pass age value to update Person object to
        :return: success or failure codes
        """
        if age is None:
            return 401, 'No age passed'
        elif not str(age).isdigit():
            return 401, 'Age must be integer'
        self.age = age
        return 200, 'Age updated'

    def update_role(self, role: str):
        """

        :param role: pass role value to update Person object to
        :return: success or failure codes
        """
        if role is None:
            return 401, 'No role passed'
        self.role = role
        return 200, 'Role updated'

    def __repr__(self):
        """
        :return: description of Person object
        """
        return f'{self.name} is {self.age} years old and is a {self.role}'


# person = Person('Chris',20,'Teacher')

