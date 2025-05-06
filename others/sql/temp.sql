-- Insert into location Table
INSERT INTO location (location_id, location, landmark, road_type)
VALUES ('LOC001', 'Main Street', 'Central Park', 'Paved');

-- Insert into asset Table
INSERT INTO asset (asset_id, asset_type)
VALUES ('AST001', 'Bridge');

-- Insert into supervisor Table (INTEGER PRIMARY KEY auto-increments)
INSERT INTO supervisor (name)
VALUES ('John Doe');

-- Insert into inspector Table (INTEGER PRIMARY KEY auto-increments)
INSERT INTO inspector (name)
VALUES ('Jane Smith');

-- Insert into reported_via Table (INTEGER PRIMARY KEY auto-increments)
INSERT INTO reported_via (method, agency, date_id, time_id)
VALUES ('Phone', 'Agency A', 1, 1);

-- Insert into acknowledgement Table (INTEGER PRIMARY KEY auto-increments)
INSERT INTO acknowledgement (method, date_id, time_id)
VALUES ('Email', 1, 1);

-- Insert into lta_verified_by Table (INTEGER PRIMARY KEY auto-increments)
INSERT INTO lta_verified_by (name, date_id, instructions, wso_no)
VALUES ('Alice Johnson', 1, 'Verify structural integrity', 'WSO123');

-- Insert into contractor_acknowledged_received_by Table (INTEGER PRIMARY KEY auto-increments)
INSERT INTO contractor_acknowledged_received_by (name, date_id)
VALUES ('Bob Williams', 1);

-- Insert into report Table
INSERT INTO report (
    defect_ref_no, date_id, location_id, asset_id, supervisor_id, 
    inspector_id, reported_via_id, acknowledgement_id, lta_verified_by_id, 
    contractor_acknowledged_received_by_id, repeated_defect, description, 
    quantity, measurement, cause_of_defect, reccomendation
)
VALUES (
    'DEF001', 1, 'LOC001', 'AST001', 1, 1, 1, 1, 1, 1, 
    FALSE, 'Crack in the structure', 5, 12, 'Wear and tear', 'Repair and monitor'
);

--------------------------------------------------------------------

-- Insert into location Table
INSERT INTO location (location_id, location, landmark, road_type)
VALUES ('LOC002', 'Broadway Avenue', 'City Hall', 'Asphalt');

-- Insert into asset Table
INSERT INTO asset (asset_id, asset_type)
VALUES ('AST002', 'Road Sign');

-- Insert into supervisor Table (INTEGER PRIMARY KEY auto-increments)
INSERT INTO supervisor (name)
VALUES ('Sarah Lee');

-- Insert into inspector Table (INTEGER PRIMARY KEY auto-increments)
INSERT INTO inspector (name)
VALUES ('Michael Green');

-- Insert into reported_via Table (INTEGER PRIMARY KEY auto-increments)
INSERT INTO reported_via (method, agency, date_id, time_id)
VALUES ('Email', 'Agency B', 1, 2);

-- Insert into acknowledgement Table (INTEGER PRIMARY KEY auto-increments)
INSERT INTO acknowledgement (method, date_id, time_id)
VALUES ('Phone', 1, 2);

-- Insert into lta_verified_by Table (INTEGER PRIMARY KEY auto-increments)
INSERT INTO lta_verified_by (name, date_id, instructions, wso_no)
VALUES ('David Brown', 1, 'Check for faulty wiring', 'WSO456');

-- Insert into contractor_acknowledged_received_by Table (INTEGER PRIMARY KEY auto-increments)
INSERT INTO contractor_acknowledged_received_by (name, date_id)
VALUES ('Emily Clark', 1);

-- Insert into report Table
INSERT INTO report (
    defect_ref_no, date_id, location_id, asset_id, supervisor_id, 
    inspector_id, reported_via_id, acknowledgement_id, lta_verified_by_id, 
    contractor_acknowledged_received_by_id, repeated_defect, description, 
    quantity, measurement, cause_of_defect, reccomendation
)
VALUES (
    'DEF002', 1, 'LOC002', 'AST002', 2, 2, 2, 2, 2, 2, 
    FALSE, 'Faded road sign with unclear instructions', 1, 5, 'Sun exposure and weathering', 'Replace the sign and monitor condition'
);

---

DELETE FROM report;
DELETE FROM contractor_acknowledged_received_by;
DELETE FROM lta_verified_by;
DELETE FROM acknowledgement;
DELETE FROM reported_via;
DELETE FROM inspector;
DELETE FROM supervisor;
DELETE FROM asset;
DELETE FROM location;