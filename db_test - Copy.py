import db_manager as db

conn = db.connect()
st = db.Students_info(conn,"grade","G4",False,"1")
a = db.Assessements_ifo(conn,"BHB5",False,"student",sem="s1",CourseID="i-ct")
print(a)
print(db.Attendace_info(conn,"6N61B1",'teacher',False,StudentID="BHB5"))