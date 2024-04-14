import psycopg2
from datetime import date, timedelta
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

def printPretty(cursor,string):
    rows = cursor.fetchall()
    colnames = [desc[0] for desc in cursor.description]
    filtered_colnames = [name for name in colnames if string not in name]
    filtered_rows = []
    for row in rows:
        filtered_row = []
        for col, val in zip(colnames, row):
            if col in filtered_colnames:
                if val == '0':
                    filtered_row.append("no")
                elif val == '1':
                    filtered_row.append("yes")
                else:
                    filtered_row.append(val)
        filtered_rows.append(filtered_row)
    col_widths = [max(len(str(x)) for x in col) for col in zip(*([filtered_colnames] + filtered_rows))]
    print(' | '.join(name.ljust(width) for name, width in zip(filtered_colnames, col_widths)))
    for row in filtered_rows:
        print(' | '.join(str(val).ljust(width) for val, width in zip(row, col_widths)))



def registerMember(email, password, fullname, phonenum, dob):
    cursor.execute(f''' INSERT INTO Member (email, password, name, phone, date_of_birth) VALUES
    ('{email}', '{password}', '{fullname}', '{phonenum}', '{dob}'); ''')
    conn.commit()
    createBilling(100, f'registration for {fullname}')

def loginMember(email, password):
    cursor.execute(f''' select * from member where email='{email}' and password = '{password}';''')
    results = cursor.fetchall()
    if(len(results) == 1):
        print(f"Signed into {results[0][3]}\n")
        memberMenu(results[0][0])
        return True
    return False

def manageProfile(id):
    print("\nCurrent profile:")
    print("\nAccount info:")
    cursor.execute(f''' select * from member where member_id='{id}';''')
    printPretty(cursor,'id')
    print("\nHealth Metrics:")
    cursor.execute(f''' select * from metrics where member_id ='{id}';''')
    printPretty(cursor,'id')
    print("\nFitness Goal:")
    cursor.execute(f'''select * from fitnessgoal where member_id='{id}' and completed = 0::BIT;''')
    printPretty(cursor,'id')
    choice = input(f"\nWelcome to Profile Management!\nPress 1 to Update personal information\nPress 2 to complete and add a new fitness goal\nPress 3 to change health metrics\nPress 4 to go back\n")
    if choice == "1":
        updateMemberInfo(id)
    elif choice == "2":
        updateFitnessGoals(id)
    elif choice == "3":
        updateHealthMetrics(id)
    elif choice == "4":
        return -1


def updateMemberInfo(id):
    cursor.execute(f''' select * from member where member_id='{id}';''')
    print("Current information:\n")
    printPretty(cursor,'id')
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

def updateHealthMetrics(id):
    cursor.execute(f''' select * from metrics where member_id ='{id}';''')
    print("Current Health Metrics:\n")
    printPretty(cursor,'id')
    print("\n\nUpdating info:\n")
    weight = input("What is your weight? ")
    height = input("What is your height? ")
    bmi = input("What is your bmi? ")
    cursor.execute(f''' UPDATE metrics
                    SET weight = '{weight}', height = '{height}', bmi = '{bmi}'
                    WHERE member_id = {id};
                    ''')

def updateFitnessGoals(id):
    cursor.execute(f'''select * from fitnessgoal where member_id='{id}' and completed = 0::BIT;''')
    print("Current fitness goal:\n")
    printPretty(cursor,'id')
    choice = -1

    print("Completed fitness goal!")

    print("\n\nUpdating fitness goal:\n")
    targetwt = input("What is your new target weight? ")
    deadline = input("When do you want to have completed your new goal? ")
    description = input("What are the other parts of your goals for this deadline? ")
    cursor.execute(f''' UPDATE fitnessgoal
                    SET date_completed = CURRENT_DATE, completed = 1::BIT
                    WHERE member_id = {id} and completed = 0::BIT;
                    ''')
    cursor.execute(f''' INSERT INTO FitnessGoal (member_id, target_weight, target_time, other_goals, completed) VALUES
                    ({id}, {targetwt}, '{deadline}', '{description}', 0::BIT);
                    ''')

def displayDashboard(id):
    print("\nDashboard:")
    print("\nRoutines:")
    cursor.execute(f'''select * from exerciseroutine where member_id = {id};''')
    printPretty(cursor,'id')
    print("\nFitness Achievements:")
    cursor.execute(f'''select * from fitnessgoal where member_id='{id}' and completed = 1::BIT order by date_completed;''')
    printPretty(cursor,'id')
    print("\nHealth Statistics past 7 days:")
    sevendaysago = str(date.today()- timedelta(days=7))
    cursor.execute(f'''select *
                        from statistics
                        where member_id = {id} and date_measured >= '{sevendaysago}';''')
    printPretty(cursor,'id')

def schedulePTSession(id):
    print("\nScheduling Personal Trainer Session:")
    date = input("What date do you want to schedule your session? ")

    cursor.execute(f'''SELECT date, start_time, email, name, phone, expertise_area
                    FROM availabletimeslot natural join trainer where booked = 0::BIT and date = '{date}';''')
    print(f"Possible timeslots for {date} with trainers:\n")
    printPretty(cursor,'id')
    time = input(f"\nWhich of the above times work best for you? (xx:xx:xx) ")
    email = input(f"\nEmail of the trainer you'd like to schedule with? ")

    cursor.execute(f'''SELECT trainer_id
                        FROM trainer where email = '{email}';''')
    trainer_id = cursor.fetchall()[0][0]
    cursor.execute(f''' UPDATE availabletimeslot
                    SET booked = 1::BIT
                    WHERE trainer_id = {trainer_id} and date = '{date}' and start_time = '{time}';
                    ''')
    
    cursor.execute(f'''INSERT INTO PersonalTrainingSession (member_id, trainer_id, date, start_time, booking_id) VALUES
                    ({id}, {trainer_id}, '{date}', '{time}', NULL);''')
    createBilling(50, f'personal training session with {email} on {date} at {time}')

def cancelPTSession(id):
    print("\nPT sessions scheduled:")
    cursor.execute(f'''SELECT date, start_time, email, name, phone, expertise_area
                    FROM personaltrainingsession natural join trainer where member_id = {id};''')
    printPretty(cursor,'id')
    date = input("What is the date of the session you would like to cancel? (yyyy-mm-dd) ")
    time = input(f"\nWhat is the time of the session you would like to cancel? (xx:xx:xx) ")
    email = input(f"\nEmail of the trainer for the session you'd like to cancel? ")

    cursor.execute(f'''SELECT trainer_id
                        FROM trainer where email = '{email}';''')
    trainer_id = cursor.fetchall()[0][0]
    cursor.execute(f''' UPDATE availabletimeslot
                    SET booked = 0::BIT
                    WHERE trainer_id = {trainer_id} and date = '{date}' and start_time = '{time}';
                    ''')

    cursor.execute(f''' DELETE FROM PersonalTrainingSession
            WHERE start_time = '{time}'
            AND date = '{date}'
            AND trainer_id = (
                SELECT trainer_id
                FROM Trainer
                WHERE email = '{email}'
    );''')
    
    choice = input(f"\nWould you like to reschedule (yes/no)? ")
    if(choice == "yes"):
        schedulePTSession(id)
    else:
        pass

def enrollGroupClass(id):
    print("\nGroup classes available:")
    cursor.execute(f'''SELECT gc.class_id, gc.trainer_id, gc.class_name, gc.date, gc.start_time, gc.capacity, gc.remaining_capacity, gc.booking_id
                    FROM GroupClass gc
                    LEFT JOIN GroupRegistration gr ON gc.class_id = gr.class_id
                    AND gr.member_id = {id}
                    WHERE gr.class_id IS NULL
                    AND gc.remaining_capacity > 0
                    ''')
    printPretty(cursor,'id')

    name = input("What is the name of the group class you would like to enroll in? ")

    cursor.execute(f'''SELECT class_id
                        FROM groupclass where class_name = '{name}';''')
    class_id = cursor.fetchall()[0][0]

    cursor.execute(f'''INSERT INTO GroupRegistration (class_id, member_id) VALUES
                    ({class_id}, {id});''')
    
    cursor.execute(f'''UPDATE GroupClass
                    SET remaining_capacity = remaining_capacity - 1
                    WHERE class_id = {class_id};''')
    createBilling(25, f'Enrolled in group class: {name}')

def unenrollGroupClass(id):
    print("\nGroup classes enrolled in:")
    cursor.execute(f'''SELECT class_name, date, start_time, capacity, remaining_capacity
        FROM groupclass 
        Natural JOIN groupregistration 
        WHERE member_id = {id};
        ''')
    printPretty(cursor,'id')
    name = input("What is the name of the group class you would like to unenroll from? ")

    cursor.execute(f'''SELECT class_id
                        FROM groupclass where class_name = '{name}';''')
    class_id = cursor.fetchall()[0][0]
    cursor.execute(f'''DELETE FROM groupregistration
        WHERE class_id = {class_id} AND member_id = {id};''')
    
    cursor.execute(f'''UPDATE GroupClass
                    SET remaining_capacity = remaining_capacity + 1
                    WHERE class_id = {class_id};''')

def memberMenu(id):
    choice = "-1"
    while(choice != "0"):
        print()
        choice = input(f"Welcome to the member menu!\nPress 1 to Manage your profile\nPress 2 to display your dashboard\nPress 3 to schedule personal training sessions\nPress 4 to reschedule or cancel a personal training session\nPress 5 to enroll in a group class\nPress 6 to unenroll from a group class\nPress 0 to exit\n")
        print()
        if choice == "1":
            manageProfile(id)
        elif choice == "2":
            displayDashboard(id)
        elif choice == "3":
            schedulePTSession(id)
        elif choice == "4":
            cancelPTSession(id)
        elif choice == "5":
            enrollGroupClass(id)
        elif choice == "6":
            unenrollGroupClass(id)
        

def trainerMenu(id):
    choice = "-1"
    while(choice != "0"):
        print()
        choice = input(f"Welcome to the trainer menu!\nPress 1 to manage your schedule\nPress 2 to display a member's profile\nPress 0 to exit\n")
        print()
        if choice == "1":
            manageSchedule(id)
        elif choice == "2":
            displayMember()

def displayMember():
    name = input("What is the name of the member whose profile you are trying to view? ")
    cursor.execute(f'''SELECT member_id
                        FROM member where name = '{name}';''')
    member_id = cursor.fetchall()[0][0]
    print("\nAccount info:")
    cursor.execute(f''' select * from member where member_id='{member_id}';''')
    printPretty(cursor,'id')
    print("\nHealth Metrics:")
    cursor.execute(f''' select * from metrics where member_id ='{member_id}';''')
    printPretty(cursor,'id')
    print("\nFitness Goal:")
    cursor.execute(f'''select * from fitnessgoal where member_id='{member_id}' and completed = 0::BIT;''')
    printPretty(cursor,'id')


def addTimeslots(id, date):
    start_time = int(input("What is the starting time that you are available for (put the hour only in 24 hour format, xx)? "))
    end_time = int(input("What is the ending time that you are available for (put the hour only in 24 hour format, xx)? "))

    for time in range(start_time,end_time):
        time_str = str(time)
        if(len(time_str) == 1):
            time_str = "0"+time_str
        cursor.execute(f'''INSERT INTO AvailableTimeslot (trainer_id, booked, date, start_time) VALUES
                            ({id}, 0::BIT, '{date}', '{time_str}:00:00');
        ''')
    conn.commit()

def removeTimeslots(id, date):
    start_time = int(input("What is the starting time that you are no longer available for (put the hour only in 24 hour format, xx)? "))
    end_time = int(input("What is the ending time that you are no longer available for (put the hour only in 24 hour format, xx)? "))

    for time in range(start_time,end_time):
        time_str = str(time)
        if(len(time_str) == 1):
            time_str = "0"+time_str
        try:
            cursor.execute(f'''DELETE from availabletimeslot
                               where start_time = '{time_str}:00:00' and trainer_id = {id} and date = '{date}' and booked = 0::BIT;
            ''')
        except:
            pass
        

def manageSchedule(id):
    print("\nManaging personal schedule:")
    date = input("What date do you want make a schedule for? ")
    print(f"\nPersonal schedule on {date}:")
    cursor.execute(f'''SELECT tslot_id, date, start_time
        FROM availabletimeslot
        WHERE trainer_id = {id} AND date = '{date}' AND booked = 0::BIT;''')
    printPretty(cursor, 'id')
    choice = input("Would you like to add another slot or remove a slot (add, remove)? ")
    if(choice == "add"):
        addTimeslots(id, date)
    elif (choice == "remove"):
        removeTimeslots(id, date)

def loginTrainer(email, password):
    cursor.execute(f''' select * from trainer where email='{email}' and password = '{password}';''')
    results = cursor.fetchall()
    if(len(results) == 1):
        print(f"Signed into {results[0][3]}\n")
        trainerMenu(results[0][0])
        return True
    return False


def loginAdmin(email, password):
    cursor.execute(f''' select * from admin where email='{email}' and password = '{password}';''')
    results = cursor.fetchall()
    if(len(results) == 1):
        print(f"Signed into {results[0][3]}\n")
        adminMenu(results[0][0])
        return True
    return False

def adminMenu(id):
    choice = "-1"
    while(choice != "0"):
        print()
        choice = input(f"Welcome to the admin menu!\nPress 1 to manage room bookings\nPress 2 to monitor equipment maintenance\nPress 3 to update group class schedules\nPress 4 to process billings and payments\nPress 0 to exit\n")
        print()
        if choice == "1":
            manageBookings()
        elif choice == "2":
            maintainEquipment()
        elif choice == "3":
            changeGroupClassSchedules()
        elif choice == "4":
            processPayments(id)
    

def manageBookings():
    print(f"\nBook rooms for personal trainer sessions:")
    cursor.execute(f'''SELECT pts.pt_id, pts.start_time, t.name AS trainer_name, m.name AS member_name
                    FROM PersonalTrainingSession pts
                    JOIN Trainer t ON pts.trainer_id = t.trainer_id
                    JOIN Member m ON pts.member_id = m.member_id
                    WHERE pts.booking_id IS NULL;''')
    printPretty(cursor, '`')
    pt_id = input("What is the id of the personal training session you'd like to book a room for? ")    

    cursor.execute('''SELECT *
                    FROM Room
                    WHERE capacity >= 1;''')
    printPretty(cursor, '`')

    room_id = input("What is the id of the room you'd like to book the personal training session for? ")
    cursor.execute(f'''SELECT t.name AS trainer_name, m.name AS member_name, pts.start_time, pts.date
                    FROM PersonalTrainingSession pts
                    JOIN Trainer t ON pts.trainer_id = t.trainer_id
                    JOIN Member m ON pts.member_id = m.member_id
                    WHERE pts.pt_id = {pt_id};''')
    results = cursor.fetchall()[0]

    cursor.execute(f'''INSERT INTO RoomBooking (room_id, start_time, purpose) VALUES
    ({room_id}, '{results[3]} {results[2]}', 'Personal Trainer session for {results[0]} and {results[1]}')
    RETURNING booking_id;''')
    booking_id = cursor.fetchone()[0]
    cursor.execute(f'''UPDATE PersonalTrainingSession 
                    SET booking_id = {booking_id}
                    WHERE pt_id = {pt_id};''')


def maintainEquipment():
    print(f"\nEquipment status:")
    cursor.execute('''SELECT *
                FROM Equipment;''')
    printPretty(cursor, '`')

    choice = input("Would you like to repair a piece of equipment or report a piece of equipment for being in need of repair (repair, report)? ")
    if(choice == "repair"):
        e_id = input("What is the equipment id of the equipment you are trying to repair? ")
        cost = input("How much did it cost to repair? ")
        cursor.execute(f''' UPDATE Equipment
                        SET status = 'in service', maintenance_cost = {cost}, maintenance_date = CURRENT_DATE
                        WHERE equipment_id = {e_id};
                        ''')
    elif (choice == "report"):
        e_id = input("What is the equipment id of the equipment you are reporting? ")
        cursor.execute(f''' UPDATE Equipment
                        SET status = 'need repair'
                        WHERE equipment_id = {e_id};
                        ''')

def changeGroupClassSchedules(id):
    print(f"\nGroup Classes:")
    cursor.execute('''SELECT *
                FROM groupclass;''')
    printPretty(cursor, '`')

    gc_id = input("What is the group class id of the group class you'd like to reschedule? ")
    cursor.execute(f''' SELECT trainer_id, date, booking_id, capacity
                            FROM GroupClass
                            WHERE class_id = {gc_id};''')
    trainer_id, date, booking_id, capacity = cursor.fetchall()[0]

    print(f"Possible timeslots for that group class and trainer:\n")
    cursor.execute(f''' SELECT *
                        FROM AvailableTimeslot
                        WHERE trainer_id = {trainer_id}
                        AND date = '{date}'
                        AND booked = 0::BIT;''')
    printPretty(cursor, '`')
    ts_id = input("What is the time slot id you'd like to reschedule the group class to? ")

    print(f"Possible rooms:\n")
    cursor.execute(f'''SELECT *
                    FROM Room
                    WHERE capacity >= {capacity};''')
    printPretty(cursor, '`')
    room_id = input("What is the room id you'd like to reschedule the group class to? ")
    
    try:
        cursor.execute(f'''
            UPDATE RoomBooking
            SET room_id = {room_id}, start_time = (
                SELECT start_time
                FROM AvailableTimeslot
                WHERE tslot_id = {ts_id}
            ), booking_id = {booking_id}
            WHERE room_id = {room_id}
            AND tslot_id = {ts_id}
            AND DATE(start_time) = '{date}'
            AND booking_id = {booking_id}
            AND NOT EXISTS (
                SELECT 1
                FROM RoomBooking
                WHERE room_id = {room_id}
                AND start_time = (
                    SELECT start_time
                    FROM AvailableTimeslot
                    WHERE tslot_id = {ts_id}
                )
            );
        ''')
    except:
        pass
    # cursor.execute(f''' DELETE FROM RoomBooking
    #                     WHERE booking_id = {booking_id};
    #                     ''' )

def createBilling(amount, purpose):
    print(f"You have been billed {amount} dollars for {purpose}")
    cursor.execute(f'''INSERT INTO Billing (member_id, admin_id, amount, billing_date, payment_date, purpose) VALUES
    (1, NULL,  {amount}, CURRENT_DATE, NULL, '{purpose}');
    ''')
        

def processPayments(id):
    print("All unpaid billings")
    cursor.execute(f'''SELECT *
                    FROM Billing
                    WHERE payment_date IS NULL;
    ''')
    printPretty(cursor, '`')
    billing_id = input("What is the billing id of the billing you'd like to process? ")

    print("Processing payment...")
    print("Payment paid.")

    cursor.execute(f'''UPDATE Billing
        SET payment_date = CURRENT_DATE, admin_id = {id}
        WHERE billing_id = {billing_id};
    ''')

    pass

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
        email = input("What is your email? ")
        password = input("What is your password? ")
        if(not loginTrainer(email, password)):
            print("Incorrect email or password, try again\n")
            continue
    elif choice == "4":
        email = input("What is your email? ")
        password = input("What is your password? ")
        if(not loginAdmin(email, password)):
            print("Incorrect email or password, try again\n")
            continue
    elif choice == "0":
        print("Exiting...")
        conn.commit()
        break
    else:
        print("Input a valid choice")

