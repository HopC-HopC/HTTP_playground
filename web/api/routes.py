from flask import Blueprint, render_template, url_for, make_response, jsonify, request, abort


api = Blueprint('api', __name__)


@api.get('/get/<id_>')
def get_by_id(id_):
    """

    :param id_: retrieve ID from URL; must be int
    :return: __repr__ of Person object
    """
    from web import DB_URI
    from ..DBManager import DBManager
    db = DBManager(DB_URI)
    if not str(id_).isdigit():
        """
        id_ taken from parameters will be a string; id_ passed to the function may
        be an int. Performing str.isdigit() to cover either case.
        """
        abort(406, 'ID must be integer')

    id_ = int(id_)
    person = db.get_by_id(id_)
    if not person.id == id_:
        print(str(person))
        abort(404, 'ID not found')

    response = make_response(
        jsonify(
            {'body': str(person)}
        ),
        200,
    )
    response.headers["Content-Type"] = "application/json"
    return response


@api.get('/get_all')
def get_all():
    """

    :return: __repr__ of all stored Person objects
    """
    from web import DB_URI
    from ..DBManager import DBManager
    db = DBManager(DB_URI)
    all_entries = db.get_all()
    people = {}
    from ..models import Person
    for entry in all_entries:
        if len(entry) == 4:
            person = Person(id_=entry[0], age=entry[1], name=entry[2], role=entry[3])
            people[person.id] = str(person)
    response = make_response(
        jsonify(
            people
        ),
        200,
    )
    response.headers["Content-Type"] = "application/json"
    return response


@api.get('/generate')
def generate():
    """
    Populates database with Person objects
    :return: status OK
    """
    from web import DB_URI
    from ..DBManager import DBManager
    db = DBManager(DB_URI)
    from ..models import Person
    person1 = Person('Jeff', 22, 'Unknown')
    db.save_person(person1)
    return 200, 'OK'


@api.patch('/update_age/<id_>/<age>')
def update_age(id_, age):
    """

    :param id_: ID of Person object ot modify, as integer
    :param age: New age for Person object
    :return: __repr__ of modified Person object
    """
    if not str(id_).isdigit():
        """
        id_ taken from parameters will be a string; id_ passed to the function may
        be an int. Performing str.isdigit() to cover either case.
        """
        abort(406, 'ID must be integer')
    if not str(age).isdigit():
        """
        As above
        """
        abort(406, 'Age must be integer')

    id_ = int(id_)
    age = int(age)
    from web import DB_URI
    from ..DBManager import DBManager
    db = DBManager(DB_URI)
    person = db.get_by_id(id_)
    if person.id != id_:
        abort(404, f'Nobody with ID of {id_} exists')
    person.update_age(age)
    person = db.save_person(person)
    response = make_response(
        jsonify(
            {'body': str(person), 'message': 'success'}
        ),
        200,
    )
    response.headers["Content-Type"] = "application/json"
    return response


@api.patch('/update_role/<id_>/<role>')
def update_role(id_, role):
    """

    :param id_: ID of Person object ot modify, as integer
    :param role: New age for Person object
    :return: __repr__ of modified Person object
    """
    if not str(id_).isdigit():
        """
        id_ taken from parameters will be a string; id_ passed to the function may
        be an int. Performing str.isdigit() to cover either case.
        """
        abort(406, 'ID must be integer')

    id_ = int(id_)
    from web import DB_URI
    from ..DBManager import DBManager
    db = DBManager(DB_URI)
    person = db.get_by_id(id_)
    if person.id != id_:
        abort(404, f'Nobody with ID of {id_} exists')
    person.update_role(role)
    person = db.save_person(person)
    response = make_response(
        jsonify(
            {'body': str(person), 'message': 'success'}
        ),
        200,
    )
    response.headers["Content-Type"] = "application/json"
    return response


@api.delete('/delete/<id_>')
def delete_entry(id_):
    if not str(id_).isdigit():
        """
        id_ taken from parameters will be a string; id_ passed to the function may
        be an int. Performing str.isdigit() to cover either case.
        """
        abort(406, 'ID must be integer')
    id_ = int(id_)
    from web import DB_URI
    from ..DBManager import DBManager
    db = DBManager(DB_URI)
    db.delete_entry(id_)
    response = make_response(
        {'message': 'success'},
        200,
    )
    response.headers["Content-Type"] = "application/json"
    return response


@api.post('/create')
def create_entry():
    data = request.get_json(silent=True, force=True)

    if data is None:
        abort(406, 'use json.dumps() on data packet')
    elif not all([attr in data.keys() for attr in ['name', 'age', 'role']]):
        abort(406, 'attributes name, age and role required')
    elif not str(data['age']).isdigit():
        abort(406, 'age must be digits')

    from ..models import Person
    from ..DBManager import DBManager
    db = DBManager('data.db')
    person = Person(name=data['name'], age=data['age'], role=data['role'])
    db.save_person(person)

    response = make_response(
        jsonify(
            {'body': person.name + ' created', 'message': 'success'}
        ),
        201,
    )
    response.headers["Content-Type"] = "application/json"
    return response
