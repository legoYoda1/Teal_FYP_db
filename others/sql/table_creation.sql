-- Date Table
CREATE TABLE date_dim (
    date_id INTEGER PRIMARY KEY,
    day INTEGER CHECK (day BETWEEN 1 AND 31),
    month INTEGER CHECK (month BETWEEN 1 AND 12),
    year INTEGER CHECK (year BETWEEN 2000 AND 2050)
);

-- Time Table
CREATE TABLE time_dim (
    time_id INTEGER PRIMARY KEY,
    minute INTEGER CHECK (minute BETWEEN 0 AND 59),
    hour INTEGER CHECK (hour BETWEEN 0 AND 23)
);

-- Location Table
CREATE TABLE location_dim (
    location_id TEXT PRIMARY KEY,
    zone TEXT, -- zone refers to both region and zone (SW & SW1)
    location TEXT,
    lamppost_id TEXT,
    road_type TEXT
);

-- Asset Table
CREATE TABLE asset_dim (
    asset_id TEXT PRIMARY KEY,
    asset_type TEXT
);

-- Supervisor Table
CREATE TABLE supervisor_dim (
    supervisor_id INTEGER PRIMARY KEY,
    name TEXT
);

-- Inspector Table
CREATE TABLE inspector_dim (
    inspector_id INTEGER PRIMARY KEY,
    name TEXT
);



-- Main Report Table
CREATE TABLE report_fact (
    report_id INTEGER PRIMARY KEY,
    defect_ref_no TEXT,
    date_id INTEGER,
    time_id INTEGER,
    location_id TEXT,
    asset_id TEXT,
    supervisor_id INTEGER,
    inspector_id INTEGER,
    reported_via_id INTEGER,
    acknowledgement_id INTEGER,
    repeated_defect INTEGER CHECK (repeated_defect IN (0, 1)),
    description TEXT,
    quantity INTEGER,
    measurement INTEGER,
    cause_of_defect TEXT,
    recommendation TEXT,
    report_path TEXT,
    FOREIGN KEY (date_id) REFERENCES date_dim(date_id),
    FOREIGN KEY (time_id) REFERENCES time_dim(time_id),
    FOREIGN KEY (location_id) REFERENCES location_dim(location_id),
    FOREIGN KEY (asset_id) REFERENCES asset_dim(asset_id),
    FOREIGN KEY (supervisor_id) REFERENCES supervisor_dim(supervisor_id),
    FOREIGN KEY (inspector_id) REFERENCES inspector_dim(inspector_id),
    FOREIGN KEY (reported_via_id) REFERENCES reported_via_dim(reported_via_id),
    FOREIGN KEY (acknowledgement_id) REFERENCES acknowledgement_dim(acknowledgement_id)
);


-- -- Reported Via Table
-- CREATE TABLE reported_via_dim (
--     reported_via_id INTEGER PRIMARY KEY,
--     method TEXT,
--     agency TEXT,
--     date_id INTEGER,
--     time_id INTEGER,
--     FOREIGN KEY (date_id) REFERENCES date_dim(date_id),
--     FOREIGN KEY (time_id) REFERENCES time_dim(time_id)
-- );

-- -- Acknowledgement Table
-- CREATE TABLE acknowledgement_dim (
--     acknowledgement_id INTEGER PRIMARY KEY,
--     method TEXT,
--     date_id INTEGER,
--     time_id INTEGER,
--     FOREIGN KEY (date_id) REFERENCES date_dim(date_id),
--     FOREIGN KEY (time_id) REFERENCES time_dim(time_id)
-- );


