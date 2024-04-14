SELECT trainer_id, class_name, date, start_time, end_time, capacity, remaining_capacity, booking_id
FROM GroupClass gc
Natural JOIN GroupRegistration gr
WHERE gr.member_id = 1;