Creating database in MySQL

-- Create the database:

CREATE  database  ip_project;
USE   ip_project;

--Create the table:

CREATE TABLE compound_data (
    element_name VARCHAR(50),
    element_symbol VARCHAR(10),
    valency INT,
    compound VARCHAR(20),
    compound_name VARCHAR(100),
    structure VARCHAR(50),
    bond_type VARCHAR(20),
    num_elements INT);

-- Insert data into the table:

INSERT INTO compound_data (element_name, element_symbol, valency, compound, compound_name, structure, bond_type, num_elements) VALUES
('Hydrogen', 'H', 1, 'H2O', 'Water', 'Bent', 'Covalent', 2),
('Oxygen', 'O', 6, 'H2O', 'Water', 'Bent', 'Covalent', 2),
('Nitrogen', 'N', 5, 'NH3', 'Ammonia', 'Trigonal Pyramidal', 'Covalent', 2),
('Hydrogen', 'H', 1, 'NH3', 'Ammonia', 'Trigonal Pyramidal', 'Covalent', 2),
('Carbon', 'C', 4, 'CO2', 'Carbon Dioxide', 'Linear', 'Covalent', 2),
('Oxygen', 'O', 6, 'CO2', 'Carbon Dioxide', 'Linear', 'Covalent', 2),
('Carbon', 'C', 4, 'CH4', 'Methane', 'Tetrahedral', 'Covalent', 2),
('Hydrogen', 'H', 1, 'CH4', 'Methane', 'Tetrahedral', 'Covalent', 2),
('Hydrogen', 'H', 1, 'HCl', 'Hydrogen Chloride', 'Linear', 'Covalent', 2),
('Chlorine', 'Cl', 7, 'HCl', 'Hydrogen Chloride', 'Linear', 'Covalent', 2),
('Carbon', 'C', 4, 'C2H6', 'Ethane', 'Tetrahedral', 'Covalent', 2),
('Hydrogen', 'H', 1, 'C2H6', 'Ethane', 'Tetrahedral', 'Covalent', 2);


--To view the table formed:

SELECT * FROM  compound_data;

