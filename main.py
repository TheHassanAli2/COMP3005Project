import psycopg2

conn = psycopg2.connect(database="3005",
                        host="localhost",
                        user="postgres",
                        password="postgres",
                        port="5432")

cursor = conn.cursor()

#Create database
with conn.cursor() as cursor:
    with open("DDL.sql", "r") as sql_file:
        cursor.execute(sql_file.read())
conn.commit()

cursor = conn.cursor()

#Insert data
with conn.cursor() as cursor:
    with open("DML.sql", "r") as sql_file:
        cursor.execute(sql_file.read())
conn.commit()

cursor = conn.cursor()

def registerMember(email, password, fullname, phonenum, dob):
    cursor.execute(f''' INSERT INTO Member (email, password, name, phone, date_of_birth) VALUES
    ('{email}', '{password}', '{fullname}', '{phonenum}', '{dob}'); ''')
    conn.commit()

def loginMember(email, password):
    cursor.execute(f''' select * from member where email='{email}' and password = '{password}';''')
    results = cursor.fetchall()
    if(len(results) == 1):
        print(f"Signed into {results[0][3]}\n\n")
        memberMenu(results[0][3], results[0][0])
    return False

def updateMemberInfo(id):
    cursor.execute(f''' select * from member where member_id='{id}';''')
    results = cursor.fetchall()
    print("Current profile:\n")
    print(results)
    print("\n\nUpdating info:\n")
    fullname = input("What is your fullname? ")
    email = input("What is your email? ")
    password = input("What is your password? ")
    phonenum = input("What is your phone number (xxx-xxx-xxxx)? ")
    dob = input("What is your date of birth (yyyy-mm-dd)? ")
    cursor.execute(f''' UPDATE member
                    SET email = '{email}', password = '{password}', name = '{fullname}', phone = '{phonenum}', date_of_birth = '{dob}'
                    WHERE member_id = {id};
                    ''')

def updateFitnessGoals(id):
    cursor.execute(f'''select * from fitnessgoal where member_id='{id}';''')
    results = cursor.fetchall()
    print("Current fitness goal:\n")
    print(results)
    print("\n\nUpdating fitness goal:\n")
    targetwt = input("What is your target weight? ")
    deadline = input("When do you want to have completed your goal? ")
    description = input("What are the other parts of your goals for this time? ")
    phonenum = input("What is your phone number (xxx-xxx-xxxx)? ")
    dob = input("What is your date of birth (yyyy-mm-dd)? ")
    cursor.execute(f''' UPDATE member
                    SET email = '{email}', password = '{password}', name = '{fullname}', phone = '{phonenum}', date_of_birth = '{dob}'
                    WHERE member_id = {id};
                    ''')


#Returns all of the students in the students table
def getAllStudents():
    cursor.execute(''' Select * from students;''')
    for i in cursor.fetchall():
        print(i)

#Adds a student to the student table with the given parameters
def addStudent(first_name, last_name, email, enrollment_date):
    cursor.execute(f''' INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES
    ('{first_name}', '{last_name}', '{email}', '{enrollment_date}'); ''')
    conn.commit()

#Updates a student's emial using the parameters
def updateStudentEmail(student_id, new_email):
    cursor.execute(f'''
        UPDATE students
        SET email = '{new_email}'
        WHERE student_id = {student_id};
    ''')
    conn.commit()

#Deletes a student using their id
def deleteStudent(student_id):
    cursor.execute(f'''
        DELETE FROM students
        WHERE student_id = {student_id};
    ''')
    conn.commit()

def memberMenu(name, id):
    choice = "-1"
    while(choice != "0"):
        print()
        choice = input(f"Welcome to the member menu!\nPress 1 to Update personal information\nPress 2 to add fitness goals\nPress 3 to change health metrics\n ")
        print()
        if choice == "1":
            updateMemberInfo(id)
        



#Menu Loop
choice = "-1"
while(choice != "0"):
    print()
    choice = input("Welcome to the Fitness tracker app!\nPress 1 to register as a member\nPress 2 to sign in as a member\nPress 3 to sign in as a Trainer\nPress 4 to sign in as an Admin\nPress 0 to exit: ")
    print()
    if choice == "1":
        fullname = input("What is your fullname? ")
        email = input("What is your email? ")
        password = input("What is your password? ")
        phonenum = input("What is your phone number (xxx-xxx-xxxx)? ")
        dob = input("What is your date of birth (yyyy-mm-dd)? ")
        registerMember(email, password, fullname, phonenum, dob)
        print("Registered, go back to login\n")
        continue
    elif choice == "2":
        email = input("What is your email? ")
        password = input("What is your password? ")
        if(not loginMember(email, password)):
            print("Incorrect email or password, try again\n")
            continue
    elif choice == "3":
        id = input("What is the student's id? ")
        email = input("What is the new email that you'd like to change to? ")
        updateStudentEmail(id, email)
    elif choice == "4":
        id = input("What is the student's id? ")
        deleteStudent(id)
    elif choice == "0":
        print("Exiting...")
        break
    else:
        print("Input a valid choice")

