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


CREATE OR REPLACE TRIGGER trg_check_work_date
BEFORE INSERT OR UPDATE ON ts_timesheets
FOR EACH ROW
DECLARE
    v_hire_date DATE;
BEGIN
    -- Check 1: work_date cannot be in the future
    IF :NEW.work_date > SYSDATE THEN
        RAISE_APPLICATION_ERROR(-20001, 'Data raportarii nu poate fi in viitor.');
    END IF;

    -- OPTIONAL: Check 2: work_date cannot be before employee was hired
    SELECT hire_date INTO v_hire_date
    FROM ts_employees
    WHERE employee_id = :NEW.employee_id;

    IF :NEW.work_date < v_hire_date THEN
        RAISE_APPLICATION_ERROR(-20002, 'Data raportarii nu poate fi inainte de angajare.');
    END IF;
END;

INSERT INTO ts_departments (department_id, name) VALUES (1, 'IT');
INSERT INTO ts_departments (department_id, name) VALUES (2, 'HR');
INSERT INTO ts_departments (department_id, name) VALUES (3, 'Finance');
INSERT INTO ts_departments (department_id, name) VALUES (4, 'Marketing');
INSERT INTO ts_departments (department_id, name) VALUES (5, 'Support');



INSERT INTO ts_employees (employee_id, name, hire_date, salary, department_id)
VALUES (101, 'Alice Popescu', DATE '2022-06-15', 5200.00, 1);

INSERT INTO ts_employees (employee_id, name, hire_date, salary, department_id)
VALUES (102, 'Bogdan Ionescu', DATE '2023-01-10', 4800.50, 2);

INSERT INTO ts_employees (employee_id, name, hire_date, salary, department_id)
VALUES (103, 'Cristina Marinescu', DATE '2022-03-20', 6100.00, 3);

INSERT INTO ts_employees (employee_id, name, hire_date, salary, department_id)
VALUES (104, 'Daniel Vasilescu', DATE '2021-11-01', 5700.00, 4);

INSERT INTO ts_employees (employee_id, name, hire_date, salary, department_id)
VALUES (105, 'Elena Georgescu', DATE '2023-08-10', 4950.00, 5);


INSERT INTO ts_projects (project_id, name, status, start_date, end_date)
VALUES (201, 'Optimizare ERP', 'Active', DATE '2023-03-01', DATE '2024-12-31');

INSERT INTO ts_projects (project_id, name, status, start_date, end_date)
VALUES (202, 'Implementare CRM', 'Active', DATE '2024-01-01', NULL);

INSERT INTO ts_projects (project_id, name, status, start_date, end_date)
VALUES (203, 'Migrare Intranet', 'Completed', DATE '2022-02-01', DATE '2023-07-31');

INSERT INTO ts_projects (project_id, name, status, start_date, end_date)
VALUES (204, 'Audit Financiar', 'Suspended', DATE '2023-06-01', NULL);

INSERT INTO ts_projects (project_id, name, status, start_date, end_date)
VALUES (205, 'Automatizare HR', 'Active', DATE '2024-02-15', NULL);


INSERT INTO ts_timesheets (timesheet_id, employee_id, project_id, work_date, hours, work_details)
VALUES (1006, 103, 201, DATE '2023-10-15', 6.75, 'Scriere proceduri ERP');

INSERT INTO ts_timesheets (timesheet_id, employee_id, project_id, work_date, hours, work_details)
VALUES (1007, 103, 203, DATE '2022-06-22', 5.50, 'Testare functionalitati intranet');

INSERT INTO ts_timesheets (timesheet_id, employee_id, project_id, work_date, hours, work_details)
VALUES (1008, 104, 204, DATE '2023-09-11', 7.00, 'Prezentare pentru audit');

INSERT INTO ts_timesheets (timesheet_id, employee_id, project_id, work_date, hours, work_details)
VALUES (1009, 104, 202, DATE '2024-04-02', 4.25, 'Coordonare cu clientul');

INSERT INTO ts_timesheets (timesheet_id, employee_id, project_id, work_date, hours, work_details)
VALUES (1010, 105, 205, DATE '2024-06-01', 3.75, 'Training echipa HR');

INSERT INTO ts_timesheets (timesheet_id, employee_id, project_id, work_date, hours, work_details)
VALUES (1011, 105, 205, DATE '2024-06-05', 4.00, 'Documentatie fluxuri automate');

INSERT INTO ts_timesheets (timesheet_id, employee_id, project_id, work_date, hours, work_details)
VALUES (1012, 101, 201, DATE '2023-03-14', 6.5, 'Analiza cerințe ERP modul contabil');

INSERT INTO ts_timesheets (timesheet_id, employee_id, project_id, work_date, hours, work_details)
VALUES (1013, 101, 202, DATE '2024-02-20', 7.0, 'Întâlnire cu clientul pentru CRM');

INSERT INTO ts_timesheets (timesheet_id, employee_id, project_id, work_date, hours, work_details)
VALUES (1014, 101, 201, DATE '2024-12-01', 5.5, 'Testare finală modul ERP');

INSERT INTO ts_timesheets (timesheet_id, employee_id, project_id, work_date, hours, work_details)
VALUES (1015, 101, 202, SYSDATE - 3, 3.75, 'Feedback documentație CRM');

INSERT INTO ts_timesheets (timesheet_id, employee_id, project_id, work_date, hours, work_details)
VALUES (1016, 102, 202, DATE '2024-03-10', 4.5, 'Configurare inițială modul CRM');

INSERT INTO ts_timesheets (timesheet_id, employee_id, project_id, work_date, hours, work_details)
VALUES (1017, 102, 201, DATE '2023-09-05', 6.0, 'Refactorizare cod sursă ERP');

INSERT INTO ts_timesheets (timesheet_id, employee_id, project_id, work_date, hours, work_details)
VALUES (1018, 102, 202, DATE '2024-06-04', 2.0, 'Monitorizare livrare incrementală');

INSERT INTO ts_timesheets (timesheet_id, employee_id, project_id, work_date, hours, work_details)
VALUES (1019, 102, 202, SYSDATE - 2, 3.25, 'Corecturi după QA');

-- View: total ore pe angajat
CREATE OR REPLACE VIEW ts_view_employee_hours AS
SELECT 
    e.employee_id,
    e.name AS employee_name,
    SUM(t.hours) AS total_hours
FROM ts_employees e
JOIN ts_timesheets t ON e.employee_id = t.employee_id
GROUP BY e.employee_id, e.name;


-- Materialized view: total ore per proiect
CREATE MATERIALIZED VIEW ts_view_materialized_project_hours
BUILD IMMEDIATE
REFRESH ON DEMAND
AS
SELECT 
    t.project_id,
    COUNT(*) AS entry_count,
    SUM(t.hours) AS total_hours
FROM ts_timesheets t
GROUP BY t.project_id;

-- Acest SELECT returnează totalul orelor lucrate de fiecare angajat, grupat pe lună
SELECT 
    employee_id,
    TO_CHAR(work_date, 'YYYY-MM') AS work_month,
    SUM(hours) AS total_monthly_hours
FROM ts_timesheets
GROUP BY employee_id, TO_CHAR(work_date, 'YYYY-MM');

-- Afișează toți angajații cu nume și salariu ordonat descrescător după salariu
SELECT 
    employee_id,
    name,
    salary
FROM ts_employees
ORDER BY salary DESC;

-- Afișează proiectele active, sortate după data de început
SELECT 
    project_id,
    name,
    start_date,
    end_date
FROM ts_projects
WHERE status = 'Active'
ORDER BY start_date;

-- Afișează toate orele lucrate într-o anumită zi (ex. 2024-06-01)
SELECT 
    employee_id,
    project_id,
    work_date,
    hours,
    work_details
FROM ts_timesheets
WHERE work_date = DATE '2024-06-01';

-- Afișează orele lucrate de 'Alice Popescu' pe fiecare proiect
SELECT 
    p.name AS project_name,
    t.work_date,
    t.hours
FROM ts_timesheets t
JOIN ts_employees e ON t.employee_id = e.employee_id
JOIN ts_projects p ON t.project_id = p.project_id
WHERE e.name = 'Alice Popescu';


-- Afișează toți angajații și (dacă există) detalii despre orele lor lucrate
SELECT 
    e.name AS employee_name,
    t.work_date,
    t.hours
FROM ts_employees e
LEFT JOIN ts_timesheets t ON e.employee_id = t.employee_id;

-- Afișează orele lucrate de fiecare angajat și orele lucrate anterior (LAG)
SELECT 
    employee_id,
    work_date,
    hours,
    LAG(hours, 1, 0) OVER (PARTITION BY employee_id ORDER BY work_date) AS prev_hours
FROM ts_timesheets;

CREATE OR REPLACE PROCEDURE show_timesheets(p_emp_id IN NUMBER)
AS
BEGIN
    FOR r IN (
        SELECT work_date, hours, work_details
        FROM ts_timesheets
        WHERE employee_id = p_emp_id
    ) LOOP
        DBMS_OUTPUT.PUT_LINE('Date: ' || r.work_date || ' - Hours: ' || r.hours || ' - Details: ' || r.work_details);
    END LOOP;
END;

ALTER TABLE ts_timesheets ADD json_details CLOB;

UPDATE ts_timesheets
SET json_details = '{
    "task_type": "development",
    "tools_used": ["Jira", "Git", "Oracle SQL Developer"],
    "remote": true
}'
WHERE timesheet_id = 1006;

-- Exemplu 1: task de analiză
UPDATE ts_timesheets SET json_details = '{
    "task_type": "analysis",
    "tools_used": ["Excel", "Confluence"],
    "remote": false
}' WHERE timesheet_id = 1007;

-- Exemplu 2: întâlnire cu clientul
UPDATE ts_timesheets SET json_details = '{
    "task_type": "meeting",
    "tools_used": ["Zoom", "Slack"],
    "remote": true
}' WHERE timesheet_id = 1010;

-- Exemplu 3: debugging
UPDATE ts_timesheets SET json_details = '{
    "task_type": "debugging",
    "tools_used": ["Postman", "Oracle SQL Developer"],
    "remote": false
}' WHERE timesheet_id = 1012;


-- Selectează tipul de task (din json_details) și numele angajatului
SELECT 
    e.name AS employee_name,
    JSON_VALUE(t.json_details, '$.task_type') AS task_type
FROM ts_timesheets t
JOIN ts_employees e ON t.employee_id = e.employee_id
WHERE t.json_details IS NOT NULL;

-- Afișează totalul orelor raportate de fiecare angajat (din view-ul creat)
SELECT * FROM ts_view_employee_hours;

-- Afișează totalul orelor și numărul de înregistrări per proiect (din materialized view)
SELECT * FROM ts_view_materialized_project_hours;

-- View cu informații din JSON plus date despre angajați și proiecte
CREATE OR REPLACE VIEW ts_view_json_summary AS
SELECT 
    t.timesheet_id,
    e.name AS employee_name,
    p.name AS project_name,
    JSON_VALUE(t.json_details, '$.task_type') AS task_type,
    JSON_VALUE(t.json_details, '$.remote') AS remote_flag
FROM ts_timesheets t
JOIN ts_employees e ON e.employee_id = t.employee_id
JOIN ts_projects p ON p.project_id = t.project_id
WHERE t.json_details IS NOT NULL;
