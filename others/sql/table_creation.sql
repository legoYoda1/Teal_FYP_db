-- Date Table
CREATE TABLE date_dim (
    date_id INT PRIMARY KEY,
    day INT CHECK (day BETWEEN 1 AND 31),
    month INT CHECK (month BETWEEN 1 AND 12),
    year INT CHECK (year BETWEEN 2000 AND 2050)
);

-- Time Table
CREATE TABLE time_dim (
    time_id INT PRIMARY KEY,
    minute INT CHECK (minute BETWEEN 0 AND 59),
    hour INT CHECK (hour BETWEEN 0 AND 23)
);

-- Location Table
CREATE TABLE location (
    location_id VARCHAR(10) PRIMARY KEY,
    location VARCHAR(255),
    landmark VARCHAR(255),
    road_type VARCHAR(100)
);

-- Asset Table
CREATE TABLE asset (
    asset_id VARCHAR(10) PRIMARY KEY,
    asset_type VARCHAR(100)
);

-- Supervisor Table
CREATE TABLE supervisor (
    supervisor_id SERIAL PRIMARY KEY,
    name VARCHAR(255)
);

-- Inspector Table
CREATE TABLE inspector (
    inspector_id SERIAL PRIMARY KEY,
    name VARCHAR(255)
);

-- Reported Via Table
CREATE TABLE reported_via (
    reported_via_id SERIAL PRIMARY KEY,
    method VARCHAR(100),
    agency VARCHAR(100),
    date_id INT,
    time_id INT,
    FOREIGN KEY (date_id) REFERENCES date_dim(date_id),
    FOREIGN KEY (time_id) REFERENCES time_dim(time_id)
);

-- Acknowledgement Table
CREATE TABLE acknowledgement (
    acknowledgement_id SERIAL PRIMARY KEY,
    method VARCHAR(100),
    date_id INT,
    time_id INT,
    FOREIGN KEY (date_id) REFERENCES date_dim(date_id),
    FOREIGN KEY (time_id) REFERENCES time_dim(time_id)
);

-- LTA Verified By Table
CREATE TABLE lta_verified_by (
    lta_verified_by_id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    date_id INT,
    instructions TEXT,
    wso_no VARCHAR(100), -- stored as string since it's string/int (tbc)
    FOREIGN KEY (date_id) REFERENCES date_dim(date_id)
);

-- Contractor Acknowledged Received By Table
CREATE TABLE contractor_acknowledged_received_by (
    contractor_acknowledged_received_by_id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    date_id INT,
    FOREIGN KEY (date_id) REFERENCES date_dim(date_id)
);

-- Main Report Table
CREATE TABLE report (
    report_id SERIAL PRIMARY KEY,
    defect_ref_no VARCHAR(100),
    date_id INT,
    location_id VARCHAR(10),
    asset_id VARCHAR(10),
    supervisor_id INT,
    inspector_id INT,
    reported_via_id INT,
    acknowledgement_id INT,
    lta_verified_by_id INT,
    contractor_acknowledged_received_by_id INT,
    repeated_defect BOOLEAN,
    description TEXT,
    quantity INT,
    measurement INT,
    cause_of_defect TEXT,
    reccomendation TEXT,
    FOREIGN KEY (date_id) REFERENCES date_dim(date_id),
    FOREIGN KEY (location_id) REFERENCES location(location_id),
    FOREIGN KEY (asset_id) REFERENCES asset(asset_id),
    FOREIGN KEY (supervisor_id) REFERENCES supervisor(supervisor_id),
    FOREIGN KEY (inspector_id) REFERENCES inspector(inspector_id),
    FOREIGN KEY (reported_via_id) REFERENCES reported_via(reported_via_id),
    FOREIGN KEY (acknowledgement_id) REFERENCES acknowledgement(acknowledgement_id),
    FOREIGN KEY (lta_verified_by_id) REFERENCES lta_verified_by(lta_verified_by_id),
    FOREIGN KEY (contractor_acknowledged_received_by_id) REFERENCES contractor_acknowledged_received_by(contractor_acknowledged_received_by_id)
);
