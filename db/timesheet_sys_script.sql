CREATE TABLESPACE timesheet_data_davax DATAFILE 'timesheet_davax.dbf' SIZE 100M AUTOEXTEND ON NEXT 10M;
CREATE TABLESPACE timesheet_index_davax DATAFILE 'timesheet_index_davax.dbf' SIZE 50M AUTOEXTEND ON NEXT 5M;

CREATE USER timesheet_user_davax IDENTIFIED BY davax_pass DEFAULT TABLESPACE timesheet_data_davax TEMPORARY TABLESPACE temp;
GRANT CONNECT, RESOURCE TO timesheet_user_davax;
GRANT CREATE SESSION TO timesheet_user_davax;
GRANT CREATE VIEW, CREATE MATERIALIZED VIEW TO timesheet_user_davax;
GRANT CREATE PROCEDURE TO timesheet_user_davax;

ALTER USER timesheet_user_davax QUOTA UNLIMITED ON timesheet_data_davax;
ALTER USER timesheet_user_davax QUOTA UNLIMITED ON timesheet_index_davax;

-- PAS 2: Creare tabele (schema implicita: user)
CREATE TABLE ts_departments (
    department_id NUMBER PRIMARY KEY,
    name VARCHAR2(100) NOT NULL
) TABLESPACE timesheet_data_davax;


CREATE TABLE ts_employees (
    employee_id NUMBER PRIMARY KEY,
    name VARCHAR2(100) NOT NULL,
    hire_date DATE DEFAULT SYSDATE,
    salary NUMBER(10,2) CHECK (salary > 0),
    department_id NUMBER NOT NULL,
    CONSTRAINT fk_emp_dept FOREIGN KEY (department_id) REFERENCES ts_departments(department_id)
) TABLESPACE timesheet_data_davax;

CREATE INDEX idx_employee_name ON ts_employees(name);


CREATE TABLE ts_projects (
    project_id NUMBER PRIMARY KEY,
    name VARCHAR2(100) NOT NULL,
    status VARCHAR2(20) DEFAULT 'Active' CHECK (status IN ('Active', 'Completed', 'Suspended')),
    start_date DATE NOT NULL,
    end_date DATE
) TABLESPACE timesheet_data_davax;


CREATE INDEX idx_project_name ON ts_projects(name);

-- TABEL TIMESHEETS
CREATE TABLE ts_timesheets (
    timesheet_id NUMBER PRIMARY KEY,
    employee_id NUMBER NOT NULL,
    project_id NUMBER NOT NULL,
    work_date DATE NOT NULL,
    hours NUMBER(4,2) CHECK (hours BETWEEN 0 AND 24),
    work_details CLOB,
    CONSTRAINT fk_timesheet_emp FOREIGN KEY (employee_id) REFERENCES ts_employees(employee_id),
    CONSTRAINT fk_timesheet_proj FOREIGN KEY (project_id) REFERENCES ts_projects(project_id)
) TABLESPACE timesheet_data_davax;

GRANT SELECT ON ts_departments TO timesheet_user_davax;
GRANT SELECT ON ts_employees TO timesheet_user_davax;
GRANT SELECT ON ts_projects TO timesheet_user_davax;
GRANT SELECT ON ts_timesheets TO timesheet_user_davax;
