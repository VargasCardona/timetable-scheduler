import enum
from datetime import time
from typing import List, Optional, Dict, Tuple
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import (
    ProfessorModel,
    CourseModel, 
    ClassroomModel,
    ScheduleModel,
    ProfessorRestrictionModel,
    WeekDay,
    TimeBlock
)


class SchedulerService:
    """
    Service to handle scheduling logic for courses, professors, and classrooms.
    """
    
    @staticmethod
    def add_professor(
        db: Session, 
        name: str, 
        document_id: str
    ) -> ProfessorModel:
        """Add a new professor to the database."""
        if not name or not document_id:
            raise ValueError("Name and document ID are required")

        try:
            professor = ProfessorModel(
                name=name,
                document_id=document_id
            )
            db.add(professor)
            db.commit()
            db.refresh(professor)
        except IntegrityError as exc:
            db.rollback()
            raise ValueError(f"Professor with document ID {document_id} already exists") from exc
        
        return professor

    @staticmethod
    def update_professor(
        db: Session,
        professor_id: str,
        name: Optional[str] = None,
        document_id: Optional[str] = None
    ) -> Optional[ProfessorModel]:
        """Update an existing professor's details."""
        professor = db.query(ProfessorModel).filter(ProfessorModel.id == professor_id).first()
        if not professor:
            raise ValueError(f"Professor with ID {professor_id} not found")
        
        # Update only the fields that are provided
        if name:
            professor.name = name
        if document_id:
            professor.document_id = document_id
        
        try:
            db.commit()
            db.refresh(professor)
        except IntegrityError as exc:
            db.rollback()
            raise ValueError(f"Professor with document ID {document_id} already exists") from exc
        
        return professor

    @staticmethod
    def delete_professor(db: Session, professor_id: str) -> bool:
        """Delete a professor by their ID."""
        professor = db.query(ProfessorModel).filter(ProfessorModel.id == professor_id).first()
        if professor:
            db.delete(professor)
            db.commit()
            return True
        return False
    
    @staticmethod
    def get_professors(db: Session) -> Optional[List[ProfessorModel]]:
        """Get a professors"""
        return db.query(ProfessorModel).all()

    @staticmethod
    def get_professor_by_id(db: Session, id: str) -> Optional[ProfessorModel]:
        """Get a professor by their ID."""
        professor = db.query(ProfessorModel).filter(ProfessorModel.id == id).first()
        if not professor:
            raise ValueError(f"Professor with ID {id} not found")
        return professor
    
    @staticmethod
    def get_professor_by_name(db: Session, name: str) -> List[ProfessorModel]:
        """Get professors by name (partial match)."""
        return db.query(ProfessorModel).filter(ProfessorModel.name.ilike(f'%{name}%')).all()
    
    @staticmethod
    def add_professor_restriction(
        db: Session, 
        professor_id: int, 
        weekday: WeekDay, 
        time_block: TimeBlock
    ) -> ProfessorRestrictionModel:
        """Add a time restriction for a professor."""
        restriction = ProfessorRestrictionModel(
            professor_id=professor_id,
            weekday=weekday,
            time_block=time_block
        )
        db.add(restriction)
        db.commit()
        db.refresh(restriction)
        return restriction

    @staticmethod
    def update_course(
        db: Session,
        course_id: str,
        code: Optional[str] = None,
        name: Optional[str] = None,
        weekly_hours: Optional[int] = None,
        requires_equipment: Optional[bool] = None
    ) -> Optional[CourseModel]:
        """Update an existing course's details."""
        course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
        if not course:
            raise ValueError(f"Course with ID {course_id} not found")

        # Update only the fields that are provided
        if code:
            course.code = code
        if name:
            course.name = name
        if weekly_hours is not None:
            if weekly_hours not in [3, 4]:
                raise ValueError("Weekly hours must be either 3 or 4")
            course.weekly_hours = weekly_hours
        if requires_equipment is not None:
            course.requires_equipment = requires_equipment

        try:
            db.commit()
            db.refresh(course)
        except IntegrityError as exc:
            db.rollback()
            raise ValueError(f"Course with code {code} already exists") from exc

        return course


    @staticmethod
    def delete_course(db: Session, course_id: str) -> bool:
        """Delete a course by its ID."""
        course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
        if course:
            db.delete(course)
            db.commit()
            return True
        return False


    @staticmethod
    def get_courses(db: Session) -> Optional[List[CourseModel]]:
        """Get all courses."""
        return db.query(CourseModel).all()


    @staticmethod
    def get_course_by_id(db: Session, course_id: str) -> Optional[CourseModel]:
        """Get a course by its ID."""
        course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
        if not course:
            raise ValueError(f"Course with ID {course_id} not found")
        return course
    
    @staticmethod
    def add_course(
        db: Session, 
        code: str, 
        name: str, 
        weekly_hours: int = 4, 
        requires_equipment: bool = False
    ) -> CourseModel:
        """Add a new course to the database."""
        if not code or not name:
            raise ValueError("Code and name are required")
        if weekly_hours not in [3, 4]:
            raise ValueError("Weekly hours must be either 3 or 4")
        if requires_equipment not in [True, False]:
            raise ValueError("Requires equipment must be a boolean value")

        course = CourseModel(
            code=code,
            name=name,
            weekly_hours=weekly_hours,
            requires_equipment=requires_equipment
        )
        db.add(course)
        db.commit()
        db.refresh(course)
        return course
    
    @staticmethod
    def add_classroom(
        db: Session, 
        name: str, 
        has_equipment: bool = False, 
        capacity: int = 30
    ) -> ClassroomModel:
        """Add a new classroom to the database."""
        if not name:
            raise ValueError("Name is required")
        if capacity <= 0:
            raise ValueError("Capacity must be a positive integer")
        if has_equipment not in [True, False]:
            raise ValueError("Has equipment must be a boolean value")

        classroom = ClassroomModel(
            name=name,
            has_equipment=has_equipment,
            capacity=capacity
        )
        db.add(classroom)
        db.commit()
        db.refresh(classroom)
        return classroom


    @staticmethod
    def update_classroom(
        db: Session,
        classroom_id: str,
        name: Optional[str] = None,
        has_equipment: Optional[bool] = None,
        capacity: Optional[int] = None
    ) -> Optional[ClassroomModel]:
        """Update an existing classroom's details."""
        classroom = db.query(ClassroomModel).filter(ClassroomModel.id == classroom_id).first()
        if not classroom:
            raise ValueError(f"Classroom with ID {classroom_id} not found")

        # Update only the fields that are provided
        if name:
            classroom.name = name
        if has_equipment is not None:
            classroom.has_equipment = has_equipment
        if capacity is not None:
            if capacity <= 0:
                raise ValueError("Capacity must be a positive integer")
            classroom.capacity = capacity

        try:
            db.commit()
            db.refresh(classroom)
        except IntegrityError as exc:
            db.rollback()
            raise ValueError(f"Classroom with name {name} already exists") from exc

        return classroom


    @staticmethod
    def delete_classroom(db: Session, classroom_id: str) -> bool:
        """Delete a classroom by its ID."""
        classroom = db.query(ClassroomModel).filter(ClassroomModel.id == classroom_id).first()
        if classroom:
            db.delete(classroom)
            db.commit()
            return True
        return False


    @staticmethod
    def get_classrooms(db: Session) -> Optional[List[ClassroomModel]]:
        """Get all classrooms."""
        return db.query(ClassroomModel).all()


    @staticmethod
    def get_classroom_by_id(db: Session, classroom_id: str) -> Optional[ClassroomModel]:
        """Get a classroom by its ID."""
        classroom = db.query(ClassroomModel).filter(ClassroomModel.id == classroom_id).first()
        if not classroom:
            raise ValueError(f"Classroom with ID {classroom_id} not found")
        return classroom
    
    @staticmethod
    def assign_course_to_professor(
        db: Session, 
        professor_id: int, 
        course_id: int
    ) -> None:
        """Assign a course to a professor."""
        professor = db.query(ProfessorModel).filter(ProfessorModel.id == professor_id).first()
        course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
        
        if not professor:
            raise ValueError(f"Professor with ID {professor_id} not found")
        if not course:
            raise ValueError(f"Course with ID {course_id} not found")
    
        # Check if professor already has 6 courses
        if len(professor.courses) >= 6:
            raise ValueError("Professor already has the maximum of 6 courses assigned")
        
        try:
            professor.courses.append(course)
            db.commit()
        except IntegrityError as exc:
            db.rollback()
            raise ValueError(f"Course {course.name} is already assigned to professor {professor.name}") from exc
    
    @staticmethod
    def remove_course_from_professor(
        db: Session, 
        professor_id: int, 
        course_id: int
    ) -> None:
        """Remove a course from a professor."""
        professor = db.query(ProfessorModel).filter(ProfessorModel.id == professor_id).first()
        course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
        
        if not professor:
            raise ValueError(f"Professor with ID {professor_id} not found")
        if not course:
            raise ValueError(f"Course with ID {course_id} not found")
        
        # Check if the course is already scheduled
        if db.query(ScheduleModel).filter(
            ScheduleModel.course_id == course_id, ScheduleModel.professor_id == professor_id
        ).count() > 0:
            raise ValueError(f"Course {course.name} is already scheduled and cannot be removed")

        if course in professor.courses:
            professor.courses.remove(course)
            db.commit()
        else:
            raise ValueError(f"Course {course.name} is not assigned to professor {professor.name}")

    @staticmethod
    def schedule_course_session(
        db: Session,
        course_id: int,
        professor_id: int,
        classroom_id: int,
        weekday: WeekDay,
        start_time: time,
        end_time: time
    ) -> ScheduleModel:
        """Schedule a session for a course with professor and classroom."""
        # Check if professor is assigned to this course
        professor = db.query(ProfessorModel).filter(ProfessorModel.id == professor_id).first()
        course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
        
        if not professor:
            raise ValueError(f"Professor with ID {professor_id} not found")
        if not course:
            raise ValueError(f"Course with ID {course_id} not found")
        if course not in professor.courses:
            raise ValueError(f"Professor {professor.name} is not assigned to course {course.name}")
        
        # Check if the time is valid
        if start_time >= end_time:
            raise ValueError("Start time must be before end time")
        if start_time < time(8, 0) or end_time > time(22, 0):
            raise ValueError("Classroom hours must be between 08:00 and 22:00")
        course_duration = (end_time.hour - start_time.hour) + (end_time.minute - start_time.minute) / 60
        if course.weekly_hours == 3 and course_duration != 3:
            raise ValueError("3-hour courses must be scheduled in one block")
        if course.weekly_hours == 4 and course_duration != 2:
            raise ValueError("4-hour courses must be scheduled in two blocks of 2 hours each")

        # Check if professor has a restriction for this time
        time_block = SchedulerService._determine_time_block(start_time)
        restriction = db.query(ProfessorRestrictionModel).filter(
            ProfessorRestrictionModel.professor_id == professor_id,
            ProfessorRestrictionModel.weekday == weekday,
            ProfessorRestrictionModel.time_block == time_block
        ).first()
        
        if restriction:
            raise ValueError(f"Professor has a restriction for {weekday.value} during {time_block.value}")
        
        # Check if classroom has required equipment
        classroom = db.query(ClassroomModel).filter(ClassroomModel.id == classroom_id).first()

        if not classroom:
            raise ValueError(f"Classroom with ID {classroom_id} not found")
        if course.requires_equipment and not classroom.has_equipment:
            raise ValueError(f"Course {course.name} requires equipment but classroom {classroom.name} doesn't have it")
        
        # Check for scheduling conflicts
        SchedulerService._check_scheduling_conflicts(
            db, professor_id, classroom_id, weekday, start_time, end_time
        )
        
        # Create schedule
        schedule = ScheduleModel(
            course_id=course_id,
            professor_id=professor_id,
            classroom_id=classroom_id,
            weekday=weekday,
            start_time=start_time,
            end_time=end_time
        )
        
        db.add(schedule)
        db.commit()
        db.refresh(schedule)
        return schedule
    
    @staticmethod
    def remove_course_session(
        db: Session,
        schedule_id: int
    ) -> None:
        """Remove a scheduled session."""
        schedule = db.query(ScheduleModel).filter(ScheduleModel.id == schedule_id).first()
        if not schedule:
            raise ValueError(f"Schedule with ID {schedule_id} not found")
        
        db.delete(schedule)
        db.commit()

    @staticmethod
    def _determine_time_block(start_time: time) -> TimeBlock:
        """Determine the time block based on the start time."""
        if start_time < time(12, 0):
            return TimeBlock.MORNING
        elif start_time < time(18, 0):
            return TimeBlock.AFTERNOON
        else:
            return TimeBlock.EVENING
    
    @staticmethod
    def _check_scheduling_conflicts(
        db: Session,
        professor_id: int,
        classroom_id: int,
        weekday: WeekDay,
        start_time: time,
        end_time: time
    ) -> None:
        """Check for scheduling conflicts with existing schedules."""
        # Check professor schedule conflicts
        professor_conflicts = db.query(ScheduleModel).filter(
            ScheduleModel.professor_id == professor_id,
            ScheduleModel.weekday == weekday,
            ((ScheduleModel.start_time <= start_time) & (ScheduleModel.end_time > start_time)) |
            ((ScheduleModel.start_time < end_time) & (ScheduleModel.end_time >= end_time)) |
            ((ScheduleModel.start_time >= start_time) & (ScheduleModel.end_time <= end_time))
        ).first()
        
        if professor_conflicts:
            raise ValueError(f"Professor already has a class scheduled at this time on {weekday.value}")
        
        # Check classroom schedule conflicts
        classroom_conflicts = db.query(ScheduleModel).filter(
            ScheduleModel.classroom_id == classroom_id,
            ScheduleModel.weekday == weekday,
            ((ScheduleModel.start_time <= start_time) & (ScheduleModel.end_time > start_time)) |
            ((ScheduleModel.start_time < end_time) & (ScheduleModel.end_time >= end_time)) |
            ((ScheduleModel.start_time >= start_time) & (ScheduleModel.end_time <= end_time))
        ).first()
        
        if classroom_conflicts:
            raise ValueError(f"Classroom is already booked at this time on {weekday.value}")
    
    @staticmethod
    def get_professor_schedule(db: Session, professor_id: int) -> List[ScheduleModel]:
        """Get the complete schedule for a professor."""
        return db.query(ScheduleModel).filter(ScheduleModel.professor_id == professor_id).all()
    
    @staticmethod
    def get_classroom_schedule(db: Session, classroom_id: int) -> List[ScheduleModel]:
        """Get the complete schedule for a classroom."""
        return db.query(ScheduleModel).filter(ScheduleModel.classroom_id == classroom_id).all()
    
    @staticmethod
    def get_course_schedule(db: Session, course_id: int) -> List[ScheduleModel]:
        """Get the complete schedule for a course."""
        return db.query(ScheduleModel).filter(ScheduleModel.course_id == course_id).all()
    
    @staticmethod
    def validate_course_scheduling(db: Session, course_id: int) -> bool:
        """
        Validate that a course is properly scheduled according to its weekly hours.
        - 3-hour courses should have one block
        - 4-hour courses should have two 2-hour blocks on different days
        """
        course = db.query(CourseModel).filter(CourseModel.id == course_id).first()

        if not course:
            raise ValueError(f"Course with ID {course_id} not found")

        schedules = db.query(ScheduleModel).filter(ScheduleModel.course_id == course_id).all()
        
        total_hours = sum((s.end_time.hour - s.start_time.hour) + 
                         (s.end_time.minute - s.start_time.minute) / 60 
                         for s in schedules)
        
        # Check if total scheduled hours match course weekly hours
        if total_hours != course.weekly_hours:
            return False
        
        # For 4-hour courses, check if they're split into two blocks on different days
        if course.weekly_hours == 4:
            # Get unique days
            days = set(s.weekday for s in schedules)
            # Check if there are at least 2 different days
            if len(days) < 2:
                return False
            
            # Check if each block is 2 hours
            for schedule in schedules:
                hours = (schedule.end_time.hour - schedule.start_time.hour) + \
                       (schedule.end_time.minute - schedule.start_time.minute) / 60
                if hours != 2:
                    return False
        
        return True
