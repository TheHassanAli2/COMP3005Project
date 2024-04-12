DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

CREATE TABLE Trainer (
    trainer_id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    expertise_area VARCHAR(255) NOT NULL
);

CREATE TABLE Member (
    member_id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    date_of_birth DATE NOT NULL
);

CREATE TABLE Admin (
    admin_id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL
);

CREATE TABLE Metrics (
    metric_id SERIAL PRIMARY KEY,
    member_id INT REFERENCES Member(member_id),
    weight FLOAT NOT NULL,
    height FLOAT NOT NULL,
    bmi FLOAT NOT NULL
);

CREATE TABLE FitnessGoal (
    goal_id SERIAL PRIMARY KEY,
    member_id INT REFERENCES Member(member_id),
    target_weight FLOAT,
    target_time DATE NOT NULL,
    other_goals TEXT,
    status VARCHAR(255) DEFAULT 'incomplete'
);

CREATE TABLE Statistics (
    stat_id SERIAL PRIMARY KEY,
    member_id INT REFERENCES Member(member_id),
    calories_burned FLOAT,
    avg_heart_rate FLOAT,
    max_heart_rate FLOAT,
    hydration_levels FLOAT,
    date_measured DATE
);

CREATE TABLE AvailableTimeslot (
    tslot_id SERIAL PRIMARY KEY,
    trainer_id INT REFERENCES Trainer(trainer_id),
    date DATE,
    start_time TIME,
    end_time TIME
);

CREATE TABLE Equipment (
    equipment_id SERIAL PRIMARY KEY,
    equipment_name VARCHAR(255),
    maintenance_cost FLOAT,
    maintenance_date DATE,
    status VARCHAR(255) DEFAULT 'in service'
);

CREATE TABLE ExerciseRoutine (
    routine_id SERIAL PRIMARY KEY,
    member_id INT REFERENCES Member(member_id),
    date DATE,
    description TEXT,
    duration_minutes INT
);

CREATE TABLE Room (
    room_id SERIAL PRIMARY KEY,
    room_name VARCHAR(255),
    capacity INT
);

CREATE TABLE RoomBooking (
    booking_id SERIAL PRIMARY KEY,
    room_id INT REFERENCES Room(room_id),
    booking_admin_id INT REFERENCES Admin(admin_id) NULL,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
	purpose TEXT, 
    status VARCHAR(255) DEFAULT 'unconfirmed'
);

CREATE TABLE GroupClass (
    class_id SERIAL PRIMARY KEY,
    trainer_id INT REFERENCES Trainer(trainer_id),
    class_name VARCHAR(255),
    date DATE,
    start_time TIME,
    end_time TIME,
    capacity INT,
    remaining_capacity INT,
    booking_id INT REFERENCES RoomBooking(booking_id)
);

CREATE TABLE GroupRegistration (
    class_id INT REFERENCES GroupClass(class_id),
    member_id INT REFERENCES Member(member_id),
    PRIMARY KEY (class_id, member_id)
);

CREATE TABLE PersonalTrainingSession (
    pt_id SERIAL PRIMARY KEY,
    member_id INT REFERENCES Member(member_id),
    trainer_id INT REFERENCES Trainer(trainer_id),
    date DATE,
    start_time TIME,
    end_time TIME,
    status VARCHAR(255),
    booking_id INT REFERENCES RoomBooking(booking_id)
);

CREATE TABLE Billing (
    billing_id SERIAL PRIMARY KEY,
    member_id INT REFERENCES Member(member_id),
    admin_id INT REFERENCES Admin(admin_id) NULL,
    date DATE,
    amount FLOAT,
	billing_date DATE,
	payment_date DATE,
    payment_status VARCHAR(255) DEFAULT 'unpaid'
);