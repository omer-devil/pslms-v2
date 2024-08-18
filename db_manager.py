"""
School Management System Database Operations

This script provides functions to perform various database operations for a school management system.

Dependencies:
    - mysql.connector
    - settings.Settings

Usage:
    - Ensure MySQL database server is running and accessible.
    - Adjust settings in the 'settings.py' file as needed.
    - Use the provided functions to interact with the database.

Functions:
    Database Initialization:
        - create_database(): Create the specified database if it doesn't exist.
        - connect(): Establish a connection to the database.
        - create_tables(conn): Create necessary tables for the project.
        - default_tables(conn): Insert default data into the tables.

    Data Retrieval:
        - Students_info(conn, SearchBy=None, Search=None, flage=True, section=None): Retrieve student information.
        - Teachers_info(conn, SeasrchBy=None, ID=None, flage=True): Retrieve teacher information.
        - Parents_info(conn, SearchBy="address", ID=None, flage=True, kebela=None, house_number=None): Retrieve parent information.
        - Assessements_info(conn, ID, flage=True, SearchBy="Student", section=None): Retrieve assessment information.
        - Attendance_info(conn, ID, SearchBy="student", flage=True, section=None): Retrieve attendance information.
        - Grades_info(conn, ID=None, flage=True, SearchBy="student"): Retrieve grade information.
        - Resource_info(conn, role="admin"): Retrieve resource information.

    Data Insertion:
        - Insert_User_info(conn, UserID, UserName, UID, Role): Insert user information.
        - insert_Teacher_info(conn, UserID, CourseID, GradeID, FirstName, LastName, Specialty, EducationalLevel, PhoneNumber): Insert teacher information.
        - insert_student_info(conn, UserID, ParentID, GradeID, Section, FirstName, LastName, DateOfBirth): Insert student information.
        - insert_parent_info(conn, UserID, FirstName, LastName, Kebala, Wareda, HouseNumber, PhoneNumber1, PhoneNumber2): Insert parent information.
        - insert_course_info(conn, CourseID, Title, GradeID, Description): Insert course information.
        - insert_assessment_info(conn, MarkID, Mark, StudentID, TeacherID): Insert assessment information.
        - insert_attendance_info(conn, TeacherID, StudentID, Status, GradeID): Insert attendance information.
        - insert_Grade_info(conn, GradeID, Grade): Insert grade information.
        - insert_Resource_info(conn, ID, ResoureName, Description, path, Validation=0): Insert resource information.

    Data Update and Delete:
        - update(conn, table, columns, new_values): Update records in the database.
        - delete(conn, table, ID, name_column): Delete a record from the database.
"""


import mysql.connector
from settings import Settings
import datetime
import random
import string

var = Settings()
var.variables()
username = var.DB_USERNAME
DB_name = var.DB_NAME
host = var.DB_HOST
password = var.DB_PASSWORD


db_names = {
        "Development": "development",
        "Testing": "testing",
        "Production": "production"
    }
db_name = db_names[DB_name]

# Function to create the specified database if it doesn't exist
def create_database():
    """
    :return: True if the database creation is successful, otherwise False
    """
    conn = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
    )
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    conn.commit()
    return True

# Function to establish a connection to the database
def connect():
    """
    :return: Connection object if connection is successful, otherwise None
    """
    conn = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=db_name
    )
    return conn
# Function to create all the necessary tables for the project

def create_tables(conn):
    """
    :param conn: Database connection object
    :return: True if table creation is successful, otherwise False
    """
    q = [
        """CREATE TABLE IF NOT EXISTS USER(
            UserID VARCHAR(50) PRIMARY KEY,
            UserName VARCHAR(50),
            UID VARCHAR(50),
            Role VARCHAR(50)
        );""",
        """CREATE TABLE IF NOT EXISTS TEACHER(
            UserID VARCHAR(50) PRIMARY KEY,
            CourseID VARCHAR(100),
            FirstName VARCHAR(50),
            LastName VARCHAR(50),
            Speciality VARCHAR(50),
            EducationalLevel VARCHAR(50),
            GradeID VARCHAR(50),
            Profile VARCHAR(100),
            Gender VARCHAR(100),
            Kebala VARCHAR(50),
            HouseNumber INTEGER,
            PhoneNumber INTEGER
            
        );""",
        """CREATE TABLE IF NOT EXISTS STUDENT(
            UserID VARCHAR(50) PRIMARY KEY,
            ParentID VARCHAR(10),
            GradeID VARCHAR(10),
            Section VARCHAR(10),
            FirstName VARCHAR(50),
            LastName VARCHAR(50),
            Profile VARCHAR(100),
            Gender VARCHAR(100),
            Age INTEGER,
            DateOfBirth DATE
        );""",
        """CREATE TABLE IF NOT EXISTS PARENT(
            ParentID VARCHAR(10) PRIMARY KEY,
            FirstName VARCHAR(50),
            LastName VARCHAR(50),
            Kebala VARCHAR(50),
            HouseNumber VARCHAR(50),
            Wareda VARCHAR(50),
            PhoneNumber1 INTEGER,
            PhoneNumber2 INTEGER
            
        );""",
        """CREATE TABLE IF NOT EXISTS COURSE(
            CourseID VARCHAR(50) PRIMARY KEY,
            Title VARCHAR(50)
        );""",
        """CREATE TABLE IF NOT EXISTS ASSESSMENT(
            AssessmentID VARCHAR(10) PRIMARY KEY,
            MarkID VARCHAR(10),
            Mark VARCHAR(10),
            CourseID VARCHAR(50),
            Term VARCHAR(50),
            StudentID VARCHAR(10),
            TeacherID VARCHAR(10),
            GradeID VARCHAR(10),
            Section VARCHAR(10)
        );""",
        """CREATE TABLE IF NOT EXISTS ATTENDANCE(
            AttendanceID VARCHAR(50) PRIMARY KEY,
            TeacherID VARCHAR(10),
            StudentID VARCHAR(10),
            GradeID VARCHAR(10),
            Section VARCHAR(10),
            Date DATE,
            Status INTEGER
        );""",
        """CREATE TABLE IF NOT EXISTS GRADE(
            GradeID VARCHAR(10) PRIMARY KEY,
            Grade VARCHAR(10)
        );""",
        """CREATE TABLE IF NOT EXISTS RESOURCE(
            ResourceID VARCHAR(10) PRIMARY KEY,
            ResourceName VARCHAR(1000),
            Description VARCHAR(1000),
            Path VARCHAR(1000),
            Validation INT(2)
        );""",
        """CREATE TABLE IF NOT EXISTS SECTION(
            GradeID VARCHAR(100),
            section VARCHAR(10)
        );"""
    ]

    cursor = conn.cursor()
    for query in q:
        cursor.execute(query)
    conn.commit()
    cursor.close()

# inserting deffoult data
def get_section_by_id(id):
    SECTION = var.SECTION
    for ID, section in SECTION:
        if id == ID:
            return section
    return None

def get_section_ID_by_letter(_section):
    SECTION = var.SECTION
    for ID, section in SECTION:
        if section.lower() == _section:
            return ID
    return None


def default_tables(conn):
    courses = var.COURSE
    coursesID = var.COURSE_ID
    grades = var.GRADE
    userID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    gradesID = var.GRADE_ID
    user_name = var.ADMIN_NAME
    password = var.ADMIN_PASSWORD
    cur = conn.cursor()

    q_course = "INSERT INTO COURSE VALUES (%s, %s);"
    q_grade = "INSERT INTO GRADE VALUES (%s, %s);"

    _courses = []
    _grades = []

    try:
        for course in courses:
            _courses.append((coursesID[course], course))

        cur.executemany(q_course, _courses)

        for grade in grades:
            _grades.append((gradesID[grade], grade))

        cur.executemany(q_grade, _grades)
        cur.execute("INSERT INTO USER VALUES(%s,%s,%s,%s);", (userID, user_name, password, "admin"))
        conn.commit()

        return True
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()  # Rollback changes if an error occurs
        return False



'''def Relational_statement(conn):
    alter_statements = [
        """ALTER TABLE TEACHER
           ADD CONSTRAINT fk_teacher_course
           FOREIGN KEY (CourseID) REFERENCES COURSE(CourseID),
           ADD CONSTRAINT fk_teacher_user
           FOREIGN KEY (UserID) REFERENCES USER(UserID),
           ADD CONSTRAINT fk_teacher_grade
           FOREIGN KEY (GradeID) REFERENCES GRADE(GradeID)""",
        """ALTER TABLE RESOURCE
           ADD CONSTRAINT fk_resource_grade
           FOREIGN KEY (GradeID) REFERENCES GRADE(GradeID)""",
        """ALTER TABLE ASSESSMENT
           ADD CONSTRAINT fk_assessment_grade
           FOREIGN KEY (GradeID) REFERENCES GRADE(GradeID)"""
    ]
    cur = conn.cursor()
    for alter_statement in alter_statements:
        try:
            cur.execute(alter_statement)
            conn.commit()
        except Exception as e:
            print("i am the problam and my problame is :",e)
    cur.close()'''

def user(conn,username, uid,role,ToDo="login"):
    """
    :param conn: Database connection object
    :param username: Username
    :param uid: User ID
    :param ToDo: Operation to perform (default is "login")
    :return: Result of the operation
    """
    cur = conn.cursor()
    if ToDo == "login":
        try:
            cur.execute("SELECT * FROM USER WHERE UserName = %s AND  UID = %s AND Role = %s", (username,uid,role))
            data = cur.fetchall()
            print("=" * 8, data)
            if len(data) > 0:
                print("$"*8,data)
                return True
            else:
                return False
        except Exception as e:
            return False
    elif ToDo == "selectall":
        try:
            cur.execute("SELECT * FROM USER;")
            data = cur.fetchall()
            return data
        except Exception as e:
            return f"[ERROR] {e}"
    elif ToDo == "search":
        try:
            cur.execute("SELECT * FROM USER WHERE UserName = %s AND  UID = %s AND Role = %s", (username, uid,role))
            data = cur.fetchall()
            print(data)
            return data
        except Exception as e:
            return f"[ERROR] {e}"

#fecth info for each table

def Students_info(conn, SearchBy=None, Search=None, flage=True, section=None):
    """
    :param conn: Database connection object
    :param SearchBy: Search criteria (default is None)
    :param Search: Search keyword (default is None)
    :param flage: Flag to indicate whether to fetch all students or filtered (default is True)
    :param section: Section filter for grade search (default is None)
    :return: Information about students or error message
    """
    cur = conn.cursor()
    if flage:
        try:
            cur.execute("SELECT * FROM STUDENT;")
            info = cur.fetchall()
            return info
        except Exception as e:
            return f"[ERROR] {e}"
    else:
        if SearchBy == "grade":
            if section is not None:
                try:
                    cur.execute("SELECT * FROM STUDENT WHERE GradeID = %s AND Section = %s;", (Search, section))
                    info = cur.fetchall()
                    return info
                except Exception as e:
                    return f"[ERROR] {e}"
            else:
                return "[ERROR] Section parameter is required for grade search"
        elif SearchBy == "student":
            try:
                cur.execute("SELECT * FROM STUDENT WHERE UserID = %s;", (Search,))
                info = cur.fetchall()
                return info
            except Exception as e:
                return f"[ERROR] {e}"
        elif SearchBy == "parent":
            try:
                cur.execute("SELECT * FROM STUDENT WHERE ParentID = %s;", (Search,))
                info = cur.fetchall()
                return info
            except Exception as e:
                return f"[ERROR] {e}"
        else:
            return "[ERROR] Invalid SearchBy value"

def Course_info(conn,ID):
    """
    :param conn: Database connection object
    :param SearchBy: Search criteria (default is None)
    :param Search: Search keyword (default is None)
    :param flage: Flag to indicate whether to fetch all students or filtered (default is True)
    :return: Information about students
    """
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT * FROM COURSE WHERE CourseID = %s;",(ID,))
        info = cur.fetchall()
        return info
    except Exception as e:
        return f"[ERROR] {e}"

def Techears_info(conn,SeasrchBy=None,ID=None,flage=True,MapID=None):
    """
    :param conn: Database connection object
    :param SearchBy: Search criteria ("User", "Grade", "Course") (default is None)
    :param ID: User ID, Grade ID, or Course ID (default is None)
    :param flage: Flag to indicate whether to fetch all teachers or filtered (default is True)
    :return: Information about teachers
    """
    cur = conn.cursor()
    if flage:
        try:
            cur.execute("SELECT * FROM TEACHER;")
            info = cur.fetchall()
            return info
        except Exception as e:
            return f"[ERROR] {e}"
    elif not(flage):
        if SeasrchBy == "user":
            try:
                cur.execute("SELECT * FROM TEACHER WHERE UserID = %s;",(ID,))
                info = cur.fetchall()
                return info
            except Exception as e:
                return f"[ERROR] {e}"
        elif SeasrchBy == "grade":
            try:
                cur.execute("SELECT * FROM TEACHER WHERE GradeID = %s;",(ID,))
                info = cur.fetchall()
                return info
            except Exception as e:
                return f"[ERROR] {e}"
        elif SeasrchBy == "course":
            try:
                cur.execute("SELECT * FROM TEACHER WHERE CourseID = %s AND GradeID = %s;",(ID,MapID))
                info = cur.fetchall()
                return info
            except Exception as e:
                return f"[ERROR] {e}"

def Parents_info(conn,SearchBy="address",ID=None,flage=True,kebela=None,house_number=None):
    """
    :param conn: Database connection object
    :param ID: Parent ID (default is None)
    :param flage: Flag to indicate whether to fetch all parents or filtered (default is True)
    :return: Information about parents
    """
    cur = conn.cursor()
    if flage:
        try:
            cur.execute("SELECT * FROM PARENT;")
            info = cur.fetchall()
            return info
        except Exception as e:
            return f"[ERROR] {e}"
    elif not(flage):
        if SearchBy == "id":
            try:
                cur.execute("SELECT * FROM PARENT WHERE ParentID = %s;",(ID,))
                info = cur.fetchall()
                return info
            except Exception as e:
                return f"[ERROR] {e}"
        elif SearchBy == "address":
            cur.execute("SELECT * FROM PARENT WHERE Kebala = %s AND HouseNumber = %s;", (kebela,house_number))
            info = cur.fetchall()
            return info


def Assessements_ifo(conn,ID,flage=True,SearchBy="student",section=None,markID=None,sem=None,CourseID=None):
    """
    :param conn: Database connection object
    :param ID: Student ID or Teacher ID
    :param flage: Flag to indicate whether to fetch all assessments or filtered (default is True)
    :param SearchBy: Search criteria ("Student" or "Teacher") (default is "Student")
    :return: Information about assessments
    """
    cur = conn.cursor()
    if flage:
        try:
            cur.execute("SELECT * FROM ASSESSMENT;")
            info = cur.fetchall()
            return info
        except Exception as e:
            return f"[ERROR] {e}"
    elif not(flage):
        if SearchBy == "student":
            print(ID,sem)
            try:
                cur.execute("SELECT * FROM ASSESSMENT WHERE StudentID = %s AND Term = %s AND CourseID = %s ",(ID,sem,CourseID))
                info = cur.fetchall()
                return info
            except Exception as e:
                return f"[ERROR] {e}"
        elif SearchBy == "teacher":
            try:
                cur.execute("SELECT * FROM ASSESSMENT WHERE TeacherID = %s AND Term = s%;",(ID,sem))
                info = cur.fetchall()
                return info
            except Exception as e:
                return f"[ERROR] {e}"
        elif SearchBy == "grade":
            try:
                cur.execute("SELECT * FROM ASSESSMENT WHERE GradeID = %s AND Section = %s AND Term = %s;",(ID,section,sem))
                info = cur.fetchall()
                return info
            except Exception as e:
                return f"[ERROR] {e}"
        elif SearchBy == "ng":
            try:
                cur.execute("SELECT * FROM ASSESSMENT WHERE GradeID = %s AND Section = %s AND Mark = ng;",(ID,section))
                info = cur.fetchall()
                return info
            except Exception as e:
                return f"[ERROR] {e}"
        elif SearchBy == "mark":
            try:
                cur.execute("SELECT * FROM ASSESSMENT WHERE StudentID = %s AND MarkID = %s;",(ID,markID))
                info = cur.fetchall()
                return info
            except Exception as e:
                return f"[ERROR] {e}"


def Attendace_info(conn,ID,SearchBy="student",flage=True,section=None,StudentID=None):
    """
    :param conn: Database connection object
    :param ID: Student ID or Teacher ID
    :param SearchBy: Search criteria ("Student" or "Teacher") (default is "Student")
    :param flage: Flag to indicate whether to fetch all attendance records or filtered (default is True)
    :return: Information about attendance
    """
    cur = conn.cursor()
    if flage:
        try:
            cur.execute("SELECT * FROM ASSESSMENT;")
            info = cur.fetchall()
            return info
        except Exception as e:
            return f"[ERROR] {e}"
    elif not(flage):
        if SearchBy == "student":
            try:
                cur.execute("SELECT * FROM ATTENDANCE WHERE StudentID = %s ;",(ID,))
                info = cur.fetchall()
                return info
            except Exception as e:
                return f"[ERROR] {e}"
        elif SearchBy == "teacher":
            try:
                cur.execute("SELECT * FROM ATTENDANCE WHERE TeacherID = %s AND StudentID = %s;",(ID,StudentID))
                info = cur.fetchall()
                return info
            except Exception as e:
                return f"[ERROR] {e}"
        elif SearchBy == "grade":
            try:
                cur.execute("SELECT * FROM ATTENDANCE WHERE GradeID = %s AND Section = %s;",(ID,section))
                info = cur.fetchall()
                return info
            except Exception as e:
                return f"[ERROR] {e}"

def Grades_info(conn,ID=None,flage=True,SearchBy="student"):
    """
    :param conn: Database connection object
    :param ID: Student ID or Teacher ID (default is None)
    :param flage: Flag to indicate whether to fetch all grades or filtered (default is True)
    :param SearchBy: Search criteria ("student" or "teacher") (default is "student")
    :return: Information about grades
    """
    cur = conn.cursor()
    if flage:
        try:
            cur.execute("SELECT * FROM GRADE;")
            info = cur.fetchall()
            return info
        except Exception as e:
            return f"[ERROR] {e}"
    elif not(flage):
        if SearchBy == "student":
            try:
                cur.execute("SELECT * FROM GRADE WHERE StudentID = %s;",(ID,))
                info = cur.fetchall()
                return info
            except Exception as e:
                return f"[ERROR] {e}"
        elif SearchBy == "teacher":
            try:
                cur.execute("SELECT * FROM GRADE WHERE TeacheID = %s;",(ID,))
                info = cur.fetchall()
                return info
            except Exception as e:
                return f"[ERROR] {e}"

def Resource_info(conn):
    """
    :param conn: Database connection object
    :return: Information about resources
    """
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM RESOURCE;")
        info = cur.fetchall()
        return info
    except Exception as e:
        return f"[ERROR] {e}"

def Section_info(conn):
    """
    :param conn: Database connection object
    :return: Information about resources
    """
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM section;")
        info = cur.fetchall()
        return info
    except Exception as e:
        return f"[ERROR] {e}"
#inserting info into each table
def Insert_User_info(conn,UserID,UserName,UID,Role):
    """
    :param conn: Database connection object
    :param UserID: User ID
    :param UserName: Username
    :param UID: User ID
    :param Role: User role
    :return: True if insertion is successful, otherwise False
    """
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM USER WHERE UserName = %s AND UID = %s AND Role = %s;",(UserName,UID,Role))
        data = cur.fetchall()
        if len(data) == 0:
            cur.execute("INSERT INTO USER VALUES(%s,%s,%s,%s);",(UserID,UserName,UID,Role))
            return True
        else:
            return False
    except Exception as e:
        return e

def insert_Teacher_info(conn,UserID,CourseID,FirstName,LastName,Specialty,EducationalLevel,Grade,Profile,Gender,kebala,house_number,PhoneNumber):
    """
    :param conn: Database connection object
    :param UserID: Teacher's user ID
    :param CourseID: Course ID
    :param GradeID: Grade ID
    :param FirstName: Teacher's first name
    :param LastName: Teacher's last name
    :param Specialty: Teacher's specialty
    :return: True if insertion is successful, otherwise False
    """
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM TEACHER WHERE CourseID = %s AND FirstName = %s AND LastName = %s AND Speciality = %s AND EducationalLevel = %s ;", (CourseID,FirstName,LastName,Specialty,EducationalLevel))
        data = cur.fetchall()
        if len(data) == 0:
            cur.execute("INSERT INTO TEACHER VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",(UserID,CourseID,FirstName,LastName,Specialty,EducationalLevel,Grade,Profile,Gender,kebala,house_number,PhoneNumber))
            return "i am the problam"
        else:
            return False
    except Exception as e:
        return e

def insert_student_info(conn, UserID, ParentID, GradeID, Section, FirstName, LastName, Profile, gender, age, DateOfBirth):
    """
    :param conn: Database connection object
    :param UserID: Student's user ID
    :param ParentID: Parent's ID
    :param GradeID: Grade ID
    :param Section: Section
    :param FirstName: Student's first name
    :param LastName: Student's last name
    :param Profile: Student's profile picture
    :param gender: Student's gender
    :param age: Student's age
    :param DateOfBirth: Student's date of birth
    :return: True if insertion is successful, otherwise False
    """
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM STUDENT WHERE ParentID = %s AND GradeID = %s AND Section = %s AND FirstName = %s AND LastName = %s;",(ParentID,GradeID,Section,FirstName,LastName))
        data = cur.fetchall()
        print("459875837data",data)
        if len(data) == 0:
            cur.execute("INSERT INTO STUDENT VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",(UserID,ParentID,GradeID,Section,FirstName,LastName,Profile,gender,age,DateOfBirth))
            return True
        else:
            return False
    except Exception as e:
        print("err",e)
        return False

def insert_parent_info(conn,UserID,FirstName,LastName,Kebala,Wareda,HouseNumber,PhoneNumber1,PhoneNumber2):
    """
    :param conn: Database connection object
    :param UserID: Parent's user ID
    :param FirstName: Parent's first name
    :param LastName: Parent's last name
    :param PhoneNumber: Parent's phone number
    :return: True if insertion is successful, otherwise False
    """
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM PARENT WHERE Kebala = %s AND HouseNumber = %s;",(Kebala,HouseNumber))
        data = cur.fetchall()
        print("459875837data", data)
        if len(data) == 0:
            cur.execute("INSERT INTO PARENT VALUES(%s,%s,%s,%s,%s,%s,%s,%s);",(UserID,FirstName,LastName,Kebala,HouseNumber,Wareda,PhoneNumber1,PhoneNumber2))
            return True
    except Exception as e:
        return e
def insert_course_info(conn,CourseID,Title,GradeID,Description):
    """
    :param conn: Database connection object
    :param CourseID: Course ID
    :param Title: Course title
    :param GradeID: Grade ID
    :param Description: Course description
    :return: True if insertion is successful, otherwise False
    """
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO COURSE VALUES(%s,%s,%s,%s);",(CourseID,Title,GradeID,Description))
        conn.commit()
        return True
    except Exception as e:
        return False

def insert_assessment_info(conn,AssessmentID,MarkID,Mark,CourseID,Term,StudentID,TeacherID,GradeID,SectionID):
    """
    :param conn: Database connection object
    :param Test1: Test 1 score
    :param Test2: Test 2 score
    :param Assignment1: Assignment 1 score
    :param Assignment2: Assignment 2 score
    :param Notebook: Notebook score
    :param StudentID: Student's ID
    :param TeacherID: Teacher's ID
    :return: True if insertion is successful, otherwise False
    """
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM ASSESSMENT WHERE MarkID = %s AND StudentID = %s AND Term = %s AND CourseID = %s;", (MarkID,StudentID,Term,CourseID))
        data = cur.fetchall()
        if len(data) == 0:
            cur.execute("INSERT INTO ASSESSMENT VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);",(AssessmentID,MarkID,Mark,CourseID,Term,StudentID,TeacherID,GradeID,SectionID))
            conn.commit()
            return True
        else:
            return False
    except Exception as e:
        print("Err",e)
        return False

def insert_attendance_info(conn,AttendanceID,TeacherID,StudentID,GradeID,Section,Date,Status):
    """
    :param conn: Database connection object
    :param TeacherID: Teacher's ID
    :param StudentID: Student's ID
    :param Status: Attendance status
    :param GradeID: Grade ID
    :return: True if insertion is successful, otherwise False
    """
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO ATTENDANCE VALUES(%s,%s,%s,%s,%s,%s,%s);",(AttendanceID,TeacherID,StudentID,GradeID,Section,Date,Status))
        conn.commit()
        return True
    except Exception as e:
        print("Err",e)
        return False

def insert_Grade_info(conn,GradeID,Grade):
    """
    :param conn: Database connection object
    :param TeacherID: Teacher's ID
    :param StudentID: Student's ID
    :param Status: Attendance status
    :param GradeID: Grade ID
    :return: True if insertion is successful, otherwise False
    """
    cur = conn.coursor()
    try:
        cur.execute("INSERT INTO COURSE VALUES(%s,%s);",(GradeID,Grade))
        conn.commit()
        return True
    except Exception as e:
        return False

def insert_Resource_info(conn,ID,ResoureName,Description,path,Validation=0):
    """
    :param conn: Database connection object
    :param ResourceID: Resource ID
    :param ResourceName: Resource name
    :param Description: Resource description
    :param GradeID: Grade ID
    :return: True if insertion is successful, otherwise False
    """
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO RESOURCE VALUES(%s,%s,%s,%s,%s);",(ID,ResoureName,Description,path,Validation))
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return e

def insert_Section_info(conn,GradeID,section):
    """
    :param conn: Database connection object
    :param TeacherID: Teacher's ID
    :param StudentID: Student's ID
    :param Status: Attendance status
    :param GradeID: Grade ID
    :return: True if insertion is successful, otherwise False
    """
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM SECTION WHERE GradeID = %s AND section = %s", (GradeID, section))
        data = cur.fetchall()
        if len(data) == 0:
            cur.execute("INSERT INTO SECTION VALUES(%s,%s);",(GradeID,section))
            return True
        else:
            return data
    except Exception as e:
        return e

#update section qurey = UPDATE TABLENAME SET Update = %s  WHERE ID = %s

def update(conn, table, columns, new_values, ID_column_name, ID):
    """
    Update records in the database.

    :param conn: Database connection object
    :param table: Table name
    :param columns: List of column names to update
    :param new_values: New values for the specified columns
    :param ID_column_name: Name of the column used for ID
    :param ID: ID value
    :return: True if update is successful, otherwise False
    """
    try:
        cur = conn.cursor()

        # Generate the SET part of the SQL query
        set_part = ", ".join([f"{column}=%s" for column in columns])

        # Update table information
        query = f"UPDATE {table} SET {set_part} WHERE {ID_column_name}=%s;"

        # Append the ID value to new_values
        new_values.append(ID)

        # Execute the query with new_values as a tuple
        cur.execute(query, tuple(new_values))

        # Commit changes and close connection
        conn.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

#delete section

def delete(conn, table, ID, name_column):
    """
    Delete a record from the database.

    :param conn: Database connection object
    :param table: Table name
    :param ID: ID of the record to delete
    :param name_column: Column name to use for condition
    :return: True if delete is successful, otherwise False
    """
    try:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {table} WHERE {name_column} = %s", (ID,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

