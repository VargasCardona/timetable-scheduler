import enum
import uuid
from datetime import time
from typing import List, Optional, Dict, Tuple
from sqlalchemy.orm import Session

from app.models.models import (
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
        professor = ProfessorModel(
            name=name,
            document_id=document_id
        )
        db.add(professor)
        db.commit()
        db.refresh(professor)
        return professor
    
    @staticmethod
    def get_professor_by_document(db: Session, document_id: str) -> Optional[ProfessorModel]:
        """Get a professor by their document ID."""
        return db.query(ProfessorModel).filter(ProfessorModel.document_id == document_id).first()
    
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
    def add_course(
        db: Session, 
        code: str, 
        name: str, 
        weekly_hours: int = 4, 
        requires_equipment: bool = False
    ) -> CourseModel:
        """Add a new course to the database."""
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
    def assign_course_to_professor(
        db: Session, 
        professor_id: int, 
        course_id: int
    ) -> None:
        """Assign a course to a professor."""
        professor = db.query(ProfessorModel).filter(ProfessorModel.id == professor_id).first()
        course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
        
        if professor and course:
            # Check if professor already has 6 courses
            if len(professor.courses) >= 6:
                raise ValueError("Professor already has the maximum of 6 courses assigned")
                
            professor.courses.append(course)
            db.commit()
    
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
        professor = db.query(ProfessorModel).filter(ProfessorModel.uuid == professor_id).first()
        course = db.query(CourseModel).filter(CourseModel.uuid == course_id).first()
        
        if course not in professor.courses:
            raise ValueError(f"Professor {professor.name} is not assigned to course {course.name}")
        
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
        classroom = db.query(ClassroomModel).filter(ClassroomModel.uuid == classroom_id).first()
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
        course = db.query(CourseModel).filter(CourseModel.uuid == course_id).first()
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