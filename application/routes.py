from application import app, db, mail
from flask import jsonify, request
from application.models import User, Course, UserSchema, CourseSchema
from flask_jwt_extended import jwt_required, create_access_token
from flask_mail import Message

user_schema = UserSchema()
users_schema = UserSchema(many=True)

course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created!')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped!')


@app.cli.command('db_seed')
def db_seed():
    msdba = Course(course_name='MS DBA',
                   course_type='DE',
                   teacher='Jie Liu',
                   hours=40,
                   tution=1100)

    powerbi = Course(course_name='MS POWERBI',
                     course_type='DA',
                     teacher='Jie Liu',
                     hours=20,
                     tution=800)

    azureai = Course(course_name='AZURE AI',
                     course_type='AI',
                     teacher='Louis Li',
                     hours=40,
                     tution=800)

    db.session.add(msdba)
    db.session.add(powerbi)
    db.session.add(azureai)

    father = User(first_name='Ping',
                  last_name='Xu',
                  email='ping@test.com',
                  password='P@ssw0rd')

    child = User(first_name='Eric',
                 last_name='Xu',
                 email='eric@test.com',
                 password='P@ssw0rd')

    db.session.add(father)
    db.session.add(child)
    db.session.commit()
    print('Database seeded!')


@app.route('/')
def hello_world():
    return jsonify(message='hello world!')


@app.route('/super_simple')
def super_simple():
    return jsonify(message='Hello from Super Simple!')


@app.route('/not_found')
def not_found():
    return jsonify(message='That resource was not found!'), 404


@app.route('/parameters')
def parameters():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    if age < 18:
        return jsonify(message=f'Hi {name}, Age must be older than 18'), 401
    else:
        return jsonify(message=f'Hi {name}, welcome here')


@app.route('/url_variables/<string:name>/<int:age>')
def url_variables(name: str, age: int):
    if age < 18:
        return jsonify(message=f'Hi {name}, Age must be older than 18'), 401
    else:
        return jsonify(message=f'Hi {name}, welcome here')


@app.route('/users', methods=['GET'])
def users():
    users_list = User.query.all()
    result = users_schema.dump(users_list)
    return jsonify(result)


@app.route('/users/<int:user_id>', methods=['GET'])
def user_detail(user_id: int):
    user = User.query.filter_by(id=user_id).first()
    result = user_schema.dump(user)
    return jsonify(result)


@app.route('/courses', methods=['GET'])
def courses():
    courses_list = Course.query.all()
    result = courses_schema.dump(courses_list)
    return jsonify(result)


@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    test = User.query.filter_by(email=email).first()
    if test:
        return jsonify(message='That email is already registered.'), 409
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message='Registration successful'), 201


@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    test = User.query.filter_by(email=email, password=password).first()
    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message="Login succeeded!", access_token=access_token)
    else:
        return jsonify(message="Bad email or password"), 401


@app.route('/course_details/<int:course_id>', methods=['GET'])
def course_details(course_id: int):
    course = Course.query.filter_by(id=course_id).first()
    if course:
        result = course_schema.dump(course)
        return jsonify(result)
    else:
        return jsonify(message="That course_id doesn't exist"), 404


@app.route('/add_course', methods=['POST'])
@jwt_required()
def add_course():
    course_name = request.form['course_name']
    test = Course.query.filter_by(course_name=course_name).first()
    if test:
        return jsonify(message="That course_id has already exists"), 409
    else:
        course_type = request.form['course_type']
        teacher = request.form['teacher']
        course_hours = int(request.form['course_hours'])
        course_tution = float(request.form['course_tution'])
        course = Course(course_name=course_name, course_type=course_type, teacher=teacher, hours=course_hours, tution=course_tution)
        db.session.add(course)
        db.session.commit()
        return jsonify(message="Course is added successfully"), 201


@app.route('/update_course', methods=['PUT'])
@jwt_required()
def update_course():
    course_name = request.form['course_name']
    course = Course.query.filter_by(course_name=course_name).first()
    if course:
        course.course_type = request.form['course_type']
        course.teacher = request.form['teacher']
        course.hours = int(request.form['course_hours'])
        course.tution = float(request.form['course_tution'])
        db.session.commit()
        return jsonify(message="Course is updated successfully"), 201
    else:
        return jsonify(message="That course doesn't exists"), 409


@app.route('/remove_course/<string:course_name>', methods=['DELETE'])
@jwt_required()
def remove_course(course_name: str):
    course = Course.query.filter_by(course_name=course_name).first()
    if course:
        db.session.delete(course)
        db.session.commit()
        return jsonify(message="Course is removed successfully"), 201
    else:
        return jsonify(message="That course doesn't exists"), 409


@app.route('/retrieve_password/<string:email>', methods=['GET'])
def retrieve_password(email: str):
    user = User.query.filter_by(email=email).first()
    if user:
        msg = Message("your planetary API password is " + user.password,
                      sender="admin@planetary-api.com",
                      recipients=[email])
        mail.send(msg)
        return jsonify(message="Password sent to " + email)
    else:
        return jsonify(message="That email doesn't exist"), 401
