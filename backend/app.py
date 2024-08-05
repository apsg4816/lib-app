from flask_jwt_extended import verify_jwt_in_request
from sqlalchemy import or_, and_, func
from flask import Blueprint, request, Response, make_response
import json
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Flask, request, jsonify, current_app, send_file
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from datetime import datetime, timedelta
from sqlalchemy.orm import joinedload
from celery_config import celery
import redis
from functools import wraps
from flask_caching import Cache



app = Flask(__name__)
redis_client = redis.Redis(host='localhost', port=6379, db=0)
cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS': redis_client})
CORS(app, origins='*')
app.config['JWT_SECRET_KEY'] = 'library_mac'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lib.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
celery.conf.update(app.config)

db = SQLAlchemy(app)
jwt = JWTManager(app)


# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    First_Name = db.Column(db.String(50))
    Last_Name = db.Column(db.String(50))
    user_name = db.Column(db.String(50))
    Interests = db.Column(db.String(250))
    role = db.Column(db.String(50), db.ForeignKey('role.name'))

# Role model


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


# Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ForSection = db.Column(db.String(100))
    Book_Title = db.Column(db.String(100))
    ForSection = db.Column(db.String(50))
    Author = db.Column(db.String(50))
    Content = db.Column(db.String(1000))


# Section Model
class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Section_Title = db.Column(db.String(100))
    DateCreated = db.Column(db.String(100))
    Description = db.Column(db.String(1000))


# Book Request Model
class RequestBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255))
    Section_Title = db.Column(db.String(255))
    BookId = db.Column(db.String(255))
    Book_Title = db.Column(db.String(255))
    email = db.Column(db.String(255))
    ReqStatus = db.Column(db.String(255))
    Ndays = db.Column(db.Integer)
    ReqdateTime = db.Column(db.DateTime)
    DuedateTime = db.Column(db.DateTime)


# Book Feedback
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    user_name = db.Column(db.String(255))
    Section_Title = db.Column(db.String(255))
    BookId = db.Column(db.String(255))
    Book_Title = db.Column(db.String(255))
    Book_Rating = db.Column(db.Integer)
    User_comments = db.Column(db.String(255))


def initialise_database():
    with app.app_context():
        inspector = db.inspect(db.engine)
        table_names = inspector.get_table_names()

        if not table_names:  # If no tables exist
            db.create_all()
            adminRole = Role(name='ADMIN', description='')
            userRole = Role(name='END_USER', description='')

            adminUser = User(email="apsg4816@gmail.com",
                             password=generate_password_hash("abhay"), role="ADMIN", active=True)

            db.session.add(adminRole)
            db.session.add(userRole)
            db.session.add(adminUser)

            db.session.commit()

            print("Database tables created.")
        else:
            print("Database tables already exist.")


# for initialising database with admin values
initialise_database()

def role_required(roles):
    """
        Decorator to verify roles of user. 
        Must be used after jwt_required decorator.
        
        PARAMS
        1. roles : A list of roles which are accepted
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                curr_user = get_jwt_identity()
                id = curr_user.get('id')

                if not id:
                    return {'msg' : 'Invalid Token'} , 403

                user = User.query.filter_by(id = id).first()
                if not user:
                    return {'msg' : 'User not found.'} , 404

                if not user.role in roles:
                    return {'msg' : 'Unauthorised.'} , 401
                return fn(*args, **kwargs)

            except Exception as e:
                return {'msg' : 'Internal Server Error'} , 500
        return wrapper
    return decorator

# To Register User
@app.route('/register', methods=['POST'])
def register_user():
    data = request.json

    if data.get('email') and data.get('password') and data.get('user_name'):
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'User already exists'}), 409
        if User.query.filter_by(user_name=data['user_name']).first():
            return jsonify({'message': 'User already exists'}), 409

        user = User(
            email=data['email'],
            password=generate_password_hash(data['password']),
            First_Name=data['First_Name'],
            Last_Name=data['Last_Name'],
            Interests=data['Interests'],
            user_name=data['user_name'],
            active=True,
            role="END_USER"
        )
        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 201
    else:
        return jsonify({'message': 'Missing details'}), 400


# User Login
@app.route('/login', methods=['POST'])
def user_login():
    data = request.get_json()

    if data.get('email') and data.get('password'):
        user = User.query.filter_by(email=data['email']).first()

        if user and check_password_hash(user.password, data['password']):
            identity = {'id': user.id, 'email': user.email}
            access_token = create_access_token(
                identity=identity, expires_delta=timedelta(2))

            return jsonify({
                'message': 'User logged in successfully',
                'access_token': access_token,
                'role': user.role,
                'id': user.id,
                'user_name': user.user_name,
                'First_Name': user.First_Name,
                'Last_Name': user.Last_Name,
                'Interests': user.Interests,
                'email': user.email
            }), 200

        return jsonify({'message': 'Invalid email or password'}), 401
    else:
        return jsonify({'message': 'Missing details'}), 400


# Admin CRUD Operations for Sections

@app.route('/admin_section', methods=['POST'])
@jwt_required()
@role_required(['ADMIN'])
def admin_section():
    if request.method == 'POST':
        data = request.json

        if data.get('Section_Title') and data.get('DateCreated') and data.get('Description'):
            if Section.query.filter_by(Section_Title=data['Section_Title']).first():
                return jsonify({'message': 'Section already exists'}), 409

            section = Section(
                Section_Title=data['Section_Title'],
                DateCreated=data['DateCreated'],
                Description=data['Description'],
            )
            db.session.add(section)
            db.session.commit()

            return jsonify({'message': 'Section Created successfully'}), 201
        else:
            return jsonify({'message': 'Missing details'}), 400


@app.route('/admin_section', methods=['GET'])
@jwt_required()
@cache.cached(timeout=2)
def admin_section_get():

    sections = Section.query.all()

    sections_data = []
    for section in sections:
        sections_data.append({
            'id': section.id,
            'Section_Title': section.Section_Title,
            'DateCreated': section.DateCreated,
            'Description': section.Description,
        })

    return jsonify({'sections': sections_data}), 200


@app.route('/admin_section/<int:id>', methods=['PUT', 'DELETE', 'GET'])
@jwt_required()

def update_delete_section(id):
    section = Section.query.get(id)
    if not section:
        return jsonify({"message": "Section Not Found"}), 404
    if request.method == 'GET':
        sections_data = {
            'id': section.id,
            'Section_Title': section.Section_Title,
            'DateCreated': section.DateCreated,
            'Description': section.Description,
        }
        return jsonify({'sections': sections_data}), 200
    if request.method == 'PUT':
        data = request.json

        if 'Section_Title' in data:
            section.Section_Title = data['Section_Title']
        if 'DateCreated' in data:
            section.DateCreated = data['DateCreated']
        if 'Description' in data:
            section.Description = data['Description']

        db.session.commit()

        return jsonify({'message': 'Section updated successfully'}), 200

    elif request.method == 'DELETE':
        db.session.delete(section)
        db.session.commit()

        return jsonify({'message': 'Section deleted successfully'}), 200


# Search for Sections and Books

@app.route('/section_book_search/<string:keyword>', methods=['GET'])
# @jwt_required()
def search_admin_section(keyword):

    sections_data = []
    books_data = []

    if keyword:

        # Search for sections with the keyword

        sections = Section.query.filter(or_(
            Section.Section_Title.ilike(f'%{keyword}%'),
            Section.Description.ilike(f'%{keyword}%')
        )).all()

        if sections:
            for section in sections:
                sections_data.append({
                    'id': section.id,
                    'Section_Title': section.Section_Title,
                    'Description': section.Description,
                })

        # Search for books with the keyword
        books = Book.query.filter(or_(
            Book.Book_Title.ilike(f'%{keyword}%'),
            Book.Author.ilike(f'%{keyword}%'),
        )).all()

        if books:
            for book in books:
                books_data.append({
                    'id': book.id,
                    # 'user_name': book.user_name,
                    'Book_Title': book.Book_Title,
                    'Author': book.Author,
                    'ForSection': book.ForSection,
                })

        return jsonify({'sections': sections_data}, {'books': books_data},), 200
    else:
        return jsonify({'message': 'Keyword parameter is missing'}), 400


# Admin CRUD Operations for Books
@app.route('/admin_book', methods=['POST'])
@jwt_required()
@role_required(['ADMIN'])
def admin_book():
    if request.method == 'POST':
        data = request.json

        if data.get('Book_Title') and data.get('Author') and data.get('Content') and data.get('ForSection'):
            if Book.query.filter_by(Book_Title=data['Book_Title']).first():
                return jsonify({'message': 'Book already exists'}), 409

            book = Book(
                ForSection=data['ForSection'],
                Book_Title=data['Book_Title'],
                Author=data['Author'],
                Content=data['Content'],
            )
            db.session.add(book)
            db.session.commit()

            return jsonify({'message': 'Book Created successfully'}), 201
        else:
            return jsonify({'message': 'Missing details'}), 400


@app.route('/admin_book', methods=['GET'])
@jwt_required()
@cache.cached(timeout=2)
def admin_book_get():
    books = Book.query.all()

    book_data = []
    for book in books:
        book_data.append({
            'id': book.id,
            'ForSection': book.ForSection,
            'Book_Title': book.Book_Title,
            'Author': book.Author,
            'Content': book.Content,
        })

    return jsonify({'books': book_data}), 200


@app.route('/admin_book/<int:id>', methods=['PUT', 'DELETE', 'GET'])
@jwt_required()

def update_delete_book(id):
    # Retrieve the book by ID
    book = Book.query.get(id)
    sections = Section.query.filter_by(Section_Title=book.ForSection).first()
    # Check if the book exists
    if not book:
        return jsonify({"message": "Book Not Found"}), 404

    if request.method == 'GET':
        # Create dictionary for book data
        book_data = {
            'id': book.id,
            'ForSection': book.ForSection,
            'Book_Title': book.Book_Title,
            'Author': book.Author,
            'Content': book.Content,
        }

        return jsonify({'book': book_data}), 200

    elif request.method == 'PUT':
        data = request.json
        if Section.query.filter_by(Section_Title=data['ForSection']).first():
            if 'ForSection' in data and sections:
                book.ForSection = data['ForSection']
            else:
                return jsonify({'message': 'Section Not Found'}), 404
            # Update book attributes if provided in the request data
            if 'Book_Title' in data:
                book.Book_Title = data['Book_Title']

            if 'Author' in data:
                book.Author = data['Author']
            if 'Content' in data:
                book.Content = data['Content']
        else:
            return jsonify({'message': 'Please use pre-existing Sections to change'}), 404
        # Commit changes to the database
        db.session.commit()

        return jsonify({'message': 'Book updated successfully'}), 200

    elif request.method == 'DELETE':
        # Delete the book
        db.session.delete(book)
        db.session.commit()

        return jsonify({'message': 'Book deleted successfully'}), 200


@app.route('/user_book/<string:book_title>', methods=['GET'])
def user_book_content(book_title):
    # Retrieve the book by Book_Title
    book = Book.query.filter_by(Book_Title=book_title).first()
    # Retrieve the book by ID
    # book = Book.query.get(id)

    # Check if the book exists
    if not book:
        return jsonify({"message": "Book Not Found"}), 404

    if request.method == 'GET':
        # Create dictionary for book data
        book_data = {
            'id': book.id,
            'ForSection': book.ForSection,
            'Book_Title': book.Book_Title,
            'Author': book.Author,
            'Content': book.Content,
        }

        return jsonify({'book': book_data}), 200


@app.route('/user_book/<int:id>', methods=['GET'])
# @jwt_required()
def user_book_read(id):
    # Retrieve the book by ID
    book = Book.query.get(id)

    # Check if the book exists
    if not book:
        return jsonify({"message": "Book Not Found"}), 404

    if request.method == 'GET':
        # Create dictionary for book data
        book_data = {
            'id': book.id,
            'ForSection': book.ForSection,
            'Book_Title': book.Book_Title,
            'Author': book.Author,
            'Content': book.Content,
        }

        return jsonify({'book': book_data}), 200


# User Book Request Operations
@app.route('/book_request', methods=['POST', 'GET'])
@jwt_required()
# @role_required(['END_USER'])
def book_request():
    if request.method == 'POST':
        data = request.json

        if data.get('Ndays'):
            ReqdateTime = datetime.now()
            Ndays = int(data['Ndays'])
            DuedateTime = ReqdateTime + timedelta(days=Ndays)

            ReqBook = RequestBook(
                user_name=data['user_name'],
                Book_Title=data['Book_Title'],
                Ndays=Ndays,
                Section_Title=data['Section_Title'],
                BookId=data['BookId'],
                ReqStatus=data['ReqStatus'],
                email=data['email'],
                ReqdateTime=ReqdateTime,
                DuedateTime=DuedateTime
            )
            db.session.add(ReqBook)
            db.session.commit()

            return jsonify({'message': 'Book Requested successfully'}), 201
        else:
            return jsonify({'message': 'Missing details'}), 900

    elif request.method == 'GET':
        books = RequestBook.query.all()

        user_book_data = []
        for book in books:
            # Check if the due date has passed
            if book.DuedateTime and book.DuedateTime < datetime.now():
                # If the due date has passed, update the ReqStatus to "Rejected"
                book.ReqStatus = "Rejected"
                # Commit the change to the database
                db.session.commit()

            user_book_data.append({
                'id': book.id,
                'user_name': book.user_name,
                'Book_Title': book.Book_Title,
                'Section_Title': book.Section_Title,
                'Ndays': book.Ndays,
                'ReqStatus': book.ReqStatus,
                'BookId': book.BookId
            })

        return jsonify({'bookReq': user_book_data}), 200

    elif request.method == 'PATCH':
        data = request.json
        book_data = RequestBook.query.get(id)
        if book_data:
            if 'ReqStatus' in data:
                book_data.ReqStatus = data['ReqStatus']

            db.session.commit()
            return jsonify({'message': 'ReqStatus Updated successfully'}), 200
        return jsonify({'message': 'Book Details not found'}), 404


# PATCH REQUEST
@app.route('/book_request/<int:requestId>', methods=['PATCH'])
@jwt_required()
def changeStatus(requestId):
    book_data = RequestBook.query.get(requestId)
    if book_data:
        ReqdateTime = datetime.now()
        Ndays = int(book_data.Ndays)
        DuedateTime = ReqdateTime + timedelta(days=Ndays)
        # Assuming you receive the new status in the request JSON data
        data = request.json
        if 'ReqStatus' in data:
            book_data.ReqStatus = data['ReqStatus']
            book_data.ReqdateTime = ReqdateTime
            book_data.DuedateTime = DuedateTime
            db.session.commit()
            return jsonify({'message': 'ReqStatus Updated successfully'}), 200
        else:
            return jsonify({'message': 'ReqStatus not provided in request data'}), 400
    else:
        return jsonify({'message': 'Book Details not found'}), 404


# cache implemented
@app.route('/user_book/search', methods=['GET'])
@cache.cached(timeout=2)
@jwt_required()

def search_user_book():
    keyword = request.args.get('keyword')
    if keyword:
        # Search for booked tickets with the keyword
        book = Book.query.filter(or_(
            Book.Book_Title.ilike(f'%{keyword}%'),
            Book.Author.ilike(f'%{keyword}%'),
            Book.ForSection.ilike(f'%{keyword}%'),
            Book.Content.ilike(f'%{keyword}%')
        )).all()

        book_data = []
        for books in book:
            books.append({
                'id': book.id,
                'user_name': book.user_name,
                'Book_Title': book.Book_Title,
                'Author': book.Author,
                'ForSection': book.ForSection,
            })

        return jsonify({'tbooked': books}), 200
    else:
        return jsonify({'message': 'Keyword parameter is missing'}), 400


@app.route('/user_feedback', methods=['POST', 'GET'])
@jwt_required()

def user_comments():
    if request.method == 'POST':
        data = request.json

        if data.get('Book_Rating') and data.get('BookId') and data.get('user_id') and data.get('User_comments'):
            # if Feedback.query.filter_by(BookId=data['BookId'] , user_id=data['user_id'] ).first():
            #     return jsonify({'message': 'Feedback already exists for this book by this user'}), 409
            if (int(data.get('Book_Rating')) < 0 or int(data.get('Book_Rating')) > 5):
                return jsonify({'message': 'Rating should be between 0 and 5'}), 409

            feedback = Feedback(
                Section_Title=data['Section_Title'],
                Book_Rating=data['Book_Rating'],
                BookId=data['BookId'],
                Book_Title=data['Book_Title'],
                User_comments=data['User_comments'],
                user_name=data['user_name'],
                user_id=data['user_id'],
            )
            db.session.add(feedback)
            db.session.commit()

            return jsonify({'message': 'Feedback Given successfully'}), 201
        else:
            return jsonify({'message': 'Missing details'}), 400

    elif request.method == 'GET':

        feedbacks = Feedback.query.all()

        feedback_data = []
        for feedback in feedbacks:
            feedback_data.append({
                'id': feedback.id,
                'Section_Title': feedback.Section_Title,
                'Book_Title': feedback.Book_Title,
                'Book_Rating': feedback.Book_Rating,
                'User_comments': feedback.User_comments,
                'user_name': feedback.user_name,
                'user_id': feedback.user_id,
                'BookId': feedback.BookId,

            })

        return jsonify({'feedback': feedback_data}), 200


@app.route('/user_export/', methods=['GET'])
@jwt_required
def export_user_book_data(id):
    try:

        from tasks import export_user_books_details_as_csv

        csv_data = export_user_books_details_as_csv(id)
        response = make_response(csv_data)
        response.headers["Content-Disposition"] = "attachment;filename=user_book_data.csv"
        response.headers['Content-Type'] = "text/csv"

        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/export_book_data', methods=['GET'])
def export_book_data():
    try:
        from tasks import export_books_details_as_csv

        csv_data = export_books_details_as_csv()
        response = make_response(csv_data)
        response.headers["Content-Disposition"] = "attachment;filename=book_data.csv"
        response.headers['Content-Type'] = "txt/csv"

        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

if __name__ == '__main__':
    app.run(port=5000)
