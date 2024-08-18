"""
School Management System Configuration

Description:
    This module defines settings and configurations for the school management system application.

Usage:
    1. Customize the variables and mappings according to your application requirements.
    2. Use the configured settings throughout your application.

Variables:

    Database Settings:
        - DB_USERNAME: Database username.
        - DB_PASSWORD: Database password.
        - DB_HOST: Database host address.
        - DB_NAME: Database name.

    Application Settings:
        - SECRET_KEY: Secret key for Flask application.
        - RANDOM_ID: Randomly generated ID for various purposes.

    Data Settings:
        - MAPED_KEY: List of mapped keys.
        - GRADE_ID: Mapping of grade levels to grade IDs.
        - GRADE: List of grade levels.
        - COURSE: List of courses.
        - TABLE_ATTRIBUTE: Dictionary defining table attributes.
        - SECTION: List of sections.

    File Paths:
        - UPLOAD_RESOURCE: Path for uploading resources.
        - UPLOAD_PROFILE: Path for uploading user profiles.

    Mappings:
        - COURSE_ID: Mapping of course names to course IDs.
        - profiles: Mapping of user roles to profile templates.
        - COURSE_TAKE: Mapping of courses to grades where they are taught.
        - ASSESSEMENTS_ID: Mapping of assessment types to IDs.
        - GENERAL_ID: Mapping of grade ranges to grade IDs.
        - COURSE_TAKE_BY_GRADE: Mapping of grades to courses they take.

"""


import secrets
import string
import random

class Settings():
    def variables(self):
        """
        Set up variables for database connection, grades, courses, file paths, etc.
        """
        self.DB_USERNAME = "root"  # Database username
        self.DB_PASSWORD = "DEVILO.K@2019"  # Database password
        self.DB_HOST = "127.0.0.1"  # Database host
        self.DB_NAME = "Development"  # Database name
        self.SECRET_KEY = secrets.token_hex(16)  # Secret key for Flask application
        self.ADMIN_NAME = "admin"
        self.ADMIN_PASSWORD = "123"
        self.RABDOM_ID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

        # list of grade and course
        self.GRADE_ID = {4:"G4",5:"G5",6:"G6",7:"G7",8:"G8"}  # Mapping of grade levels to grade IDs
        self.ID_GRADE = {'G4': 4, 'G5': 5, 'G6': 6, 'G7': 7, 'G8': 8}

        self.ATTENDANCE_STATUSE = {1:"present",0:"absent",2:"permission"}

        self.GRADE = [4,5,6,7,8]  # List of grade levels
        self.SECTION_ = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        self.COURSE = [  # List of courses
            "Amharic", "Moral", "GeneralScience", "Afanoromo",
            "Science", "Maths", "English", "Ict", "Cte", "CitizenShip",
            "Harari", "SocialStudies"
        ]
        self.TABLE_ATTRIBUTE = {
            "USER": ["UserID", "UserName", "UID", "Role"],
            "TEACHER": ["UserID", "CourseID", "FirstName", "LastName", "Speciality", "EducationalLevel", "GradeID", "Profile", "Gender", "Kebala", "HouseNumber", "PhoneNumber"],
            "STUDENT": ["UserID", "ParentID", "GradeID", "Section", "FirstName", "LastName", "Profile", "Gender", "Age", "DateOfBirth"],
            "PARENT": ["ParentID", "FirstName", "LastName", "Kebala", "HouseNumber", "Wareda", "PhoneNumber1", "PhoneNumber2"],
            "COURSE": ["CourseID", "Title"],
            "ASSESSMENT": ["AssessmentID", "MarkID", "Mark", "CourseID", "Term", "StudentID", "TeacherID", "GradeID", "Section"],
            "ATTENDANCE": ["AttendanceID", "TeacherID", "StudentID", "GradeID", "Section", "Date", "Status"],
            "GRADE": ["GradeID", "Grade"],
            "RESOURCE": ["ResourceID", "ResourceName", "Description", "Path", "Validation"],
            "SECTION": ["GradeID", "Section"]
        }
        self.DELETE_IFO = {
            "USER": ["TEACHER","STUDENT","PARENT"],
            "TEACHER": ["USER","ASSESSMENT","ATTENDANCE"],
            "STUDENT": ["USER","ASSESSMENT","ATTENDANCE"],
            "PARENT": ["USER"],
            "ASSESSMENT": ["ASSESSMENT"],
            "ATTENDANCE":["ATTENDANCE"]

        }

        self.SECTION = list(enumerate(string.ascii_uppercase, start=1))

        # path
        self.PUT_UPLOAD_RESOURCE = "C:\\Users\\hacker\\PycharmProjects\\final\\static\\upload\\resource"  # Path for uploading resources
        self.PUT_UPLOAD_PROFILE = "C:\\Users\\hacker\\PycharmProjects\\final\\static\\upload\\profile"  # Path for uploading profiles
        self.GET_UPLOAD_PROFILE = "upload/profile/"
        self.GET_UPLOAD_RESOURCE = "upload/resource/"

        self.ALLOWED_EXTENSIONS = {'txt', 'png', 'jpg', 'jpeg', 'gif','.pdf','.pp','.doc','.docx','.xls','.xlsx'}
        self.COURSESID = ["a-mharic", "m-oral", "general-science", "a-fanoromo", "s-cience", "m-aths", "e-nglish", "i-ct", "c-te", "citizen-ship", "h-arari", "social-studies"]
        # mapin
        self.COURSE_ID = {  # Mapping of course names to course IDs
            "Amharic": "a-mharic",
            "Moral": "m-oral",
            "GeneralScience": "general-science",
            "Afanoromo": "a-fanoromo",
            "Science": "s-cience",
            "Maths": "m-aths",
            "English": "e-nglish",
            "Ict": "i-ct",
            "Cte": "c-te",
            "CitizenShip": "citizen-ship",
            "Harari": "h-arari",
            "SocialStudies": "social-studies"
        }
        self.ID_COURSE = {
            "a-mharic": "Amharic",
            "m-oral": "Moral",
            "general-science": "GeneralScience",
            "a-fanoromo": "Afanoromo",
            "s-cience": "Science",
            "m-aths": "Maths",
            "e-nglish": "English",
            "i-ct": "Ict",
            "c-te": "Cte",
            "citizen-ship": "CitizenShip",
            "h-arari": "Harari",
            "social-studies": "SocialStudies"
        }

        self.profiles = {  # Mapping of user roles to profile templates
            "student": "student/student_profile.html",
            "teacher": "teacher/teacher_profile.html",
            "parent" : "parent/parent_profile.html"
        }
        self.COURSE_TAKE = {  # Mapping of courses to grades where they are taught
            "a-mharic": ["G4","G5","G6","G7","G8"],
            "m-oral": ["G4","G5","G6"],
            "general-science": ["G7","G8"],
            "a-fanoromo": ["G4","G5","G6","G7","G8"],
            "s-cience": ["G4","G5","G6"],
            "m-aths": ["G4","G5","G6","G7","G8"],
            "e-nglish": ["G4","G5","G6","G7","G8"],
            "i-ct": ["G4","G5","G6","G7","G8"],
            "c-te": ["G7","G8"],
            "citizen-ship": ["G7","G8"],
            "h-arari": ["G4","G5","G6","G7","G8"],
            "social-studies": ["G7","G8"]
        }
        self.COURSE_TAKE_BY_GRADE = {
            "G4": ["a-mharic", "m-oral", "a-fanoromo", "s-cience", "m-aths", "e-nglish", "i-ct", "h-arari"],
            "G5": ["a-mharic", "m-oral", "a-fanoromo", "s-cience", "m-aths", "e-nglish", "i-ct", "h-arari"],
            "G6": ["a-mharic", "m-oral", "a-fanoromo", "s-cience", "m-aths", "e-nglish", "i-ct", "h-arari"],
            "G7": ["a-mharic", "general-science", "a-fanoromo", "s-cience", "m-aths", "e-nglish", "i-ct", "c-te",
                   "citizen-ship", "h-arari", "social-studies"],
            "G8": ["a-mharic", "general-science", "a-fanoromo", "m-aths", "e-nglish", "i-ct", "c-te", "citizen-ship",
                   "h-arari", "social-studies"]
        }

        self.ASSESSEMENTS_ID = {
            "t1":"test1",
            "t2":"test2",
            "a1":"assigment1",
            "a2":"assigment2",
            "m1":"mid",
            "f1":"final",
            "n1":"noteBook"
        }
        self.ID_ASSESSEMENTS = {
            "test1":"t1",
            "test2":"t2",
            "assigment1":"a1",
            "assigment2":"a2",
            "mid":"m1",
            "final":"f1",
            "noteBook":"n1"
        }
        self.MAPED_KEY = ["Grade4-6", "Grade7-8", "Grade-All"]

        self.GENERAL_ID = {  # Mapping of grade ranges to grade IDs
            "Grade4-6": ["G4","G5","G6"],
            "Grade7-8": ["G7","G8"],
            "Grade-All":["G4","G5","G6","G7","G8"]
        }
        self.COURSE_TAKE_BY_GRADE = {  # Mapping of grades to courses they take
            self.MAPED_KEY[0]: [
                "a-mharic", "a-fanoromo", "s-cience", "m-aths", "e-nglish",
                "i-ct", "h-arari"
            ],
            self.MAPED_KEY[1]: [
                "a-mharic", "a-fanoromo", "m-aths", "e-nglish", "i-ct",
                "general-science", "c-te", "citizen-ship", "social-studies"
            ],
            self.MAPED_KEY[2]:[
                "a-mharic", "a-fanoromo",
                "m-aths", "e-nglish", "i-ct"
            ]
        }
