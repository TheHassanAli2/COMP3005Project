-- Inserting sample data into the Trainer table
INSERT INTO Trainer (email, password, name, phone, expertise_area) VALUES
('jdoe@example.com', 'password123', 'John Doe', '123-456-7890', 'Weightlifting'),
('asmith@example.com', 'password456', 'Anna Smith', '987-654-3210', 'Yoga'),
('bwhite@example.com', 'password789', 'Bob White', '564-789-1234', 'Cardio Fitness');

-- Inserting sample data into the Member table
INSERT INTO Member (email, password, name, phone, date_of_birth) VALUES
('mikeb@example.com', 'securepass', 'Mike Brown', '321-654-9870', '1990-05-15'),
('lucys@example.com', 'mypassword', 'Lucy Smith', '456-123-7890', '1985-10-22'),
('janetk@example.com', 'janetpass', 'Janet King', '654-321-4567', '1975-03-09');

-- Inserting sample data into the Admin table
INSERT INTO Admin (email, password, name, phone) VALUES
('admin1@example.com', 'adminpass1', 'Alice Johnson', '800-123-4567'),
('admin2@example.com', 'adminpass2', 'Greg Hall', '800-765-4321');

-- Inserting sample data into the Metrics table
INSERT INTO Metrics (member_id, weight, height, bmi) VALUES
(1, 180, 5.9, 26.6),
(2, 140, 5.4, 24.1),
(3, 200, 6.1, 26.3);

-- Inserting sample data into the FitnessGoal table
INSERT INTO FitnessGoal (member_id, target_weight, target_time, other_goals, status) VALUES
(1, 175, '2024-12-31', 'Increase muscle mass', 'incomplete'),
(2, 130, '2024-06-30', 'Improve endurance', 'incomplete');

-- Inserting sample data into the Statistics table
INSERT INTO Statistics (member_id, calories_burned, avg_heart_rate, max_heart_rate, hydration_levels, date_measured) VALUES
(1, 500, 120, 150, 1500, '2023-12-01'),
(2, 450, 110, 140, 1600, '2023-12-01');
-- Inserting sample data into the AvailableTimeslot table
INSERT INTO AvailableTimeslot (trainer_id, date, start_time, end_time) VALUES
(1, '2023-12-05', '08:00:00', '10:00:00'),
(2, '2023-12-05', '10:00:00', '12:00:00');

-- Inserting sample data into the Equipment table
INSERT INTO Equipment (equipment_name, maintenance_cost, maintenance_date, status) VALUES
('Treadmill', 100, '2023-12-01', 'in service'),
('Dumbbell Set', 50, '2023-11-01', 'needs repair');

-- Inserting sample data into the ExerciseRoutine table
INSERT INTO ExerciseRoutine (member_id, date, description, duration_minutes) VALUES
(1, '2023-12-03', 'Cardio routine', 60),
(2, '2023-12-03', 'Strength training', 45);

-- Inserting sample data into the Room table
INSERT INTO Room (room_name, capacity) VALUES
('Room A', 20),
('Room B', 15);

-- Inserting sample data into the RoomBooking table
INSERT INTO RoomBooking (room_id, booking_admin_id, start_time, end_time, purpose, status) VALUES
(1, 1, '2023-12-05 09:00:00', '2023-12-05 11:00:00', 'Yoga Class', 'confirmed'),
(2, null, '2023-12-05 12:00:00', '2023-12-05 14:00:00', 'Pilates Class', 'unconfirmed');

-- Inserting sample data into the GroupClass table
INSERT INTO GroupClass (trainer_id, class_name, date, start_time, end_time, capacity, remaining_capacity, booking_id) VALUES
(1, 'Yoga Class', '2023-12-07', '09:00:00', '11:00:00', 20, 20, 1),
(2, 'Pilates Class', '2023-12-07', '12:00:00', '14:00:00', 15, 15, 2);

-- Inserting sample data into the GroupRegistration table
INSERT INTO GroupRegistration (class_id, member_id) VALUES
(1, 1),
(1, 2);

-- Inserting sample data into the PersonalTrainingSession table
INSERT INTO PersonalTrainingSession (member_id, trainer_id, date, start_time, end_time, status, booking_id) VALUES
(1, 1, '2023-12-10', '10:00:00', '11:00:00', 'scheduled', 1),
(2, 2, '2023-12-10', '11:00:00', '12:00:00', 'scheduled', 2);
-- Inserting sample data into the Billing table
INSERT INTO Billing (member_id, admin_id, date, amount, billing_date, payment_date, payment_status) VALUES
(1, 1, '2023-12-01', 100.0, '2023-12-01', '2023-12-15', 'paid'),
(2, 1, '2023-12-01', 150.0, '2023-12-01', '2023-12-15', 'unpaid');