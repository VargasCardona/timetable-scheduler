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
    except Exception as e:
        print(e)
        show_message(str(e), (255, 0, 0))
    finally:
        session.close()

def update_professor_callback():
    proff_id = dpg.get_value("prof_id")
    name = dpg.get_value("prof_name")
    doc_id = dpg.get_value("prof_doc_id")
    session = next(get_db())
    try:
        prof = scheduler_service.update_professor(session,proff_id, name, doc_id)
        show_message(f"Updated Professor", (0, 255, 0))
    except Exception as e:
        print(e)
        show_message(str(e), (255, 0, 0))
    finally:
        session.close()

def delete_professor_callback():
    proff_id = dpg.get_value("prof_id")
    session = next(get_db())
    try:
        prof = scheduler_service.delete_professor(session, proff_id)
        show_message(f"Deleted Professor", (0, 255, 0))
    except Exception as e:
        print(e)
        show_message(str(e), (255, 0, 0))
    finally:
        session.close()

def add_course_callback():
    code = dpg.get_value("course_code")
    name = dpg.get_value("course_name")
    weekly_hours = dpg.get_value("course_weekly_hours")
    requires_eq = dpg.get_value("course_requires_eq")
    session = next(get_db())
    try:
        course = scheduler_service.add_course(session, code, name, int(weekly_hours), requires_eq)
        show_message(f"Added Course: {course.name} (ID: {course.id})", (0, 255, 0))
    except Exception as e:
        show_message(str(e), (255, 0, 0))
    finally:
        session.close()

def add_classroom_callback():
    name = dpg.get_value("classroom_name")
    has_eq = dpg.get_value("classroom_has_eq")
    capacity = dpg.get_value("classroom_capacity")
    session = next(get_db())
    try:
        classroom = scheduler_service.add_classroom(session, name, has_eq, int(capacity))
        show_message(f"Added Classroom: {classroom.name} (ID: {classroom.id})", (0, 255, 0))
    except Exception as e:
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


dpg.create_context()
dpg.create_viewport(title='Scheduler GUI', width=700, height=500)

with dpg.window(label="Scheduler", width=700, height=500):
    with dpg.tab_bar():
        
        with dpg.tab(label="Add Professor"):
         with dpg.group(horizontal=True):
            with dpg.table(tag="contacts_table", header_row=True, row_background=True,
                               borders_innerH=True, borders_outerH=True, borders_innerV=True,
                               borders_outerV=True, width=300, height=200):
                dpg.add_table_column(label="ID")
                dpg.add_table_column(label="Name")
                dpg.add_table_column(label="Document ID")

                professors = get_professors()
                
                for professor in professors:
                    with dpg.table_row():
                        dpg.add_text(f"{professor.id}")
                        dpg.add_text(f"{professor.name}")
                        dpg.add_text(f"{professor.document_id}")
            with dpg.group(horizontal=False):
                      with dpg.group(horizontal=True):
                          with dpg.group(horizontal=False):
                            dpg.add_text("Buscar ID")
                            dpg.add_input_text(tag="prof_id", hint="Ingrese un ID", width=185)
                          with dpg.group(horizontal=False):
                            dpg.add_spacer(height=19)
                            dpg.add_button(label="Consultar", callback=get_professor_callback)

                      dpg.add_text("Professor's Name")
                      dpg.add_input_text(tag="prof_name", hint="Professor's Name", width=-1)

                      dpg.add_text("Document ID")
                      dpg.add_input_text(tag="prof_doc_id", hint="Document ID", width=-1)
                      dpg.add_spacer(height=2)
                      
                      with dpg.group(horizontal=True):
                       dpg.add_button(label="Register", callback=add_professor_callback)
                       dpg.add_button(label="Edit", callback=update_professor_callback)
                       dpg.add_button(label="Delete Professor", callback=delete_professor_callback)

        with dpg.tab(label="Add Course"):
            dpg.add_input_text(label="Code", tag="course_code")
            dpg.add_input_text(label="Name", tag="course_name")
            dpg.add_input_int(label="Weekly Hours", default_value=4, min_value=1, max_value=10, tag="course_weekly_hours")
            dpg.add_checkbox(label="Requires Equipment", tag="course_requires_eq")
            dpg.add_button(label="Add Course", callback=add_course_callback)
        
        with dpg.tab(label="Add Classroom"):
            dpg.add_input_text(label="Name", tag="classroom_name")
            dpg.add_checkbox(label="Has Equipment", tag="classroom_has_eq")
            dpg.add_input_int(label="Capacity", default_value=30, min_value=1, max_value=200, tag="classroom_capacity")
            dpg.add_button(label="Add Classroom", callback=add_classroom_callback)
        
        with dpg.tab(label="Assign Course to Professor"):
            dpg.add_input_int(label="Professor ID", tag="assign_professor_id")
            dpg.add_input_int(label="Course ID", tag="assign_course_id")
            dpg.add_button(label="Assign", callback=assign_course_callback)
        
        with dpg.tab(label="Schedule Course Session"):
            dpg.add_input_int(label="Course ID", tag="schedule_course_id")
            dpg.add_input_int(label="Professor ID", tag="schedule_professor_id")
            dpg.add_input_int(label="Classroom ID", tag="schedule_classroom_id")
            
            dpg.add_combo(label="Weekday", items=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], tag="schedule_weekday")
            
            dpg.add_text("Start Time")
            dpg.add_input_int(label="Hour", default_value=9, min_value=0, max_value=23, tag="schedule_start_hour")
            dpg.add_input_int(label="Minute", default_value=0, min_value=0, max_value=59, tag="schedule_start_minute")
            
            dpg.add_text("End Time")
            dpg.add_input_int(label="Hour", default_value=11, min_value=0, max_value=23, tag="schedule_end_hour")
            dpg.add_input_int(label="Minute", default_value=0, min_value=0, max_value=59, tag="schedule_end_minute")
            
            dpg.add_button(label="Schedule Session", callback=schedule_session_callback)
        
        with dpg.tab(label="Validate Course Schedule"):
            dpg.add_input_int(label="Course ID", tag="validate_course_id")
            dpg.add_button(label="Validate", callback=validate_course_callback)

    dpg.add_spacer(height=10)
    dpg.add_text("", tag="output_text")

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
