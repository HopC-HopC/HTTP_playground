from flask import Blueprint, render_template, url_for, make_response, jsonify, request

api = Blueprint('api', __name__)


@api.route('/get/<id_>', methods=['GET'])
def get_by_id(id_):
    """

    :param id_: retrieve ID from URL; must be int
    :return: __repr__ of Person object
    """
    from web import DB_URI
    from ..DBManager import DBManager
    db = DBManager(DB_URI)
    if str(id_).isdigit():
        id_ = int(id_)
        person = db.get_by_id(id_)
        if person.id == id_:
            response = make_response(
                jsonify(
                    {'body': str(person)}
                ),
                200,
            )
            response.headers["Content-Type"] = "application/json"
            return response
    else:
        response = make_response(jsonify({'message': 'ID must be integer'}), 406)
        response.headers["Content-Type"] = "application/json"
        return response


@api.route('/get_all', methods=['GET'])
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
            person = Person(id=entry[0], age=entry[1], name=entry[2], role=entry[3])
            people[person.id] = str(person)
    response = make_response(
        jsonify(
            people
        ),
        200,
    )
    response.headers["Content-Type"] = "application/json"
    return response


@api.route('/generate', methods=['GET'])
def generate():
    """
    Populates database with Person objects
    :return: status OK
    """
    from web import DB_URI
    from ..DBManager import DBManager
    db = DBManager(DB_URI)
    from ..models import Person
    person1 = Person('Jeff', 22)
    person2 = Person('Frank',44)
    person3 = Person('Shelley', 33)
    db.save_person(person1)
    db.save_person(person2)
    db.save_person(person3)
    return 200, 'OK'


@api.route('/update_age/<id_>/<age>', methods=['PATCH', 'GET', 'POST'])
def update_age(id_, age):
    """

    :param id_:
    :param age:
    :return:
    """
    if not request.method == 'PATCH':
        response = make_response(jsonify({'message': 'Method not allowed'}), 405)
        response.headers["Content-Type"] = "application/json"
        return response
    if not str(id_).isdigit():
        response = make_response(jsonify({'message': 'ID must be integer'}), 406)
        response.headers["Content-Type"] = "application/json"
        return response
    if not str(age).isdigit():
        response = make_response(jsonify({'message': 'Age must be integer'}), 406)
        response.headers["Content-Type"] = "application/json"
        return response

    id_ = int(id_)
    age = int(age)
    from web import DB_URI
    from ..DBManager import DBManager
    db = DBManager(DB_URI)
    person = db.get_by_id(id_)
    if person.id != id_:
        response = make_response(jsonify({'message': f'Nobody with ID of {id_} exists'}), 404)
        response.headers["Content-Type"] = "application/json"
        return response
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


