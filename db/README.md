# Timesheet Assignment – DavaX

This folder contains all necessary scripts for setting up and working with the **Timesheet database assignment**.

## 📁 Scripts Overview

### 🛠 `timesheet_sys_script.sql`
This script is intended to be run **by the SYS user** and includes:

- Creation of **tablespaces**
- Creation of the **TIMESHEET user**
- Granting necessary **permissions** to the TIMESHEET user
- Initial setup of the environment for the database

> Run this script as a privileged user (SYS/DBA).

---

### `timesheet_user_script.sql`
This script is run by the **TIMESHEET user** and includes:

- **Table creation**
- **Stored procedures**
- **Functions**
- **Triggers**
- **Views**
- Any **queries** used in the implementation

> Run this after the SYS script has been successfully executed and the TIMESHEET user is available.

---

###  `timesheet_full_script.sql`
A combined version that integrates the steps from both scripts above, allowing:

- Full setup from scratch
- Easier deployment in controlled environments

>  Use this for testing or automated setup where SYS access and user-level actions are executed in sequence.

---

##  Structure

The system models a simplified **Timesheet application**, including:

- Employees
- Projects
- Departments
- Timesheet entries
- Business logic encapsulated in PL/SQL


Happy coding!
