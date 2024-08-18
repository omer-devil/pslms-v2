"""
Flask Application Documentation

This Flask application provides a web interface for managing a school system.
It includes functionality for user authentication, user roles (admin, teacher, student, parent),
viewing profiles, recording attendance, managing assessments, adding students, parents, teachers,
viewing and updating user information, and managing resources.

Routes:
    /profile: View user profile based on user role.
    /student_course_info: View courses information for students.
    /Student_Assessment: View assessment information for students.
    /get_student_attendance_info: Get attendance information for students.
    /record_attendance/<grade>/<section>: Record attendance for students.
    /assessment_insert/<grade>/<section>: Insert assessment data for students.
    /Teacher_course_info: View course information for teachers.
    /admin_page: View admin page (placeholder).
    /add_student_and_parent: Add student and parent information.
    /admin_add_teacher: Add teacher information (placeholder).
    /admin_get_user_info/<user_role>: Get user information for admins.
    /admin_get_student/<grade>/<section>: Get student information for admins.
    /admin_get_attendance_and_assesement/<grade>/<section>/<get_info_from>: Get attendancen and assessment information for admins.
    /admin_update_teacher_and_parent/<user_role>/<user_ID>: Update teacher and parent information.
    /get_resource: Get resource information.
    /add_resorce: Add resource.
    /Successful/<message>: Successful operation message page.
    /403: view.unauthorized access page.
    /Error/<message>: Error page.

Blueprints:
    view: Blueprint for handling views.

Imports:
    Flask: Micro web framework for Python.
    request: Module to handle HTTP requests.
    session: Module for session management.
    render_template: Function to render templates.
    redirect: Function to redirect requests.
    Blueprint: Class for creating Blueprint objects.
    url_for: Function to build URLs.
    g: Global object for request-specific data storage.
    db_manager: Custom module for database management.
    Settings: Custom module for application settings.
    os: Module for interacting with the operating system.

Globals:
    var: Instance of Settings class for application variables.
    View: Blueprint object for view routes.

Functions:
    profile(): View user profile based on user role.
    student_info(): View courses information for students.
    student_assessment(): View assessment information for students.
    get_student_attendance_info(): Get attendance information for students.
    record_attendance(grade, section): Record attendance for students.
    assessment_insert(grade, section): Insert assessment data for students.
    teacher_course_info(): View course information for teachers.
    admin_page(): View admin page (placeholder).
    add_student_and_parent(): Add student and parent information.
    add_teacher(): Add teacher information (placeholder).
    admin_get_user_info(user_role): Get user information for admins.
    admin_get_student(grade, section): Get student information for admins.
    admin_get_attendance_and_assessment(grade, section, get_info_from): Get attendance and assessment information for admins.
    admin_update_teacher_and_parent(user_role, user_ID): Update teacher and parent information.
    get_resource(): Get resource information.
    add_resource(): Add resource.
    Successful(message): Successful operation message page.
    view.unauthorized(): view.unauthorized access page.
    error(message): Error page.
"""

from flask import Flask,request,session,render_template,redirect,Blueprint,url_for,g
import db_manager as db
from settings import Settings
from datetime import datetime
import random
import string
import os

#if os.path.isfile(path) to remove file = os.remove(file)
def ids():
    RABDOM_ID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    RABDOM_ID_3 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    RABDOM_ID_2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return RABDOM_ID,RABDOM_ID_2,RABDOM_ID_3

var = Settings()
var.variables()

View = Blueprint("view",__name__,  static_folder="static" , static_url_path="/static" ,template_folder="templates")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in var.ALLOWED_EXTENSIONS

#index route
@View.route("/")
def index():
    return render_template("index.html")

@View.route("/devlopers")
def dev():
    return render_template("dev.html")

# ################################# [all profile] #######################################
@View.route("/profile", methods=["GET"])
def profile():
    if "userID" in session:
        userID = session["userID"]
        userName = session["user"]
        role =  session["role"]
        page = var.profiles[role]

        if role == "student":
            with db.connect() as conn:
                print(userID,db.Students_info(conn,"student",userID,flage=False))
                if len(db.Students_info(conn,"student",userID,flage=False)) > 0:
                    profile = db.Students_info(conn,"student",userID,flage=False)[0]
                    print(profile)
                    path = var.GET_UPLOAD_PROFILE + profile[-4]
                    grade = var.ID_GRADE[profile[2]]
                    section = db.get_section_by_id(int(profile[3]))
                    data = [userName,section,grade, path]
                    print(data)
                    return render_template(page,data=data)
                else:
                    return redirect(url_for("login.user_login"))
        elif role == "parent":
            with db.connect() as conn:
                if len(db.Parents_info(conn,"id",userID,flage=False)) > 0:
                    profile = db.Parents_info(
                        conn,"id",userID,flage=False
                    )[0]
                    children = db.Students_info(
                        conn,SearchBy="parent",Search=profile[0],flage=False
                    )
                    if len(children)>0:
                        session["children"] = children
                        info = [profile,children]
                    else:
                        info = [profile,"Thir is no children info"]
            return render_template("parent/parent_profile.html",data=info)
        elif role == "teacher":
            with db.connect() as conn:
                profile = db.Techears_info(
                    conn,"user",userID,flage=False
                )
                if len(profile) > 0:
                    section_and_grade = db.Section_info(conn)
                    if len(section_and_grade) == 0:
                        section_and_grade = "no"
                    profile = profile[0]
                    profile_pic = profile[7]
                    path = var.GET_UPLOAD_PROFILE + profile_pic
                    print(db.Section_info(conn))
                    data = [userName,path,var.ID_COURSE[profile[1]],db.Section_info(conn)]
                    session["GradeID"] = profile[6]
                    session["course"] = profile[1]
            return render_template(page,data=data)
        else:
            return redirect(url_for("view.unauthorized"))
    else:
        return redirect(url_for("login.user_login"))
# ####################################### [student pages] ###################################
@View.route("/student_course_info")
def student_info():
    if "userID" in session:
        userID = session["userID"]
        role =  session["role"]
        if role == "student":
            with db.connect() as conn:
                all = var.MAPED_KEY[2]
                studentInfo = db.Students_info(
                    conn,role,userID,False
                )[0]
                GradeID = studentInfo[2]
                if GradeID in var.GENERAL_ID[var.MAPED_KEY[0]]:
                    mk = var.MAPED_KEY[0]
                elif GradeID in var.GENERAL_ID[var.MAPED_KEY[1]]:
                    mk = var.MAPED_KEY[1]
                elif GradeID in var.GENERAL_ID[var.MAPED_KEY[2]]:
                    mk = var.MAPED_KEY[2]
                courses = []
                coursesID = var.COURSE_TAKE
                for key,item in coursesID.items():
                    if GradeID in item:
                        courses.append(key)
                Course_info = []
                Course_info.append(session["user"])
                for ID in courses:
                    name_courses = db.Course_info(conn,ID)[0][1]
                    #GradeID map id
                    teacher_info = db.Techears_info(
                        conn,"course",ID=ID,MapID=mk,flage=False
                    )
                    print("%"*7,teacher_info)
                    if len(teacher_info) == 0:
                        teacher_info = db.Techears_info(
                            conn, "course",ID=ID, MapID=all, flage=False
                        )
                        print("-" * 7, teacher_info)
                        if len(teacher_info) > 0:
                            teacher_info = teacher_info[0]
                            teacher_name = " ".join(teacher_info[2:4])
                            print("#" * 10, teacher_name)
                            teacher_phone_number = teacher_info[-1]
                            teacher_name_and_phone = [teacher_name, teacher_phone_number]
                            Course_info.append([name_courses, teacher_name_and_phone])
                    else:
                        teacher_info = teacher_info[0]
                        teacher_name = " ".join(teacher_info[2:4])
                        print("#"*10,teacher_name)
                        teacher_phone_number = teacher_info[-1]
                        teacher_name_and_phone = [teacher_name,teacher_phone_number]
                        Course_info.append([name_courses,teacher_name_and_phone])
            return render_template("student/student_course_info.html",data=Course_info)
        else:
            return redirect(url_for("view.unauthorized"))
    else:
        return redirect(url_for("login.user_login"))

@View.route("/Student_Assessment")
def student_assessment():
    if "userID" in session:
        userID = session["userID"]
        role =  session["role"]
        if role == "student":
            with db.connect() as conn:
                courses = var.COURSESID
                filter_assessment1 = []
                for cours in courses:
                    assessments = db.Assessements_ifo(
                        conn,userID,False,"student",sem="s1",CourseID=cours
                    )
                    print(assessments)
                    if len(assessments) > 0:
                        filter_assessment1.append([var.ID_COURSE[cours],assessments])
                if len(filter_assessment1) == 0:
                    filter_assessment1 = "Empty no data yet!"
                filter_assessment2 = []
                for cours in courses:
                    assessments = db.Assessements_ifo(
                        conn,userID,False,"student",sem="s2",CourseID=cours
                    )
                    if len(assessments) > 0:
                        filter_assessment2.append([var.ID_COURSE[cours], assessments])
                if len(filter_assessment2) == 0:
                    filter_assessment2 = "Empty no data yet!"
            Student_assessment_info = [
                session["user"], filter_assessment1,filter_assessment2
            ]
            print(Student_assessment_info)
            return render_template("student/student_assessment.html",data=Student_assessment_info)
        else:
            return redirect(url_for("view.unauthorized"))
    else:
        return redirect(url_for("login.user_login"))

# attendance
@View.route("/get_student_attendance_info")
def get_student_attendance_info():
    if "userID" in session:
        userID = session["userID"]
        role =  session["role"]
        userName = session["user"]
        atendance = []
        with db.connect() as conn:
            if role == "student":
                attendances_info = db.Attendace_info(
                    conn,userID,role,flage=False
                )
                if len(attendances_info) > 0:
                    print(attendances_info)
                    for attendance_info in attendances_info:
                        statusID = attendance_info[-1]
                        status = var.ATTENDANCE_STATUSE[statusID]
                        date = attendance_info[-2].strftime('%m/%d/%Y')
                        teacher_info = db.Techears_info(
                            conn,SeasrchBy="user",ID=attendance_info[1],flage=False
                        )[0]
                        course = var.ID_COURSE[teacher_info[1]]
                        atendance.append([course,status,date])
                atendance.append(userName)
                return render_template("student/attendace_info.html",data=atendance)
            else:
                return redirect(url_for("view.unauthorized"))
    else:
        return redirect(url_for("login.user_login"))

# ##################################################### [parent] ##################################################

@View.route("/parent_get_student_cource/<studentID>")
def parent_get_student_cource(studentID):
    if "userID" in session:
        userID = session["userID"]
        role = session["role"]
        userName = session["user"]
        with db.connect() as conn:
            if role == "parent":
                with db.connect() as conn:
                    all = var.MAPED_KEY[2]
                    studentInfo = db.Students_info(
                        conn, role, studentID, False
                    )[0]
                    GradeID = studentInfo[2]
                    if GradeID in var.GENERAL_ID[var.MAPED_KEY[0]]:
                        mk = var.MAPED_KEY[0]
                    elif GradeID in var.GENERAL_ID[var.MAPED_KEY[1]]:
                        mk = var.MAPED_KEY[1]
                    elif GradeID in var.GENERAL_ID[var.MAPED_KEY[2]]:
                        mk = var.MAPED_KEY[2]
                    courses = []
                    coursesID = var.COURSE_TAKE
                    for key, item in coursesID.items():
                        if GradeID in item:
                            courses.append(key)
                    Course_info = []
                    Course_info.append(" ".join(studentInfo[4:6]))
                    for ID in courses:
                        name_courses = db.Course_info(conn, ID)[0][1]
                        # GradeID map id
                        teacher_info = db.Techears_info(
                            conn, "course", ID=ID,
                            MapID=mk, flage=False
                        )
                        print("%" * 7, teacher_info)
                        if len(teacher_info) == 0:
                            teacher_info = db.Techears_info(
                                conn, "course", ID=ID, MapID=all, flage=False
                            )
                            print("-" * 7, teacher_info)
                            if len(teacher_info) > 0:
                                teacher_info = teacher_info[0]
                                teacher_name = " ".join(teacher_info[2:4])
                                print("#" * 10, teacher_name)
                                teacher_phone_number = teacher_info[-1]
                                teacher_name_and_phone = [
                                    teacher_name, teacher_phone_number
                                ]
                                Course_info.append([name_courses, teacher_name_and_phone])
                        else:
                            teacher_info = teacher_info[0]
                            teacher_name = " ".join(teacher_info[2:4])
                            print("#" * 10, teacher_name)
                            teacher_phone_number = teacher_info[-1]
                            teacher_name_and_phone = [teacher_name, teacher_phone_number]
                            Course_info.append([name_courses, teacher_name_and_phone])
                return render_template("parent/student_course_info.html", data=Course_info)
            else:
                return redirect(url_for("view.unauthorized"))
    else:
        return redirect(url_for("login.user_login"))

@View.route("/parent_get_student_assessment/<ID>")
def parent_get_student_assessment(ID):
    if "userID" in session:
        userID = session["userID"]
        role = session["role"]
        userName = session["user"]
        if role == "parent":
            with db.connect() as conn:
                student_info = db.Students_info(conn,SearchBy="student",Search=ID,flage=False)
                if len(student_info) > 0:
                    student_name = " ".join(student_info[4:6])
                    courses = var.COURSESID
                    filter_assessment1 = []
                    for cours in courses:
                        assessments = db.Assessements_ifo(
                            conn,ID,False,"student",
                            sem="s1",CourseID=cours
                        )
                        print(assessments)
                        if len(assessments) > 0:
                            filter_assessment1.append([var.ID_COURSE[cours],assessments])
                    if len(filter_assessment1) == 0:
                        filter_assessment1 = "Empty no data yet!"
                    filter_assessment2 = []
                    for cours in courses:
                        assessments = db.Assessements_ifo(
                            conn,ID,False,"student",
                            sem="s2",CourseID=cours
                        )
                        if len(assessments) > 0:
                            filter_assessment2.append([var.ID_COURSE[cours], assessments])
                    if len(filter_assessment2) == 0:
                        filter_assessment2 = "Empty no data yet!"
                    Student_assessment_info = [
                        student_name, filter_assessment1, filter_assessment2
                    ]
                    print(Student_assessment_info)
                    return render_template("parent/student_assessment.html", data=Student_assessment_info)
                else:
                    message = "In valid user ID(not allowed)"
                    return redirect(url_for("view.error", message=message))
        else:
            return redirect(url_for("view.unauthorized"))
    else:
        return redirect(url_for("login.user_login"))

@View.route("/parent_get_student_attendance/<ID>")
def parent_get_student_attendance(ID):
    if "userID" in session:
        userID = session["userID"]
        role =  session["role"]
        userName = session["user"]
        if role == "parent":
            student_info = db.Students_info(conn,SearchBy="student",Search=ID,flage=False)
            attendances_info = db.Attendace_info(conn, userID, role, flage=False)
            if len(attendances_info) > 0 and student_info > 0:
                studentName = " ".join(student_info[4:6])
                for attendance_info in attendances_info:
                    status = var.ATTENDANCE_STATUSE[attendance_info[-1]]
                    date = attendance_info[-2].strftime('%m/%d/%Y')
                    teacher_info = db.Techears_info(
                        conn, SeasrchBy="user",
                        ID=attendance_info[1],flage=False
                    )[0]
                    course = var.ID_COURSE[teacher_info[1]]
                    atendance.append([course, status, date])
            atendance.append(studentName)
            return render_template("parent/attendace_info.html", data=atendance)
        else:
            return redirect(url_for("view.unauthorized"))
    else:
        return redirect(url_for("login.user_login"))

# ######################################## [teacher] #####################################
#attendance get and post
@View.route("/record_attendance/<grade>/<section>", methods=["GET", "POST"])
def record_attendance(grade, section):
    if "userID" in session:
            userID = session["userID"]
            role = session["role"]
            sectionID = db.get_section_ID_by_letter(section.lower())
        #try:
            gradeID = var.GRADE_ID[int(grade)]
            if role == "teacher":
                with db.connect() as conn:
                    if request.method == "GET":
                        students = db.Students_info(
                            conn, SearchBy="grade", Search=gradeID,
                            flage=False, section=str(sectionID)
                        )
                        print(students)
                        return render_template("teacher/record_attendance.html", data=students)
                    elif request.method == "POST":
                        students = db.Students_info(
                            conn, SearchBy="grade", Search=gradeID,
                            flage=False, section=str(sectionID)
                        )
                        for student_id in students:
                            studentID = student_id[0]
                            status = int(request.form[f"status{studentID}"])
                            info = db.insert_attendance_info(
                                conn,ids()[1],TeacherID=userID,StudentID=studentID,Status=status,
                                GradeID=gradeID, Section=str(sectionID), Date=datetime.today()
                            )
                            print(info)
                        return redirect(f"/record_attendance/{grade}/{section}")
            else:
                return redirect(url_for("view.unauthorized"))  # Render a template indicating that only teachers can access this functionality
        #except Exception as e:
            #message = "Something went wrong: " + str(e)
            #return render_template("error.html", message=message)  # Render an error template with the error message
    else:
        return redirect(url_for("login.user_login"))  # Redirect to the login page if the user is not authenticated

# GET ATTENDANCE
@View.route("/get_student_attendance/<studentID>")
def get_student_attendance(studentID):
    if "userID" in session:
        userID = session["userID"]
        role = session["role"]
        if role == "teacher":
            try:
                with db.connect() as conn:
                    student = db.Students_info(conn, SearchBy="student", Search=studentID, flage=False)
                    if not student:
                        return redirect(url_for("view.error", message="Student not found"))

                    # Assuming you have a method to retrieve attendance by studentID and course
                    student_name = f"{student[0][4]} {student[0][5]}"
                    attendance = db.Attendace_info(conn,userID,"teacher",False,StudentID=studentID)
                    print("---------",attendance)
                    l = []
                    for attendances in attendance:
                        status = var.ATTENDANCE_STATUSE[attendances[-1]]
                        data = attendances[-2].strftime('%m/%d/%Y')
                        l.append([status,data])
                    return render_template("teacher/student_attendance.html", attendance=[session["course"],student_name,l])

            except Exception as e:
                message = "Error fetching student attendance: " + str(e)
                return render_template("error.html", message=message)

        else:
            return redirect(url_for("view.unauthorized"))

    return redirect(url_for("login.user_login"))


# GET ASSESSMENTS
@View.route("/show_student_assessment/<ID>/<sem>")
def show_student_assessment(ID,sem):
    if "userID" in session:
        userID = session["userID"]
        role = session["role"]
        course = session["course"]
        print(course)
        if role == "teacher":
            with db.connect() as conn:
                assessment = db.Assessements_ifo(
                    conn,ID,False,"student",sem=sem,CourseID=course
                )
                if len(assessment) > 0:
                    print(assessment)
                    student = db.Students_info(conn,"student",ID,flage=False)[0]
                    student_assessment = {
                        'name': f"{student[4]} {student[5]}",
                        'subject': course,
                        'test1': next((a[2] for a in assessment if a[1] == 'test1'), 'N/A'),
                        'test2': next((a[2] for a in assessment if a[1] == 'test2'), 'N/A'),
                        'assignment1': next((a[2] for a in assessment if a[1] == 'assigment1'), 'N/A'),
                        'assignment2': next((a[2] for a in assessment if a[1] == 'assigment2'), 'N/A'),
                        'mid': next((a[2] for a in assessment if a[1] == 'mid'), 'N/A'),
                        'final': next((a[2] for a in assessment if a[1] == 'final'), 'N/A')
                    }
                    print(next((a[2] for a in assessment if a[1] == 'assignment1'), 'N/A'))
                    return render_template("teacher/assessment_view.html",assessment=student_assessment)
                else:
                    message = "no data yet"
                    return redirect(url_for("view.error",message=message))
        else:
            return redirect(url_for("view.unauthorized"))

    else:
        return redirect(url_for("login.user_login"))

#assessment
@View.route("/assessment_insert/<grade>/<section>",methods=["GET","POST"])
def assessment_insert(grade, section):
    if "userID" in session:
        userID = session["userID"]
        role = session["role"]
        sectionID = db.get_section_ID_by_letter(section.lower())
        gradeID = var.GRADE_ID[int(grade)]

        if role == "teacher":
            with db.connect() as conn:
                if request.method == "GET":
                    try:
                        students = db.Students_info(
                            conn, SearchBy="grade", Search=gradeID,
                            flage=False, section=str(sectionID)
                        )
                        assessments = db.Assessements_ifo(
                            conn, gradeID, flage=False,
                            SearchBy="grade", section=str(sectionID)
                        )
                        assessments_info = {
                            'students': students,
                            'assessments': assessments,
                            'assessment_types': var.ASSESSEMENTS_ID
                        }
                        return render_template("teacher/assessement.html", data=assessments_info)

                    except Exception as e:
                        message = f"Error retrieving data: {str(e)}"
                        return render_template("error.html", message=message)

                elif request.method == "POST":
                    try:
                        term = request.form["term"]
                        mark_type = var.ASSESSEMENTS_ID[request.form["mark_type"]]
                        students = db.Students_info(
                            conn, SearchBy="grade", Search=gradeID,
                            flage=False, section=str(sectionID)
                        )
                        CourseID = db.Techears_info(
                            conn,"user",userID,False
                        )[0][1]
                        for student in students:
                            studentID = student[0]
                            mark = request.form[f"mark{studentID}"]
                            db.insert_assessment_info(
                                conn,ids()[1],mark_type,mark,CourseID,term,studentID,userID,
                                var.GRADE_ID[int(grade)],db.get_section_ID_by_letter(section.lower())
                            )

                        return redirect(f"/assessment_insert/{grade}/{section}")

                    except Exception as e:
                        message = f"Error inserting assessment data: {str(e)}"
                        return render_template("error.html", message=message)

        else:
            return redirect(url_for("view.unauthorized"))

    else:
        return redirect(url_for("login.user_login"))

@View.route("/Teacher_course_info")
def teacher_course_info():
    if "userID" in session:
        userID = session["userID"]
        role =  session["role"]
        userName = session["user"]
        if role != "teacher":
            return redirect(url_for("view.unauthorized"))
        else:
            with db.connect() as conn:
                teacher_info = db.Techears_info(
                    conn,"user",userID,False
                )[0]
                CourseID = teacher_info[1]
                g_map = var.GENERAL_ID[session["GradeID"]]
                Grades_and_Section = db.Section_info(conn)
                gg = []
                for grade in Grades_and_Section:
                    print(g_map)
                    print(var.GRADE_ID[int(grade[0])])
                    if var.GRADE_ID[int(grade[0])] in g_map:
                        gg.append(grade)
                CourseInfo = db.Course_info(conn,CourseID)[0][1]
                data = [userName,CourseInfo,gg]
            return render_template("teacher/teacher_course_info.html",data=data)
    else:
        return redirect(url_for("login.user_login"))

# ######################################### [admin] ####################################
@View.route("/admin_users_info")
def admin_users_info():
    if "userID" in session:
        userID = session["userID"]
        role =  session["role"]
        userName = session["user"]
        if role != "admin":
            return redirect(url_for("view.unauthorized"))
        else:
            with db.connect() as conn:
                section = db.Section_info(conn)
            return render_template("admin/admin_users_info.html",data=section)
    else:
        return redirect(url_for("login.user_login"))

@View.route("/admin_get_students/<grade>/<section>")
def admin_get_students(grade,section):
    if "userID" in session:
        userID = session["userID"]
        role =  session["role"]
        if role == "admin":
            if grade and section:
                gradeID = var.GRADE_ID[int(grade)]
                sectionID = db.get_section_ID_by_letter(section.lower())
                print("peeee", sectionID, gradeID)
                with db.connect() as conn:
                    student_info = db.Students_info(
                        conn, SearchBy="grade", Search=gradeID, flage=False, section=str(sectionID)
                    )
                    print(student_info)
                return render_template("admin/admin_get_students.html", data=student_info)
        else:
            return redirect(url_for("view.unauthorized"))
    else:
        return redirect(url_for("login.user_login"))


@View.route("/admin_page")
def _admin():
    if "userID" in session:
        userID = session["userID"]
        role =  session["role"]
        if role == "admin":
            with db.connect() as conn:
                sections = db.Section_info(conn)

            return  render_template("admin/admin_home_page.html")
        else:
            return redirect(url_for("view.unauthorized"))
    else:
        return redirect(url_for("login.user_login"))

@View.route("/add_student_and_parent",methods=["GET","POST"])
def add_student_and_parent():
    if "userID" in session:
        userID = session["userID"]
        role = session["role"]
        student_role = "student"
        parent_role = "parent"
        if role == "admin":
            with db.connect() as conn:
                if request.method == "POST":
                    studentID = RABDOM_ID_2 = ids()[1]
                    profile_pic = request.files["profile_pic"]
                    firstName = request.form["firstName"]
                    lastName = request.form["lastName"]
                    gender = request.form["gender"]
                    age = request.form["age"]
                    student_role = "student"
                    student_full_name = firstName+" "+lastName
                    grade = var.GRADE_ID[int(request.form["grade"])]
                    section = db.get_section_ID_by_letter(request.form["section"].lower())
                    DateOfBirth = request.form["DateOfBirth"]
                    kebela = request.form["kebala"]
                    house_number = request.form["house_number"]
                    studentUID = request.form["studentUID"]

                    parent_exist = db.Parents_info(
                        conn,SearchBy="address",kebela=kebela,
                        house_number=house_number,flage=False
                    )

                    if len(parent_exist) == 0:
                        parentID = RABDOM_ID = ids()[0]
                        parentUID = request.form["parentUID"]
                        parent_firstName = request.form["parent_firstName"]
                        parent_lastName = request.form["parent_lastName"]
                        parent_full_name = parent_firstName+" "+parent_lastName
                        phoneNumber1 = request.form["PhoneNumber1"]
                        phoneNumber2 = request.form["PhoneNumber2"]
                        wareda = request.form["wareda"]
                        section_letter = request.form["section"].lower()
                        insert_section = db.insert_Section_info(
                            conn, var.ID_GRADE[grade], section_letter.upper()
                        )
                        print("*"*9,insert_section,section_letter)
                        insert_parent_to_user = db.Insert_User_info(
                            conn,parentID,parent_full_name,parentUID,parent_role
                        )
                        print("="*19,profile_pic.filename)
                        insert_student_to_user = db.Insert_User_info(
                            conn,studentID,student_full_name,studentUID,student_role
                        )
                        print("="*19,insert_student_to_user)
                        insert_parent = db.insert_parent_info(
                            conn,parentID,parent_firstName,parent_lastName,
                            Kebala=kebela,Wareda=wareda,HouseNumber=house_number,
                            PhoneNumber1=phoneNumber1,PhoneNumber2=phoneNumber2
                        )
                        # student
                        fileName = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))+ str(profile_pic.filename)
                        insert_student = db.insert_student_info(
                            conn, studentID, parentID,grade, section,
                            firstName, lastName, fileName, gender, age, DateOfBirth
                        )
                        print("var.ID_GRADE[grade]",var.ID_GRADE[grade],"insert_student",insert_student,"insert_parent",insert_parent,"insert_student_to_user",insert_student_to_user,"insert_parent_to_user",insert_parent_to_user)
                        if insert_parent and insert_student and insert_parent_to_user and insert_student_to_user:
                            if allowed_file(profile_pic.filename):
                                profile_pic.save(
                                    os.path.join(var.PUT_UPLOAD_PROFILE,fileName)
                                )
                                conn.commit()
                                message = "studernt information inserted Successfully"
                                return redirect(url_for(f"view.successful",message=message))
                            else:
                                message = "[Error] Couldn't insert user info (file not allowed)"
                                return redirect(url_for("view.error", message=message))
                        else:
                            message = "[Error] Couldn't insert user info"
                            return redirect(url_for("view.error",message=message))
                    else:
                        fileName = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)) + str(profile_pic.filename)
                        if allowed_file(profile_pic.filename):
                            section_letter = request.form["section"].lower()
                            insert_section = db.insert_Section_info(
                                conn, var.ID_GRADE[grade], section_letter
                            )
                            parentID = db.Parents_info(conn,SearchBy="address",kebela=kebela,house_number=house_number)[0][0]
                            print("parentID",parentID)
                            insert = db.insert_student_info(
                                conn, studentID, parentID, grade, section,
                                firstName, lastName, profile_pic.filename, gender, age, DateOfBirth
                            )
                            insert_student_to_user = db.Insert_User_info(
                                    conn, studentID, student_full_name,
                                    studentUID,student_role
                            )
                            if insert and insert_student_to_user:
                                if allowed_file(fileName):
                                    profile_pic.save(
                                    os.path.join(var.PUT_UPLOAD_PROFILE, fileName)
                                    )
                                    print("var.ID_GRADE[grade]",var.ID_GRADE[grade],"insert_student_to_user",insert_student_to_user,"insert_student_info",insert,"parentID",parentID)
                                    conn.commit()
                                    message = "studernt information inserted Successfully"
                                    return redirect(url_for("view.successful",message=message))
                                else:
                                    message = "[Error] Couldn't insert user info (file not allowed)"
                                    return redirect(url_for("view.error", message=message))
                            else:
                                message = "[Error] Couldn't insert user info"
                                return redirect(url_for("view.error", message=message))
                        else:
                            message = "[Error] Couldn't insert user info (file not allowed)"
                            return redirect(url_for("view.error", message=message))

                else:
                    sections = db.Section_info(conn)
                    info = [var.GRADE,var.SECTION_]
                    return render_template("admin/admin_add_student_and_parent_info.html",info=info)
        else:
            return redirect(url_for("view.unauthorized"))
    else:
        return redirect(url_for("login.user_login"))

#add teacher info
@View.route("/admin_add_teacher",methods=["GET","POST"])
def add_teacher():
    if "userID" in session:
        userID = session["userID"]
        role = session["role"]
        teacher_role = "teacher"
        if role == "admin":
            if request.method == "POST":
                teacherID = RABDOM_ID_3 = ids()[2]
                profile = request.files["profile_pic"]
                filName = fileName = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))+ str(profile.filename)
                firstName = request.form["firstName"].lower()
                lastName = request.form["lastName"].lower()
                full_name = firstName+" "+lastName
                gradeID = request.form["grade"]
                courseID = var.COURSE_ID[request.form["course"]]
                phoneNumber = request.form["phoneNumber"]
                gender = request.form["gender"]
                kebala = request.form["kebele"]
                house_number = request.form["houseNumber"]
                educationalLevel = request.form["educationalLevel"]
                specialty = request.form["specialty"]
                UID = request.form["UID"]
                with db.connect() as conn:
                    add_teacher_to_user = db.Insert_User_info(
                        conn,UserID=teacherID,UserName=full_name,UID=UID,Role=teacher_role
                    )
                    add_teacher = db.insert_Teacher_info(
                        conn, UserID=teacherID, CourseID=courseID, Grade=gradeID,
                        FirstName=firstName, LastName=lastName,Gender=gender,
                        Specialty=specialty,EducationalLevel=educationalLevel,
                        PhoneNumber=phoneNumber,kebala=kebala,house_number=house_number,Profile=filName
                    )
                    print("1",add_teacher_to_user,"2",add_teacher)
                    if add_teacher_to_user and add_teacher:
                        conn.commit()
                        profile.save(os.path.join(var.PUT_UPLOAD_PROFILE,filName))
                        message = "Successful update user info"
                        return redirect(url_for("view.successful",message=message))
                    else:
                        message = "[Error] Couldn't insert user info"
                        return redirect(url_for("view.error",message=message))
            else:
                with db.connect() as conn:
                    sections = db.Section_info(conn)
                    info = [var.COURSE, var.MAPED_KEY,sections]
                return render_template("admin/admin_add_teacher_info_insert.html", info=info)
        else:
            return redirect(url_for("view.unauthorized"))
    else:
        return redirect(url_for("login.user_login"))

#UPDATE AND DELETE PART 1(VIWE UPDATE AND DELETE IFO)
#parent and teacher
@View.route("/admin_get_user_info")
def admin_get_user_info():
    if "userID" in session:
        userID = session["userID"]
        role = session["role"]
        if role == "admin":
            with db.connect() as conn:
                teachers = db.Techears_info(conn,flage=True)
                return render_template("admin/admin_get_user_info.html",data=teachers)
        else:
            return redirect(url_for("view.unauthorized"))
    else:
        return redirect(url_for("login.user_login"))

#stuent
@View.route("/get_student_info/<grade>/<section>")
def get_student_info(grade=None,section=None):
    if "userID" in session:
        userID = session["userID"]
        role = session["role"]
        if role == "admin" or role == "teacher":
            if grade and section:
                gradeID = var.GRADE_ID[int(grade)]
                sectionID = db.get_section_ID_by_letter(section.lower())
                print("peeee",sectionID,gradeID)
                course = session["course"]
                with db.connect() as conn:
                    student_info = db.Students_info(
                        conn,SearchBy="grade",Search=gradeID,flage=False,section=str(sectionID)
                    )
                    print(student_info)
                return render_template("admin/admin_get_student.html",data=[student_info,course])
            else:
                message = "[Error] No seach section or grade"
                return redirect(url_for(f"view.Error/{message}"))
        else:
            return redirect(url_for("view.unauthorized"))
    else:
        return redirect(url_for("login.user_login"))

#attendance and assessement
@View.route("/admin_get_attendance_and_assesement_info/<grade>/<section>/<get_info_from>")
def admin_get_attendance_and_assesement_info(grade=None,section=None,get_info_from=None):
    if "userID" in session:
        if grade and section and get_info_from:
            userID = session["userID"]
            role = session["role"]
            if role == "admin":
                gradeID = var.GRADE_ID[grade]
                sectionID = db.get_section_ID_by_letter(section)
                with db.connect() as conn:
                    if get_info_from == "attendance":
                        student_info = db.Students_info(
                            conn,SearchBy="grade",Search=gradeID,section=sectionID
                        )
                        attendance_info = db.Attendace_info(
                            conn,gradeID,SearchBy="grade",flage=False,section=sectionID
                        )

                        info = [student_info,attendance_info]

                        return render_template("admin/admin_attendance_and_assessement_info.html",data=info)
                    elif get_info_from == "assesement":
                        student_info = db.Students_info(
                            conn, SearchBy="grade", Search=gradeID, section=sectionID
                        )
                        assesment_info = db.Assessements_ifo(
                            conn,ID=gradeID,flage=False,SearchBy="grade",section=sectionID
                        )

                        info = [student_info, assesment_info]

                        return render_template("admin/admin_attendance_and_assessement_info.html", data=info)
                    else:
                        message = "[Error] No seach section , grade or information"
                        return redirect(url_for(f"Error/{message}"))
            else:
                return redirect(url_for("view.unauthorized"))
        else:
            message = "[Error] No seach section , grade or information"
            return redirect(url_for(f"Error/{message}"))
    else:
        return redirect(url_for("login.user_login"))


#UPDATE AND DELETE PART 2(UPDATE AND DELETE RECORD)

#update TEACHER AND PARENT info
@View.route("/admin_update_teacher_and_parent/<user_role>/<user_ID>",methods=["GET","POST"])
def admin_update_teacher_and_parent(user_role=None,user_ID=None):
    if "userID" in session:
        userID = session["userID"]
        role = session["role"]
        if role == "admin":
            if user_role and user_ID:
                with db.connect() as conn:
                    if request.method == "GET":
                        if user_role == "teacher":
                            teacher_info = db.Teachers_info(
                                conn, SearchBy="user", ID=user_ID, flag=False
                            )[0][1:]
                            attribute = var.TABLE_ATTRIBUTE[user_role.upper()]
                            old_info = [teacher_info, attribute]
                            return render_template("admin/admin_update_teacher_and_parent.html", data=old_info)
                        elif user_role == "parent":
                            parent_info = db.Parents_info(
                                conn, SearchBy="id", ID=user_ID, flag=False
                            )
                            attribute = var.TABLE_ATTRIBUTE[user_role.upper()]
                            old_info = [parent_info, attribute]
                            return render_template("admin/admin_update_teacher_and_parent.html", data=old_info)
                    elif request.method == "POST":
                        if user_role == "teacher":
                            table = user_role.upper()
                            attribute = var.TABLE_ATTRIBUTE[user_role.upper()][1:]
                            firstName = request.form["firstName"].lower()
                            lastName = request.form["lastName"].lower()
                            gradeID = int(request.form["grade"])
                            courseID = var.COURSE_ID[request.form["course"]]
                            phoneNumber = request.form["phoneNumber"]
                            educationalLevel = request.form["educationalLevel"]
                            specialty = request.form["specialty"]
                            new_data = [
                                gradeID, courseID, firstName, lastName, specialty,
                                educationalLevel, phoneNumber
                            ]
                            update = db.update(
                                conn, table, attribute, new_data,
                                var.TABLE_ATTRIBUTE[user_role.upper()][0], user_ID
                            )
                            if not update:
                                message = "[Error] couldn't update user info something went wrong"
                                return redirect(url_for("view.Error", message=message))
                            else:
                                message = "[Successful] Successfully updated user info"
                                return redirect(url_for("view.Successful", message=message))
                        elif user_role == "parent":
                            table = user_role.upper()
                            attribute = var.TABLE_ATTRIBUTE[user_role.upper()][1:]
                            kebela = request.form["kebala"]
                            house_number = request.form["house_number"]
                            parent_firstName = request.form["parent_firstName"]
                            parent_lastName = request.form["parent_lastName"]
                            phoneNumber1 = request.form["phoneNumber1"]
                            phoneNumber2 = request.form["phoneNumber2"]
                            wareda = request.form["wareda"]
                            new_data = [
                                parent_firstName, parent_lastName, kebela,
                                house_number, wareda, phoneNumber1, phoneNumber2
                            ]
                            update = db.update(
                                conn, table, attribute, new_data,
                                var.TABLE_ATTRIBUTE[user_role.upper()][0], user_ID
                            )
                            if update:
                                message = "Successful update user info"
                                return redirect(url_for("view.Error", message=message))
                            else:
                                message = "[Error] couldn't update user info something went wrong"
                                return redirect(url_for("view.Successful", message=message))
            else:
                message = "Something went wrong"
                return redirect(url_for("view.Error", message=message))
        else:
            return redirect(url_for("view.unauthorized"))
    else:
        return redirect(url_for("login.user_login"))

#update STUDENT info
@View.route("/admin_update_student_info/<ID>",methods=["GET","POST"])
def admin_update_student_info(ID=None):
    if "userID" in session:
        userID = session["userID"]
        role = session["role"]
        if role == "admin":
            with db.connect() as conn:
                if request.method == "POST":
                    if student_info:
                        user_role = "student"
                        profile_pic = request.files["profile_pic"]
                        firstName = request.form["firstName"]
                        lastName = request.form["lastName"]
                        table = "student"
                        grade = var.GRADE_ID[request.form["grade"]]
                        section = db.get_section_ID_by_letter(request.form["section"])
                        DateOfBirth = request.form["DateOfBirth"]
                        attribute = var.TABLE_ATTRIBUTE[table][2:]
                        new_data = [grade, section, firstName, lastName, DateOfBirth]
                        update = db.update(
                            conn, table, attribute, new_data, var.TABLE_ATTRIBUTE[table][0], ID
                        )
                        if update:
                            message = "Successful update user info"
                            return redirect(url_for("view.Error", message=message))
                        else:
                            message = "[Error] couldn't update user info something went wrong"
                            return redirect(url_for("view.Successful", message=message))
                    else:
                        return redirect(url_for("view.unauthorized"))
                elif request.method == "GET":
                    student_info = db.Students_info(
                        conn, SearchBy="student", Search=ID, flag=False
                    )[0]
                    if student_info:
                        student_info = student_info[0][1:]
                        student_info[0] = var.ID_GRADE[student_info[0]]
                        student_info[1] = db.get_section_by_id(student_info[1])
                        return render_template("admin/admin_update_student_info.html", data=student_info)
                    else:
                        message = "Empty user data"
                        return render_template("admin/admin_update_student_info.html", data=message)
    else:
        return redirect(url_for("login.user_login"))
#assessement and attendance
@View.route("/admin_update_assessment_and_attendance/<ID>/<update_section>/<put_ID>", methods=["GET", "POST"])
def admin_update_assessment_and_attendance(ID=None, update_section=None, put_ID=None):
    if "userID" in session:
        userID = session["userID"]
        role = session["role"]
        if role == "admin":
            with db.connect() as conn:
                if ID and update_section and put_ID:
                    if request.method == "GET":
                        if update_section == "assessment":
                            assessments_info = db.Assessments_info(
                                conn, ID, flag=False, SearchBy="student"
                            )
                            if assessments_info:
                                student_name = db.Students_info(
                                    conn, SearchBy="student", ID=ID, flag=False
                                )[0][4:5]
                                full_name = firs_name + " " + last_name
                                filter_assessment ={}
                                for i, assessment_info in enumerate(assessments_info):
                                    markID = var.ASSESSMENTS_ID[assessment_info[0]]
                                    mark = assessment_info[1]
                                    firs_name = student_name[0]
                                    last_name = student_name[1]
                                    filter_assessment[i] = [markID, mark]
                                info = [ID, full_name, filter_assessment]
                                return render_template("admin/admin_update_assessment_and_attendance.html", data=info)
                            else:
                                message = "Empty user data"
                                return render_template("admin/admin_update_assessment_and_attendance.html", data=message)
                        elif update_section == "attendance":
                            # student name , date and status
                            attendances_info = db.Attendance_info(
                                conn, SearchBy="student", ID=ID, flag=False
                            )
                            if attendances_info:
                                student_name = db.Students_info(
                                    conn, SearchBy="student", ID=ID, flag=False
                                )[0][4:5]
                                full_name = firs_name + " " +  last_name
                                filter_attendance_info = {}
                                for i, attendance_info in enumerate(attendances_info):
                                    status = var.ATTENDANCE_STATUSES[attendance_info[-1]]
                                    Date = var.ATTENDANCE_STATUSES[attendance_info[-2]]
                                    filter_attendance_info[i] = [status, Date]
                                info = [full_name, filter_attendance_info]
                                return render_template("admin/admin_update_assessment_and_attendance.html", data=info)
                            else:
                                message = "Empty user data"
                                return render_template("admin/admin_update_assessment_and_attendance.html", data=message)
                        else:
                            message = "Unknown information"
                            return redirect(url_for("view.Error", message=message))
                    elif request.method == "POST":
                        if update_section == "assessment":
                            markID = var.ID_ASSESSMENTS[request.form["markID"]]
                            mark = int(request.form["mark"])
                            attribute = var.TABLE_ATTRIBUTE[update_section.upper()][0:3]
                            new_data = [markID, mark, ID]
                            table = update_section.upper()
                            update = db.update(
                                conn, table, attribute, new_data,
                                var.TABLE_ATTRIBUTE[update_section.upper()][0]
                            )
                            if update:
                                message = "Successful update user info"
                                return redirect(url_for("view.Error", message=message))
                            else:
                                message = "[Error] couldn't update user info something went wrong"
                                return redirect(url_for("view.Successful", message=message))
                        elif update_section == "attendance":
                            date = request.form["date"]
                            status = request.form["status"]
                            new_data = [date, status]
                            attribute = var.TABLE_ATTRIBUTE[update_section.upper()][-2:]
                            update = db.update(
                                conn, update_section.upper(), attribute,
                                new_data, var.TABLE_ATTRIBUTE[update_section.upper()][0],put_ID
                            )
                            if update:
                                message = "Successful update user info"
                                return redirect(url_for("view.Error", message=message))
                            else:
                                message = "[Error] couldn't update user info something went wrong"
                                return redirect(url_for("view.Successful", message=message))
                        else:
                            message = "Unknown information"
                            return redirect(url_for("view.Error", message=message))
                else:
                    message = "[Error] No search section, grade or information"
                    return redirect(url_for("view.Error", message=message))
        else:
            return redirect(url_for("view.unauthorized"))
    else:
        return redirect(url_for("login.user_login"))

#delete
@View.route("/delete_record/<ID>/<delete_section>")
def delete(ID=None,delete_section=None):
    if "userID" in session:
        userID = session["userID"]
        role = session["role"]
        if role == "admin":
            delete_data = ["TEACHER","STUDENT","PARENT","ASSESSMENT","ATTENDANCE"]
            with db.connect() as conn:
                if delete_section in delete_data:
                    delete = delete_section.upper()
                    deletes_info = var.DELETE_IFO[delete]

                    message = ""

                    for i,delete_info in enumerate(deletes_info):
                        column = var.TABLE_ATTRIBUTE[delete_info][0]
                        info = db.delete(conn,delete_ifo,ID,column)
                        message += f"column {column} info {info}"
                    return redirect(url_for(f"delete_message/{message}"))
        else:
            return redirect(url_for("view.unauthorized"))
    else:
        return redirect(url_for("login.user_login"))
#resource
@View.route("/get_resource")
def get_resource():
    if "userID" in session:
        userID = session["userID"]
        role = session["role"]
        if request.method == "GET":
            with db.connect() as conn:
                resource = db.Resource_info(conn)
                filtered_resource = []
                if len(resource) > 0:
                    for resources in resource:
                        download_link = var.GET_UPLOAD_RESOURCE+resources[1]
                        re_name = resources[1]
                        des = resources[2]
                        filtered_resource.append([download_link,re_name,des])
            return render_template("resource/resource_info.html",data=filtered_resource)
    else:
        return redirect(url_for("login.user_login"))

@View.route("/add_resource", methods=["GET","POST"])
def add_resource():
    if "userID" in session:
        userID = session["userID"]
        role = session["role"]
        path = var.PUT_UPLOAD_RESOURCE
        if role == "teacher" or role == "admin":
            if request.method == "POST":
                ID = var.RABDOM_ID
                description = request.form["description"]
                file = request.files["resource"]
                if file:
                    with db.connect() as conn:
                        if role == "admin":
                            record = db.insert_Resource_info(
                                conn, ID, file.filename,
                                description, path,Validation=1
                            )
                            if record:
                                file.save(os.path.join(path, file.filename))
                                message = "Successful update user info"
                                return redirect(url_for("view.successful", message=message))
                            else:
                                message = "Cannot save this file"
                                return redirect(url_for("view.error", message=message))
                        else:
                            record = db.insert_Resource_info(
                                conn, ID, file.filename,description,path
                            )
                            if record:
                                file.save(os.path.join(path, file.filename))
                                message = "Resource info uploded Successful"
                                return redirect(url_for("view.successful", message=message))
                            else:
                                message = "Cannot save this file"
                                return redirect(url_for("view.error", message=message))
            else:
                return render_template("resource/resource_upload.html")
        else:
            return redirect(url_for("view.unauthorized"))
    else:
        return redirect(url_for("login.user_login"))

@View.route("/Successful/<message>")
def successful(message):
    if "userID" in session:
        if message:
            return render_template("successful.html", message=message)
        else:
            return redirect(url_for("view.unauthorized"))
    else:
        return redirect(url_for("login.user_login"))

# view.unauthorized
@View.route("/403")
def unauthorized():
    return render_template("403.html")
#
@View.route("/delete_message/<message>")
def delete_message(message):
    if "userID" in session:
        if session["role"] == "admin":
            return render_template("delete_message.html", message=message)
        else:
            return redirect(url_for("view.unauthorized"))
    else:
        return redirect(url_for("login.user_login"))

@View.route("/Error/<message>")
def error(message):
    if "userID" in session:
        return render_template("error.html", data=message)
    else:
        return redirect(url_for("login.user_login"))
