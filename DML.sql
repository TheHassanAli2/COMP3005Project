-- Inserting sample data into the Trainer table
INSERT INTO Trainer (email, password, name, phone, expertise_area) VALUES
('se@example.com', 'password123', 'Sanjeev Easparan', '123-456-7890', 'Weightlifting'),
('ln@example.com', 'password456', 'Lou Nel', '987-654-3210', 'Yoga'),
('sb@example.com', 'password789', 'Sean Benjamin', '564-789-1234', 'Cardio Fitness');

-- Inserting sample data into the Member table
INSERT INTO Member (email, password, name, phone, date_of_birth) VALUES
('h@', 'p', 'Hassan Ali', '321-654-9870', '1990-05-15'),
('lucys@example.com', 'mypassword', 'Tim Dao', '456-123-7890', '1985-10-22'),
('janetk@example.com', 'janetpass', 'Tanner Farkas', '654-321-4567', '1975-03-09');

-- Inserting sample data into the Admin table
INSERT INTO Admin (email, password, name, phone) VALUES
('admin1@example.com', 'adminpass1', 'Admin One', '800-123-4567'),
('admin2@example.com', 'adminpass2', 'Admin Two', '800-765-4321');

-- Inserting sample data into the Metrics table
INSERT INTO Metrics (member_id, weight, height, bmi) VALUES
(1, 180, 170, 26.6),
(2, 140, 165, 24.1),
(3, 200, 183, 26.3);

-- Inserting sample data into the FitnessGoal table
INSERT INTO FitnessGoal (member_id, target_weight, target_time, other_goals, completed) VALUES
(1, 175, '2024-12-31', 'Increase muscle mass', 0::BIT),
(2, 130, '2024-06-30', 'Improve endurance', 0::BIT);

-- Inserting sample data into the Statistics table
INSERT INTO Statistics (member_id, calories_burned, avg_heart_rate, max_heart_rate, ml_water_consumed, date_measured) VALUES
(1, 500, 120, 150, 1500, '2024-04-10'),
(1, 400, 123, 140, 1800, '2024-04-11'),
(2, 450, 110, 140, 1600, '2024-04-09');
-- Inserting sample data into the AvailableTimeslot table
INSERT INTO AvailableTimeslot (trainer_id, booked, date, start_time) VALUES
(1,1::BIT,'2024-04-13','08:00:00'),
(1,0::BIT,'2024-04-13','09:00:00'),
(1,0::BIT,'2024-04-13','15:00:00'),
(1,0::BIT,'2024-04-13','16:00:00'),
(2,0::BIT,'2024-04-13','08:00:00'),
(2,0::BIT,'2024-04-13','09:00:00'),
(2,0::BIT,'2024-04-13','15:00:00'),
(2,0::BIT,'2024-04-13','16:00:00');


-- Inserting sample data into the Equipment table
INSERT INTO Equipment (equipment_name, maintenance_cost, maintenance_date, status) VALUES
('Treadmill', 100, '2023-12-01', 'in service'),
('Dumbbell Set', 50, '2023-11-01', 'needs repair');

-- Inserting sample data into the ExerciseRoutine table
INSERT INTO ExerciseRoutine (member_id, date, description, duration_minutes) VALUES
(1, '2023-12-03', 'Cardio routine: Warmup, then do 10 intervals of 30 second sprint, 1 minute jog', 25),
(2, '2023-12-03', 'Stretching routine: 30 hamstring stretches, 3 sets of 30 second upside-down dog, 30 second cobra stretch, ...', 45);

-- Inserting sample data into the Room table
INSERT INTO Room (room_name, capacity) VALUES
('Room A', 20),
('Room B', 15),
('Room C', 15);

-- Inserting sample data into the RoomBooking table
INSERT INTO RoomBooking (room_id, start_time, purpose) VALUES
(1, '2024-04-13 15:00:00', 'Yoga Class'),
(3,'2024-04-13 08:00:00','Personal Trainer session for Sanjeev Easparan and Hassan Ali'),
(2, '2024-04-13 16:00:00', 'Pilates Class');

-- Inserting sample data into the GroupClass table
INSERT INTO GroupClass (trainer_id, class_name, date, start_time, capacity, remaining_capacity, booking_id) VALUES
(1, 'Yoga Class', '2024-04-13', '15:00:00', 20, 1, 1),
(2, 'Pilates Class', '2024-04-13', '16:00:00', 15, 2, 2);

-- Inserting sample data into the GroupRegistration table
INSERT INTO GroupRegistration (class_id, member_id) VALUES
(2,1),
(2,2);

-- Inserting sample data into the PersonalTrainingSession table
INSERT INTO PersonalTrainingSession (member_id, trainer_id, date, start_time, booking_id) VALUES
(1,1,'2024-04-13','08:00:00',3);


-- Inserting sample data into the Billing table
INSERT INTO Billing (member_id, admin_id, amount, billing_date, payment_date, purpose) VALUES
(1,NULL,25,'2024-04-13',NULL,'Enrolled in group class: Pilates Class'),
(1,NULL,50,'2024-04-13',NULL,'personal training session with se@example.com on 2024-04-13 at 08:00:00'),
(1,NULL,25,'2024-04-13',NULL,'Enrolled in group class: Pilates Class');