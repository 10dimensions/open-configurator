-- Product Categories for Bicycle
INSERT INTO product_categories (id, name, description) VALUES
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Frame', 'Bicycle frames of various materials and sizes'),
    ('b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a12', 'Wheels', 'Wheel sets including tires and tubes'),
    ('c2eebc99-9c0b-4ef8-bb6d-6bb9bd380a13', 'Drivetrain', 'Components for power transmission including chain, cassette, and derailleurs'),
    ('d3eebc99-9c0b-4ef8-bb6d-6bb9bd380a14', 'Brakes', 'Braking systems and components'),
    ('e4eebc99-9c0b-4ef8-bb6d-6bb9bd380a15', 'Cockpit', 'Handlebars, stems, and related controls');

-- Components
INSERT INTO components (id, category_id, name, sku, description, base_price, attributes) VALUES
    -- Frames
    ('f5eebc99-9c0b-4ef8-bb6d-6bb9bd380a16', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Carbon Race Frame', 'FRM-CBN-001', 
    'Lightweight carbon fiber race frame', 1499.99, 
    '{"material": "carbon", "sizes": ["52cm", "54cm", "56cm"], "weight": "980g", "type": "road"}'),
    
    ('f6eebc99-9c0b-4ef8-bb6d-6bb9bd380a17', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Aluminum MTB Frame', 'FRM-ALU-001', 
    'Durable aluminum mountain bike frame', 699.99, 
    '{"material": "aluminum", "sizes": ["S", "M", "L"], "weight": "1500g", "type": "mountain"}'),
    
    -- Wheels
    ('f7eebc99-9c0b-4ef8-bb6d-6bb9bd380a18', 'b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a12', 'Carbon Road Wheelset', 'WHL-CBN-001', 
    'Lightweight carbon fiber road wheels', 999.99, 
    '{"material": "carbon", "size": "700c", "type": "road", "weight": "1400g", "tubeless_ready": true}'),
    
    ('f8eebc99-9c0b-4ef8-bb6d-6bb9bd380a19', 'b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a12', 'MTB Wheelset', 'WHL-MTB-001', 
    'Sturdy mountain bike wheelset', 449.99, 
    '{"material": "aluminum", "size": "29inch", "type": "mountain", "weight": "1800g", "tubeless_ready": true}'),
    
    -- Drivetrain Components
    ('f9eebc99-9c0b-4ef8-bb6d-6bb9bd380a20', 'c2eebc99-9c0b-4ef8-bb6d-6bb9bd380a13', 'Road Groupset Pro', 'DRT-ROD-001', 
    'High-end road bike groupset', 1299.99, 
    '{"speeds": 12, "type": "road", "material": "carbon/aluminum", "weight": "2.1kg"}'),
    
    ('faeebc99-9c0b-4ef8-bb6d-6bb9bd380a21', 'c2eebc99-9c0b-4ef8-bb6d-6bb9bd380a13', 'MTB Groupset Elite', 'DRT-MTB-001', 
    'Professional mountain bike groupset', 899.99, 
    '{"speeds": 12, "type": "mountain", "material": "aluminum", "weight": "2.4kg"}');

-- Compatibility Rules
INSERT INTO compatibility_rules (id, name, description, rule_type, component_id, related_component_id, condition_expression) VALUES
    -- Road Frame + Road Wheels compatibility
    ('fbeebc99-9c0b-4ef8-bb6d-6bb9bd380a22', 'Road Frame-Wheel Compatibility', 
    'Carbon Race Frame requires road-specific wheels', 
    'REQUIRES', 
    'f5eebc99-9c0b-4ef8-bb6d-6bb9bd380a16', -- Carbon Race Frame
    'f7eebc99-9c0b-4ef8-bb6d-6bb9bd380a18', -- Carbon Road Wheelset
    '{"rule": "type_match", "message": "Road frames must use road wheels"}'),

    -- MTB Frame + MTB Wheels compatibility
    ('fceebc99-9c0b-4ef8-bb6d-6bb9bd380a23', 'MTB Frame-Wheel Compatibility',
    'Aluminum MTB Frame requires MTB-specific wheels',
    'REQUIRES',
    'f6eebc99-9c0b-4ef8-bb6d-6bb9bd380a17', -- Aluminum MTB Frame
    'f8eebc99-9c0b-4ef8-bb6d-6bb9bd380a19', -- MTB Wheelset
    '{"rule": "type_match", "message": "Mountain bike frames must use MTB wheels"}'),

    -- Road Frame + Road Groupset compatibility
    ('fdeebc99-9c0b-4ef8-bb6d-6bb9bd380a24', 'Road Frame-Groupset Compatibility',
    'Carbon Race Frame requires road-specific groupset',
    'REQUIRES',
    'f5eebc99-9c0b-4ef8-bb6d-6bb9bd380a16', -- Carbon Race Frame
    'f9eebc99-9c0b-4ef8-bb6d-6bb9bd380a20', -- Road Groupset Pro
    '{"rule": "type_match", "message": "Road frames must use road groupset"}'),

    -- MTB Frame + MTB Groupset compatibility
    ('feccbc99-9c0b-4ef8-bb6d-6bb9bd380a25', 'MTB Frame-Groupset Compatibility',
    'Aluminum MTB Frame requires MTB-specific groupset',
    'REQUIRES',
    'f6eebc99-9c0b-4ef8-bb6d-6bb9bd380a17', -- Aluminum MTB Frame
    'faeebc99-9c0b-4ef8-bb6d-6bb9bd380a21', -- MTB Groupset Elite
    '{"rule": "type_match", "message": "Mountain bike frames must use MTB groupset"}'),

    -- Exclusion rules
    ('ffeebc99-9c0b-4ef8-bb6d-6bb9bd380a26', 'Road-MTB Wheel Exclusion',
    'Road Frame cannot use MTB wheels',
    'EXCLUDES',
    'f5eebc99-9c0b-4ef8-bb6d-6bb9bd380a16', -- Carbon Race Frame
    'f8eebc99-9c0b-4ef8-bb6d-6bb9bd380a19', -- MTB Wheelset
    '{"rule": "type_mismatch", "message": "Road frames cannot use MTB wheels"}');

-- Sample Configurations
INSERT INTO configurations (id, name, description, base_component_id, configuration_data, total_price, status) VALUES
    -- Pro Road Bike Build
    ('b0aabc99-9c0b-4ef8-bb6d-6bb9bd380b11', 
    'Pro Road Racing Build', 
    'Lightweight carbon road bike configuration for competitive racing',
    'f5eebc99-9c0b-4ef8-bb6d-6bb9bd380a16', -- Carbon Race Frame
    '{
        "frame_size": "54cm",
        "color_scheme": "matte black/red",
        "build_purpose": "racing",
        "rider_height": "175cm"
    }',
    3799.97,
    'COMPLETE'),

    -- Trail MTB Build
    ('b1aabc99-9c0b-4ef8-bb6d-6bb9bd380b12',
    'Trail Destroyer MTB', 
    'All-mountain trail bike configuration with durability focus',
    'f6eebc99-9c0b-4ef8-bb6d-6bb9bd380a17', -- Aluminum MTB Frame
    '{
        "frame_size": "M",
        "color_scheme": "forest green",
        "build_purpose": "trail riding",
        "rider_height": "170cm"
    }',
    2049.97,
    'COMPLETE'),

    -- Custom Road Build (Draft)
    ('b2aabc99-9c0b-4ef8-bb6d-6bb9bd380b13',
    'Custom Endurance Road', 
    'Custom road bike build for long-distance comfort',
    'f5eebc99-9c0b-4ef8-bb6d-6bb9bd380a16', -- Carbon Race Frame
    '{
        "frame_size": "56cm",
        "color_scheme": "blue/white",
        "build_purpose": "endurance",
        "rider_height": "183cm"
    }',
    3799.97,
    'DRAFT');

-- Configuration Components (relating components to configurations)
INSERT INTO configuration_components (id, configuration_id, component_id, quantity, unit_price, attributes) VALUES
    -- Pro Road Racing Build Components
    ('c0aabc99-9c0b-4ef8-bb6d-6bb9bd380c11',
    'b0aabc99-9c0b-4ef8-bb6d-6bb9bd380b11', -- Pro Road Racing Build
    'f5eebc99-9c0b-4ef8-bb6d-6bb9bd380a16', -- Carbon Race Frame
    1,
    1499.99,
    '{"size": "54cm", "color": "matte black/red"}'),

    ('c1aabc99-9c0b-4ef8-bb6d-6bb9bd380c12',
    'b0aabc99-9c0b-4ef8-bb6d-6bb9bd380b11', -- Pro Road Racing Build
    'f7eebc99-9c0b-4ef8-bb6d-6bb9bd380a18', -- Carbon Road Wheelset
    1,
    999.99,
    '{"tire_pressure": "100psi", "tubeless_setup": true}'),

    ('c2aabc99-9c0b-4ef8-bb6d-6bb9bd380c13',
    'b0aabc99-9c0b-4ef8-bb6d-6bb9bd380b11', -- Pro Road Racing Build
    'f9eebc99-9c0b-4ef8-bb6d-6bb9bd380a20', -- Road Groupset Pro
    1,
    1299.99,
    '{"crank_length": "172.5mm", "cassette_range": "11-30T"}'),

    -- Trail MTB Build Components
    ('c3aabc99-9c0b-4ef8-bb6d-6bb9bd380c14',
    'b1aabc99-9c0b-4ef8-bb6d-6bb9bd380b12', -- Trail Destroyer MTB
    'f6eebc99-9c0b-4ef8-bb6d-6bb9bd380a17', -- Aluminum MTB Frame
    1,
    699.99,
    '{"size": "M", "color": "forest green"}'),

    ('c4aabc99-9c0b-4ef8-bb6d-6bb9bd380c15',
    'b1aabc99-9c0b-4ef8-bb6d-6bb9bd380b12', -- Trail Destroyer MTB
    'f8eebc99-9c0b-4ef8-bb6d-6bb9bd380a19', -- MTB Wheelset
    1,
    449.99,
    '{"tire_pressure": "25psi", "tubeless_setup": true}'),

    ('c5aabc99-9c0b-4ef8-bb6d-6bb9bd380c16',
    'b1aabc99-9c0b-4ef8-bb6d-6bb9bd380b12', -- Trail Destroyer MTB
    'faeebc99-9c0b-4ef8-bb6d-6bb9bd380a21', -- MTB Groupset Elite
    1,
    899.99,
    '{"crank_length": "175mm", "cassette_range": "10-52T"}'),

    -- Custom Road Build Components (Draft)
    ('c6aabc99-9c0b-4ef8-bb6d-6bb9bd380c17',
    'b2aabc99-9c0b-4ef8-bb6d-6bb9bd380b13', -- Custom Endurance Road
    'f5eebc99-9c0b-4ef8-bb6d-6bb9bd380a16', -- Carbon Race Frame
    1,
    1499.99,
    '{"size": "56cm", "color": "blue/white"}'),

    ('c7aabc99-9c0b-4ef8-bb6d-6bb9bd380c18',
    'b2aabc99-9c0b-4ef8-bb6d-6bb9bd380b13', -- Custom Endurance Road
    'f7eebc99-9c0b-4ef8-bb6d-6bb9bd380a18', -- Carbon Road Wheelset
    1,
    999.99,
    '{"tire_pressure": "90psi", "tubeless_setup": true}'),

    ('c8aabc99-9c0b-4ef8-bb6d-6bb9bd380c19',
    'b2aabc99-9c0b-4ef8-bb6d-6bb9bd380b13', -- Custom Endurance Road
    'f9eebc99-9c0b-4ef8-bb6d-6bb9bd380a20', -- Road Groupset Pro
    1,
    1299.99,
    '{"crank_length": "175mm", "cassette_range": "11-34T"}');