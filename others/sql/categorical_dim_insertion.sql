INSERT INTO asset_dim (asset_id, asset_type) VALUES
('crk', 'Cracking'),
('pth', 'Potholes & Depressions'),
('def', 'Surface Deformations'),
('sfd', 'Surface Defects'),
('jnt', 'Joint Failures'),
('drn', 'Drainage Issues'),
('shd', 'Shoulder Defects'),
('wcr', 'Wear & Corrosion'),
('utd', 'Utility Damage'),
('str', 'Structural Failures');

-- Orchard Road
INSERT INTO location_dim (location_id, location, zone, lamppost_id, road_type) VALUES
('or1A', 'Orchard Road', 'SE1', '1A', 'Major Shopping Street'),
('or1B', 'Orchard Road', 'SE1', '1B', 'Major Shopping Street'),
('or1C', 'Orchard Road', 'SE1', '1C', 'Major Shopping Street'),
('or1D', 'Orchard Road', 'SE1', '1D', 'Major Shopping Street'),
('or1E', 'Orchard Road', 'SE1', '1E', 'Major Shopping Street'),
('or1F', 'Orchard Road', 'SE1', '1F', 'Major Shopping Street'),
('or2A', 'Orchard Road', 'SE1', '2A', 'Major Shopping Street'),
('or2B', 'Orchard Road', 'SE1', '2B', 'Major Shopping Street'),
('or2C', 'Orchard Road', 'SE1', '2C', 'Major Shopping Street'),
('or2D', 'Orchard Road', 'SE1', '2D', 'Major Shopping Street'),
('or2E', 'Orchard Road', 'SE1', '2E', 'Major Shopping Street'),
('or2F', 'Orchard Road', 'SE1', '2F', 'Major Shopping Street');

-- Marine Parade
INSERT INTO location_dim (location_id, location, zone, lamppost_id, road_type) VALUES
('mp1A', 'Marine Parade', 'SE2', '1A', 'Residential Area Road'),
('mp1B', 'Marine Parade', 'SE2', '1B', 'Residential Area Road'),
('mp1C', 'Marine Parade', 'SE2', '1C', 'Residential Area Road'),
('mp1D', 'Marine Parade', 'SE2', '1D', 'Residential Area Road'),
('mp1E', 'Marine Parade', 'SE2', '1E', 'Residential Area Road'),
('mp1F', 'Marine Parade', 'SE2', '1F', 'Residential Area Road'),
('mp2A', 'Marine Parade', 'SE2', '2A', 'Residential Area Road'),
('mp2B', 'Marine Parade', 'SE2', '2B', 'Residential Area Road'),
('mp2C', 'Marine Parade', 'SE2', '2C', 'Residential Area Road'),
('mp2D', 'Marine Parade', 'SE2', '2D', 'Residential Area Road'),
('mp2E', 'Marine Parade', 'SE2', '2E', 'Residential Area Road'),
('mp2F', 'Marine Parade', 'SE2', '2F', 'Residential Area Road');

-- Raffles Place
INSERT INTO location_dim (location_id, location, zone, lamppost_id, road_type) VALUES
('rp1A', 'Raffles Place', 'SE', '1A', 'Central Business District Road'),
('rp1B', 'Raffles Place', 'SE', '1B', 'Central Business District Road'),
('rp1C', 'Raffles Place', 'SE', '1C', 'Central Business District Road'),
('rp1D', 'Raffles Place', 'SE', '1D', 'Central Business District Road'),
('rp1E', 'Raffles Place', 'SE', '1E', 'Central Business District Road'),
('rp1F', 'Raffles Place', 'SE', '1F', 'Central Business District Road'),
('rp2A', 'Raffles Place', 'SE', '2A', 'Central Business District Road'),
('rp2B', 'Raffles Place', 'SE', '2B', 'Central Business District Road'),
('rp2C', 'Raffles Place', 'SE', '2C', 'Central Business District Road'),
('rp2D', 'Raffles Place', 'SE', '2D', 'Central Business District Road'),
('rp2E', 'Raffles Place', 'SE', '2E', 'Central Business District Road'),
('rp2F', 'Raffles Place', 'SE', '2F', 'Central Business District Road');

-- East Coast Parkway (ECP)
INSERT INTO location_dim (location_id, location, zone, lamppost_id, road_type) VALUES
('ecp1A', 'East Coast Parkway (ECP)', 'NW1', '1A', 'Expressway'),
('ecp1B', 'East Coast Parkway (ECP)', 'NW1', '1B', 'Expressway'),
('ecp1C', 'East Coast Parkway (ECP)', 'NW1', '1C', 'Expressway'),
('ecp1D', 'East Coast Parkway (ECP)', 'NW1', '1D', 'Expressway'),
('ecp1E', 'East Coast Parkway (ECP)', 'NW1', '1E', 'Expressway'),
('ecp1F', 'East Coast Parkway (ECP)', 'NW1', '1F', 'Expressway'),
('ecp2A', 'East Coast Parkway (ECP)', 'NW1', '2A', 'Expressway'),
('ecp2B', 'East Coast Parkway (ECP)', 'NW1', '2B', 'Expressway'),
('ecp2C', 'East Coast Parkway (ECP)', 'NW1', '2C', 'Expressway'),
('ecp2D', 'East Coast Parkway (ECP)', 'NW1', '2D', 'Expressway'),
('ecp2E', 'East Coast Parkway (ECP)', 'NW1', '2E', 'Expressway'),
('ecp2F', 'East Coast Parkway (ECP)', 'NW1', '2F', 'Expressway');

-- Sentosa
INSERT INTO location_dim (location_id, location, zone, lamppost_id, road_type) VALUES
('st1A', 'Sentosa', 'NE2', '1A', 'Resort Road'),
('st1B', 'Sentosa', 'NE2', '1B', 'Resort Road'),
('st1C', 'Sentosa', 'NE2', '1C', 'Resort Road'),
('st1D', 'Sentosa', 'NE2', '1D', 'Resort Road'),
('st1E', 'Sentosa', 'NE2', '1E', 'Resort Road'),
('st1F', 'Sentosa', 'NE2', '1F', 'Resort Road'),
('st2A', 'Sentosa', 'NE2', '2A', 'Resort Road'),
('st2B', 'Sentosa', 'NE2', '2B', 'Resort Road'),
('st2C', 'Sentosa', 'NE2', '2C', 'Resort Road'),
('st2D', 'Sentosa', 'NE2', '2D', 'Resort Road'),
('st2E', 'Sentosa', 'NE2', '2E', 'Resort Road'),
('st2F', 'Sentosa', 'NE2', '2F', 'Resort Road');
