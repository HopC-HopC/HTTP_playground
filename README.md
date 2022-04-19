# HTTP_playground
API example showing HTTP verbs and status codes, along with SQLite helper class. Using Python with Flask.

## Setup:
```bash
Unix:
python3 -m venv <directory>
cd <directory>
pip3 install requirements.txt
python3 app.py
```
Install packages from requirements.txt. Run Flask application,
start point app.py.

## API Endpoints:
**GET /get_all**
\
Retrieve all data

**GET /get/<*id*>**
\
Pass integer for ID to retrieve data


**PATCH /update_age/<*id*>/<*age*>**
\
Pass integers for ID and age to update entry


**PATCH /update_role/<*id*>/<*role*>**
\
Pass integer for ID and string for role to update entry



**DELETE /delete/<*id*>**
\
Pass integer for ID to delete entry



**POST /create**
\
Create entry by including JSON object:\
```JSON
data: {
    'name': <name: str>,
    'age': <age: int>,
    'role': <role: str>
}
```
