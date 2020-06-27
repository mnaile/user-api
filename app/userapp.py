from flask import Flask, request,jsonify,send_file, send_from_directory
from http import HTTPStatus
from marshmallow.exceptions import ValidationError
from app.model import User, UserBooks
from app.serializer import UpdateSchema, UserSchema
from app_init.app_factory import create_app
import requests

    

app = create_app()
#CREATE USER

@app.route('/users', methods=["POST"])
def register():
    user_info = request.get_json()
    user = User.query.filter_by(email = user_info.get("email")).first()
    if user:
        return jsonify(msg="User exsist"),HTTPStatus.BAD_REQUEST
    try:    
        user = UserSchema().load(user_info)
        response = requests.get(f"http://127.0.0.1:5002/books/{user_info.get('book_id')}")
        if user:  
            user.set_password()
            user = user.save_db()   
            if response.status_code == 200:
                user_books = UserBooks()
                user_books.user_id = user.id
                user_books.book_id = response.json().get('id')
                user_books.save_db()
            
        else:
            return jsonify(msg="Not found!"),HTTPStatus.NOT_FOUND
    except ValidationError as err:
        return jsonify(err.messages),HTTPStatus.BAD_REQUEST
    # user.set_password()
    # user.save_db()
    # user = User(**user)
    # db.session.add(user)
    # db.session.commit()
    return UserSchema(exclude=["password"]).jsonify(user),HTTPStatus.OK

@app.route('/users/<int:id>/books', methods=["POST"])
def create_user_books(id):
    user = User.query.get(id)
    if user:
        user_books = request.json.get('book_id')
        if user_books:
            books = UserBooks()
            books.user_id = user.id
            books.book_id = user_books
            books.save_db()
            return jsonify(msg="OK"),HTTPStatus.OK

    return jsonify(msg="User or book not found"),HTTPStatus.NOT_FOUND




# READ USER
@app.route('/users/<int:id>', methods=["GET"])
def get_id(id):
    user = User.query.filter_by(id=id).first()
    if user:
        user_books = UserBooks.query.filter_by(user_id = user.id).all()
        if user_books:
            temp = []
            for i in user_books:
                response = requests.get(f"http://127.0.0.1:5002/books/{i.book_id}")
                if response.status_code == 200:
                    temp.append(response.json())
            userschema = UserSchema()
            data = userschema.dump(user)
            data['books_info']=temp
            return jsonify(data),HTTPStatus.OK

                
        return UserSchema().jsonify(user),HTTPStatus.OK

    return jsonify(msg="User not found"),HTTPStatus.NOT_FOUND

@app.route('/users', methods=["GET"])
def get_all():
    user = User.query.all()

    # temp = []
    # for i in user:
    #     temp.append({
    #         "name" : i.name,
    #         "surname": i.surname,
    #         "email": i.email,
    #         "password": i.password
    #     })

    return UserSchema().jsonify(user,many=True),HTTPStatus.OK   

#DELETE USER

@app.route('/users/<int:id>', methods=["DELETE"])
def delete(id):
    user = User.query.filter_by(id=id).first()
    if user:
        # db.session.delete(user)
        # db.session.commit()
        user.delete_from_db()
        return jsonify(result=True),HTTPStatus.OK

    return jsonify(msg="User not found"),HTTPStatus.NOT_FOUND

# UPDATE USER

@app.route('/users/<int:id>', methods=["PUT"])
def update(id):
    user = User.query.filter_by(id=id).first()
    if user:
        user_info = request.get_json()
        users = UpdateSchema().load(user_info)
        user.update_db(**users)
        # if user_info.get("name"):
        #     user.name = user_info.get("name")
        # if user_info.get("surname"):
        #     user.surname = user_info.get("surname")
        # db.session.add(user)
        # db.session.commit()
        return UserSchema().jsonify(user_info),HTTPStatus.OK
    return jsonify(msg="User not found"),HTTPStatus.NOT_FOUND




# CREATE FILE

@app.route('/users/<int:id>/files', methods=["POST"])
def create_file(id):
    user = User.query.filter_by(id=id).first()
    if user:
        for _, val in request.files.items():
            user.update_db(filename = val.filename)
            with open(val.filename, "wb") as wr:
                wr.write(val.read())
                return jsonify(msg="ok"),HTTPStatus.OK
    return jsonify(msg="Not found"),HTTPStatus.NOT_FOUND

@app.route('/users/<int:id>/files', methods=["GET"])
def get_file(id):
    user = User.query.filter_by(id=id).first()
    if user:
        if user.filename:
            return send_from_directory("/home/naile/Desktop/flaskuser/", filename=user.filename, mimetype="image/png"),HTTPStatus.OK

    return jsonify(msg="Not found"),HTTPStatus.NOT_FOUND

