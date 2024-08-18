
import string
import db_manager as db
from settings import Settings
SECTION = list(enumerate(string.ascii_uppercase, start=1))
#print(SECTION)

var = Settings()
var.variables()

table = "teacher"
dic = var.TABLE_ATTRIBUTE[table.upper()]


#print(f"grade {grade}")
#_attributeb = [1,3,4,6]
#print(db.get_section_by_id(_attributeb[1]))
#new_list = [dic,attribute]
#print(new_list)
'''for key,item in new_list[0].items():
    print(key,item)'''
#print(var.RABDOM_ID)
'''
def attendance_analysis(student_records, attendance_records):
    attendance_count = {student[1]: {"present": 0, "absent": 0} for student in student_records}

    for record in attendance_records:
        for student in student_records:
            if record[0] == student[0]:
                if record[1] == "present":
                    attendance_count[student[1]]["present"] += 1
                elif record[1] == "absent":
                    attendance_count[student[1]]["absent"] += 1

    for student, attendance in attendance_count.items():
        total_classes = attendance["present"] + attendance["absent"]
        if total_classes == 0:
            attendance_percentage = 0
        else:
            attendance_percentage = (attendance["present"] / total_classes) * 100
        print(f"{student}: {attendance_percentage:.2f}% attendance")



absent_students_with_name = []

student = [[123, "mati"], [156, "nina"], [177, "ali"]]

attendance = [
    [123, "absent", "02/05/2024"],
    [123, "present", "03/05/2024"],
    [123, "absent", "04/05/2024"],
    [156, "present", "02/05/2024"],
    [156, "absent", "03/05/2024"],
    [156, "present", "04/05/2024"],
    [177, "absent", "04/05/2024"],
    [177, "absent", "04/05/2024"],
    [177, "absent", "04/05/2024"]
]

for record in attendance:
    if record[1] == "absent":
        student_id = record[0]
        for s in student:
            if student_id == s[0]:  # Check against the student ID
                absent_students_with_name.append([[s[0],s[1]], record])
attendance_analysis(student, attendance)
print(absent_students_with_name)

columns = ["omer","sjoi","fhsoihf","oifoafoua"]

set_part = ", ".join([f"{column}=%s" for column in columns])
print(set_part)

def get_letter_by_id(id):
    for i, section in SECTION:
        print(i)
        if id == i:
            return section
    return None
# Accessing letter by ID
id = 5
letter = get_letter_by_id(id)
if letter:
    print(f"The letter with ID {id} is {letter}.")
else:
    print("Invalid ID.")
def test_fun(me,you,them="students"):
    print(me,you,them)
test_fun(me="omer",you="love")'''
def get_section_ID_by_letter(_section):
    SECTION = var.SECTION
    for ID, section in SECTION:
        if section.lower() == _section:
            return ID




test = ['naruto uzumaki', [['Ict', [('123', 'f1', '30', 'i-ct', 's1', 'ACZ2', '0A11LC', 'G4', '1'), ('243', 'n1', '10', 'i-ct', 's1', 'ACZ2', '0A11LC', 'G4', '1'), (
'34', 'a1', '10', 'i-ct', 's1', 'ACZ2', '0A11LC', 'G4', '1'), ('343', 'a2', '10', 'i-ct', 's1', 'ACZ2', '0A11LC', 'G4', '1'), ('354', 't1', '10', 'i-ct', 's1'
, 'ACZ2', '0A11LC', 'G4', '1'), ('357', 'm1', '20', 'i-ct', 's1', 'ACZ2', '0A11LC', 'G4', '1'), ('436', 't2', '10', 'i-ct', 's1', 'ACZ2', '0A11LC', 'G4', '1')
]],['rt',[(1,1,1),(1,1,1),(1,1,1,1),(1,1)]]], 'Empty no data yet!']

test_ = test[1]
test_sl = test_[0]
test_s = test_sl[0]
test_sl_ = test_sl

GradeID = "G7"

if GradeID in var.GENERAL_ID[var.MAPED_KEY[0]]:
    print(var.MAPED_KEY[0])
