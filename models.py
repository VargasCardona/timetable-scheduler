import enum
from sqlalchemy import (
    Column,
    String,
    BINARY,
    DateTime,
    Boolean,
    Integer,
    ForeignKey,
    Table,
    Enum,
    Time,
    func
)
from sqlalchemy.orm import relationship
from config import Base

# Association table for many-to-many relationship between professors and courses
professor_course_association = Table(
    'professor_course',
    Base.metadata,
    Column('professor_id', BINARY(16), ForeignKey('professors.id')),
    Column('course_id', BINARY(16), ForeignKey('courses.id'))
)


class WeekDay(enum.Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"


class TimeBlock(enum.Enum):
    MORNING = "Morning"
    AFTERNOON = "Afternoon"
    EVENING = "Evening"
    SATURDAY = "Saturday"


class ProfessorModel(Base):
    __tablename__ = "professors"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, index=True)
    document_id = Column(String(20), nullable=False, unique=True, index=True)
    
    # Relationships
    courses = relationship("CourseModel", secondary=professor_course_association, back_populates="professors")
    restrictions = relationship("ProfessorRestrictionModel", back_populates="professor", cascade="all, delete-orphan")
    schedules = relationship("ScheduleModel", back_populates="professor", cascade="all, delete-orphan")
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class ProfessorRestrictionModel(Base):
    __tablename__ = "professor_restrictions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    professor_id = Column(BINARY(16), ForeignKey('professors.id'), nullable=False)
    weekday = Column(Enum(WeekDay), nullable=False)
    time_block = Column(Enum(TimeBlock), nullable=False)
    
    # Relationships
    professor = relationship("ProfessorModel", back_populates="restrictions")
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class CourseModel(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(20), nullable=False, unique=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    weekly_hours = Column(Integer, nullable=False, default=4)  # Default to 4 hours per week
    requires_equipment = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    professors = relationship("ProfessorModel", secondary=professor_course_association, back_populates="courses")
    schedules = relationship("ScheduleModel", back_populates="course", cascade="all, delete-orphan")
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class ClassroomModel(Base):
    __tablename__ = "classrooms"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    has_equipment = Column(Boolean, default=False, nullable=False)
    capacity = Column(Integer, nullable=False, default=30)
    
    # Relationships
    schedules = relationship("ScheduleModel", back_populates="classroom", cascade="all, delete-orphan")
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class ScheduleModel(Base):
    __tablename__ = "schedules"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(BINARY(16), ForeignKey('courses.id'), nullable=False)
    professor_id = Column(BINARY(16), ForeignKey('professors.id'), nullable=False)
    classroom_id = Column(BINARY(16), ForeignKey('classrooms.id'), nullable=False)
    weekday = Column(Enum(WeekDay), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    
    # Relationships
    course = relationship("CourseModel", back_populates="schedules")
    professor = relationship("ProfessorModel", back_populates="schedules")
    classroom = relationship("ClassroomModel", back_populates="schedules")
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
