import dearpygui.dearpygui as dpg
import dearpygui.dearpygui as dpg
from datetime import time
from session import get_db
from services import SchedulerService
from models import WeekDay

# Placeholders for external db session and service, to be assigned before use
db = get_db()
scheduler_service = SchedulerService()

def show_message(message, color=(255, 255, 255)):
    dpg.set_value("output_text", message)
    dpg.configure_item("output_text", color=color)

def get_classrooms():
    session = next(get_db())
    try:
        return scheduler_service.get_classrooms(session)
    finally:
        session.close()

def get_schedules():
    session = next(get_db())
    try:
        return scheduler_service.get_schedules(session)
    finally:
        session.close()

def get_classroom_callback():
    session = next(get_db())
    classroom_id = dpg.get_value("classroom_id")
    try:
        classroom = scheduler_service.get_classroom_by_id(session, classroom_id)
        dpg.set_value("classroom_name", classroom.name)
        dpg.set_value("has_equipment", classroom.has_equipment)
        dpg.set_value("capacity", classroom.capacity)
    except Exception as e:
        print(e)
        show_message(str(e), (255, 0, 0))
    finally:
        session.close()

def add_classroom_callback():
    name = dpg.get_value("classroom_name")
    has_equipment = dpg.get_value("has_equipment")
    capacity = dpg.get_value("capacity")
    session = next(get_db())
    try:
        classroom = scheduler_service.add_classroom(session, name, has_equipment, capacity)
        show_message(f"Added Classroom: {classroom.name} (ID: {classroom.id})", (0, 255, 0))
        update_classroom_table()
    except Exception as e:
        print(e)
        show_message(str(e), (255, 0, 0))
    finally:
        session.close()

def update_classroom_callback():
    classroom_id = dpg.get_value("classroom_id")
    name = dpg.get_value("classroom_name")
    has_equipment = dpg.get_value("has_equipment")
    capacity = dpg.get_value("capacity")
    session = next(get_db())
    try:
        scheduler_service.update_classroom(session, classroom_id, name, has_equipment, capacity)
        show_message(f"Updated Classroom", (0, 255, 0))
        update_classroom_table()
    except Exception as e:
        print(e)
        show_message(str(e), (255, 0, 0))
    finally:
        session.close()

def delete_classroom_callback():
    classroom_id = dpg.get_value("classroom_id")
    session = next(get_db())
    try:
        scheduler_service.delete_classroom(session, classroom_id)
        show_message(f"Deleted Classroom", (0, 255, 0))
        update_classroom_table()
    except Exception as e:
        print(e)
        show_message(str(e), (255, 0, 0))
    finally:
        session.close()

def get_courses():
    session = next(get_db())
    try:
        return scheduler_service.get_courses(session)
    finally:
        session.close()

def get_course_callback():
    session = next(get_db())
    course_id = dpg.get_value("course_id")
    try:
        course = scheduler_service.get_course_by_id(session, course_id)
        dpg.set_value("course_code", course.code)
        dpg.set_value("course_name", course.name)
        dpg.set_value("weekly_hours", course.weekly_hours)
        dpg.set_value("requires_equipment", course.requires_equipment)
    except Exception as e:
        print(e)
        show_message(str(e), (255, 0, 0))
    finally:
        session.close()

def add_course_callback():
    code = dpg.get_value("course_code")
    name = dpg.get_value("course_name")
    weekly_hours = dpg.get_value("weekly_hours")
    requires_equipment = dpg.get_value("requires_equipment")
    session = next(get_db())
    try:
        course = scheduler_service.add_course(session, code, name, weekly_hours, requires_equipment)
        show_message(f"Added Course: {course.name} (ID: {course.id})", (0, 255, 0))
        update_course_table()
    except Exception as e:
        print(e)
        show_message(str(e), (255, 0, 0))
    finally:
        session.close()

def update_course_callback():
    course_id = dpg.get_value("course_id")
    code = dpg.get_value("course_code")
    name = dpg.get_value("course_name")
    weekly_hours = dpg.get_value("weekly_hours")
    requires_equipment = dpg.get_value("requires_equipment")
    session = next(get_db())
    try:
        scheduler_service.update_course(session, course_id, code, name, weekly_hours, requires_equipment)
        show_message(f"Updated Course", (0, 255, 0))
        update_course_table()
    except Exception as e:
        print(e)
        show_message(str(e), (255, 0, 0))
    finally:
        session.close()

def delete_course_callback():
    course_id = dpg.get_value("course_id")
    session = next(get_db())
    try:
        scheduler_service.delete_course(session, course_id)
        show_message(f"Deleted Course", (0, 255, 0))
        update_course_table()
    except Exception as e:
        print(e)
        show_message(str(e), (255, 0, 0))
    finally:
        session.close()

def get_professors():
    session = next(get_db())
    try:
        return scheduler_service.get_professors(session)
    finally:
        session.close()

def get_professor_callback():
    session = next(get_db())
    prof_id = dpg.get_value("prof_id")
    try:
        prof = scheduler_service.get_professor_by_id(session, prof_id)
        dpg.set_value("prof_name", prof.name)
        dpg.set_value("prof_doc_id", prof.document_id)
    except Exception as e:
        print(e)
        show_message(str(e), (255, 0, 0))
    finally:
        session.close()

def add_professor_callback():
    name = dpg.get_value("prof_name")
    doc_id = dpg.get_value("prof_doc_id")
    session = next(get_db())
    try:
        prof = scheduler_service.add_professor(session, name, doc_id)
        show_message(f"Added Professor: {prof.name} (ID: {prof.id})", (0, 255, 0))
        update_prof_table()
    except Exception as e:
        print(e)
        show_message(str(e), (255, 0, 0))
    finally:
        session.close()

def update_professor_callback():
    prof_id = dpg.get_value("prof_id")
    name = dpg.get_value("prof_name")
    doc_id = dpg.get_value("prof_doc_id")
    session = next(get_db())
    try:
        scheduler_service.update_professor(session, prof_id, name, doc_id)
        show_message(f"Updated Professor", (0, 255, 0))
        update_prof_table()
    except Exception as e:
        print(e)
        show_message(str(e), (255, 0, 0))
    finally:
        session.close()

def delete_professor_callback():
    prof_id = dpg.get_value("prof_id")
    session = next(get_db())
    try:
        scheduler_service.delete_professor(session, prof_id)
        show_message(f"Deleted Professor", (0, 255, 0))
        update_prof_table()
    except Exception as e:
        print(e)
        show_message(str(e), (255, 0, 0))
    finally:
        session.close()

def assign_course_callback():
    session = next(get_db())
    try:
        prof_id = int(dpg.get_value("assign_professor_id"))
        course_id = int(dpg.get_value("assign_course_id"))
        scheduler_service.assign_course_to_professor(session, prof_id, course_id)
        show_message(f"Assigned Course {course_id} to Professor {prof_id}", (0, 255, 0))
    except Exception as e:
        show_message(str(e), (255, 0, 0))
    finally:
        session.close()

def remove_course_callback():
    session = next(get_db())
    try:
        prof_id = int(dpg.get_value("assign_professor_id"))
        course_id = int(dpg.get_value("assign_course_id"))
        scheduler_service.remove_course_from_professor(session, prof_id, course_id)
        show_message(f"Removed Course {course_id} from Professor {prof_id}", (0, 255, 0))
    except Exception as e:
        show_message(str(e), (255, 0, 0))
    finally:
        session.close()

def schedule_session_callback():
    session = next(get_db())
    try:
        course_id = int(dpg.get_value("schedule_course_id"))
        prof_id = int(dpg.get_value("schedule_professor_id"))
        classroom_id = int(dpg.get_value("schedule_classroom_id"))
        weekday = dpg.get_value("schedule_weekday")
        start_h = int(dpg.get_value("schedule_start_hour"))
        start_m = int(dpg.get_value("schedule_start_minute"))
        end_h = int(dpg.get_value("schedule_end_hour"))
        end_m = int(dpg.get_value("schedule_end_minute"))

        start_time_obj = time(start_h, start_m)
        end_time_obj = time(end_h, end_m)

        weekday_enum = None
        for day in WeekDay:
            if day.value == weekday:
                weekday_enum = day
                break
        if not weekday_enum:
            raise ValueError("Invalid weekday selected")

        schedule = scheduler_service.schedule_course_session(
            session,
            course_id,
            prof_id,
            classroom_id,
            weekday_enum,
            start_time_obj,
            end_time_obj
        )
        show_message(f"Scheduled session ID {schedule.id}", (0, 255, 0))
        update_schedule_table()
    except Exception as e:
        show_message(str(e), (255, 0, 0))
    finally:
        session.close()

def validate_course_callback():
    session = next(get_db())
    try:
        course_id = int(dpg.get_value("validate_course_id"))
        valid = scheduler_service.validate_course_scheduling(session, course_id)
        if valid:
            show_message("Course scheduling is valid!", (0, 255, 0))
        else:
            show_message("Course scheduling is NOT valid!", (255, 255, 0))
    except Exception as e:
        show_message(str(e), (255, 0, 0))
    finally:
        session.close()

def update_prof_table():
    for tag in dpg.get_item_children("prof_table")[1]:
        dpg.delete_item(tag)
    professors = get_professors()
    for professor in professors:
        with dpg.table_row(parent="prof_table"):
            dpg.add_text(f"{professor.id}")
            dpg.add_text(f"{professor.name}")
            dpg.add_text(f"{professor.document_id}")

def update_course_table():
    """Refresh the course table with the latest data."""
    for tag in dpg.get_item_children("course_table")[1]:
        dpg.delete_item(tag)
    courses = get_courses()
    for course in courses:
        with dpg.table_row(parent="course_table"):
            dpg.add_text(f"{course.id}")
            dpg.add_text(f"{course.code}")
            dpg.add_text(f"{course.name}")
            dpg.add_text(f"{course.weekly_hours}")
            dpg.add_text(f"{'Yes' if course.requires_equipment else 'No'}")

def update_classroom_table():
    """Refresh the classroom table with the latest data."""
    for tag in dpg.get_item_children("classroom_table")[1]:
        dpg.delete_item(tag)
    classrooms = get_classrooms()
    for classroom in classrooms:
        with dpg.table_row(parent="classroom_table"):
            dpg.add_text(f"{classroom.id}")
            dpg.add_text(f"{classroom.name}")
            dpg.add_text(f"{'Yes' if classroom.has_equipment else 'No'}")
            dpg.add_text(f"{classroom.capacity}")

def update_schedule_table():
    """Refresh the schedule table with the latest data."""
    for tag in dpg.get_item_children("schedule_table")[1]:
        dpg.delete_item(tag)
    schedules = get_schedules()
    for schedule in schedules:
        with dpg.table_row(parent="schedule_table"):
            dpg.add_text(f"{schedule.id}")
            dpg.add_text(f"{schedule.course_id}")
            dpg.add_text(f"{schedule.professor_id}")
            dpg.add_text(f"{schedule.classroom_id}")
            dpg.add_text(f"{schedule.weekday}")
            dpg.add_text(f"{schedule.start_time}")
            dpg.add_text(f"{schedule.end_time}")

dpg.create_context()
dpg.create_viewport(title='Scheduler GUI', width=800, height=600)

with dpg.window(label="Scheduler", width=800, height=600):
    with dpg.tab_bar():
        with dpg.tab(label="Professors"):
            with dpg.group(horizontal=True):
                with dpg.table(tag="prof_table", header_row=True, row_background=True,
                             borders_innerH=True, borders_outerH=True, borders_innerV=True,
                             borders_outerV=True, width=300, height=200):
                    dpg.add_table_column(label="ID")
                    dpg.add_table_column(label="Name")
                    dpg.add_table_column(label="Document ID")

                    update_prof_table()
                
                with dpg.group(horizontal=False):
                    with dpg.group(horizontal=True):
                        with dpg.group(horizontal=False):
                            dpg.add_text("Search ID")
                            dpg.add_input_text(tag="prof_id", hint="Enter ID", width=185)
                        with dpg.group(horizontal=False):
                            dpg.add_spacer(height=19)
                            dpg.add_button(label="Search", callback=get_professor_callback)

                    dpg.add_text("Professor's Name")
                    dpg.add_input_text(tag="prof_name", hint="Professor's Name", width=-1)

                    dpg.add_text("Document ID")
                    dpg.add_input_text(tag="prof_doc_id", hint="Document ID", width=-1)
                    dpg.add_spacer(height=2)
                    
                    with dpg.group(horizontal=True):
                        dpg.add_button(label="Add", callback=add_professor_callback)
                        dpg.add_button(label="Update", callback=update_professor_callback)
                        dpg.add_button(label="Delete", callback=delete_professor_callback)

        with dpg.tab(label="Courses"):
            with dpg.group(horizontal=True):
                with dpg.table(tag="course_table", header_row=True, row_background=True,
                             borders_innerH=True, borders_outerH=True, borders_innerV=True,
                             borders_outerV=True, width=500, height=200):
                    dpg.add_table_column(label="ID")
                    dpg.add_table_column(label="Code")
                    dpg.add_table_column(label="Name")
                    dpg.add_table_column(label="Weekly Hours")
                    dpg.add_table_column(label="Requires Equipment")

                    update_course_table()
                
                with dpg.group(horizontal=False):
                    with dpg.group(horizontal=True):
                        with dpg.group(horizontal=False):
                            dpg.add_text("Search Course ID")
                            dpg.add_input_text(tag="course_id", hint="Enter Course ID", width=185)
                        with dpg.group(horizontal=False):
                            dpg.add_spacer(height=19)
                            dpg.add_button(label="Search", callback=get_course_callback)

                    dpg.add_text("Course Code")
                    dpg.add_input_text(tag="course_code", hint="Course Code", width=-1)

                    dpg.add_text("Course Name")
                    dpg.add_input_text(tag="course_name", hint="Course Name", width=-1)

                    dpg.add_text("Weekly Hours")
                    dpg.add_input_int(tag="weekly_hours", default_value=4, min_value=1, max_value=10)

                    dpg.add_text("Requires Equipment")
                    dpg.add_checkbox(tag="requires_equipment")

                    dpg.add_spacer(height=2)
                    
                    with dpg.group(horizontal=True):
                        dpg.add_button(label="Add", callback=add_course_callback)
                        dpg.add_button(label="Update", callback=update_course_callback)
                        dpg.add_button(label="Delete", callback=delete_course_callback)
        
        with dpg.tab(label="Classrooms"):
            with dpg.group(horizontal=True):
                with dpg.table(tag="classroom_table", header_row=True, row_background=True,
                             borders_innerH=True, borders_outerH=True, borders_innerV=True,
                             borders_outerV=True, width=500, height=200):
                    dpg.add_table_column(label="ID")
                    dpg.add_table_column(label="Name")
                    dpg.add_table_column(label="Has Equipment")
                    dpg.add_table_column(label="Capacity")

                    update_classroom_table()
                
                with dpg.group(horizontal=False):
                    with dpg.group(horizontal=True):
                        with dpg.group(horizontal=False):
                            dpg.add_text("Search Classroom ID")
                            dpg.add_input_text(tag="classroom_id", hint="Enter Classroom ID", width=185)
                        with dpg.group(horizontal=False):
                            dpg.add_spacer(height=19)
                            dpg.add_button(label="Search", callback=get_classroom_callback)

                    dpg.add_text("Classroom Name")
                    dpg.add_input_text(tag="classroom_name", hint="Classroom Name", width=-1)

                    dpg.add_text("Has Equipment")
                    dpg.add_checkbox(tag="has_equipment")

                    dpg.add_text("Capacity")
                    dpg.add_input_int(tag="capacity", default_value=30, min_value=1, max_value=200)

                    dpg.add_spacer(height=2)
                    
                    with dpg.group(horizontal=True):
                        dpg.add_button(label="Add", callback=add_classroom_callback)
                        dpg.add_button(label="Update", callback=update_classroom_callback)
                        dpg.add_button(label="Delete", callback=delete_classroom_callback)
        
        with dpg.tab(label="Assign Course"):
            dpg.add_input_int(label="Professor ID", tag="assign_professor_id")
            dpg.add_input_int(label="Course ID", tag="assign_course_id")
            with dpg.group(horizontal=True):
                dpg.add_button(label="Assign", callback=assign_course_callback)
                dpg.add_button(label="Remove", callback=remove_course_callback)
        
        with dpg.tab(label="Schedule Session"):
            with dpg.table(tag="schedule_table", header_row=True, row_background=True,
                         borders_innerH=True, borders_outerH=True, borders_innerV=True,
                         borders_outerV=True, width=500, height=200):

                dpg.add_table_column(label="ID")
                dpg.add_table_column(label="Course ID")
                dpg.add_table_column(label="Professor ID")
                dpg.add_table_column(label="Classroom ID")
                dpg.add_table_column(label="Weekday")
                dpg.add_table_column(label="Start Time")
                dpg.add_table_column(label="End Time")

                update_schedule_table()

            dpg.add_input_int(label="Course ID", tag="schedule_course_id")
            dpg.add_input_int(label="Professor ID", tag="schedule_professor_id")
            dpg.add_input_int(label="Classroom ID", tag="schedule_classroom_id")
            
            dpg.add_combo(label="Weekday", items=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], tag="schedule_weekday")
            
            dpg.add_text("Start Time")
            with dpg.group(horizontal=True):
                dpg.add_input_int(label="Hour", default_value=9, min_value=0, max_value=23, tag="schedule_start_hour", width=100)
                dpg.add_input_int(label="Minute", default_value=0, min_value=0, max_value=59, tag="schedule_start_minute", width=100)
            
            dpg.add_text("End Time")
            with dpg.group(horizontal=True):
                dpg.add_input_int(label="Hour", default_value=11, min_value=0, max_value=23, tag="schedule_end_hour", width=100)
                dpg.add_input_int(label="Minute", default_value=0, min_value=0, max_value=59, tag="schedule_end_minute", width=100)
            
            dpg.add_button(label="Schedule Session", callback=schedule_session_callback)
        
        with dpg.tab(label="Validate Schedule"):
            dpg.add_input_int(label="Course ID", tag="validate_course_id")
            dpg.add_button(label="Validate", callback=validate_course_callback)

    dpg.add_spacer(height=10)
    dpg.add_text("", tag="output_text")

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
