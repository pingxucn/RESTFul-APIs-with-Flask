from application import db, ma
from sqlalchemy import Column, Integer, String, Float


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)


class Course(db.Model):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    course_name = Column(String)
    course_type = Column(String)
    teacher = Column(String)
    hours = Column(Integer)
    tution = Column(Float)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password')


class CourseSchema(ma.Schema):
    class Meta:
        fields = ('id', 'course_name', 'course_type', 'teacher', 'hours', 'tution')
