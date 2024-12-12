-- Create the database
CREATE DATABASE TaxiBookingSystem;
USE TaxiBookingSystem;


CREATE TABLE Customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255),
    phone_number VARCHAR(15) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE
);


CREATE TABLE Drivers (
    driver_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(15) NOT NULL UNIQUE,
    numberplate_color VARCHAR(255),
    availability_status BOOLEAN DEFAULT TRUE
);


CREATE TABLE Administrators (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);


CREATE TABLE Bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    pickup_location VARCHAR(255) NOT NULL,
    dropoff_location VARCHAR(255) NOT NULL,
    booking_date DATE NOT NULL,
    booking_time TIME NOT NULL,
    status ENUM('Pending', 'Assigned', 'Cancelled', 'Completed') DEFAULT 'Pending',
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE
);


CREATE TABLE DriverAssignments (
    assignment_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    driver_id INT NOT NULL,
    assignment_date DATE NOT NULL,
    FOREIGN KEY (booking_id) REFERENCES Bookings(booking_id) ON DELETE CASCADE,
    FOREIGN KEY (driver_id) REFERENCES Drivers(driver_id) ON DELETE CASCADE,
    UNIQUE (booking_id, driver_id) -- Ensure no duplicate assignments
);




CREATE TABLE LoginCredentials (
    login_id INT AUTO_INCREMENT PRIMARY KEY,
    user_role ENUM('Customer', 'Driver', 'Administrator') NOT NULL,
    user_id INT NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Customers(customer_id) ON DELETE CASCADE,
    UNIQUE (user_id, user_role, username)
);

drop table LoginCredentials;

ALTER TABLE LoginCredentials ADD COLUMN password VARCHAR(255) NOT NULL;

CREATE TABLE LoginCredentials (
    login_id INT AUTO_INCREMENT PRIMARY KEY,
    user_role ENUM('Customer', 'Driver', 'Administrator') NOT NULL,
    user_id INT NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Customers(customer_id) ON DELETE CASCADE,
    UNIQUE (user_id, user_role, username)
);
