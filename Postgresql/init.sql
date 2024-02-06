-- Create a table
CREATE TABLE IF NOT EXISTS my_table1 (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Insert data into the table
INSERT INTO my_table1 (name) VALUES
('John'),
('Jane'),
('Alice');
