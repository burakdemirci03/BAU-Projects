from mysql import connector

my_connection = connector.connect(
    host="localhost",
    user="root",
    password="########",
    database="employees"
)
my_cursor = my_connection.cursor()

# 1)
my_cursor.execute("""
    SELECT emp.last_name, dep.department_name, loc.city
    FROM employees AS emp
    INNER JOIN departments AS dep ON emp.department_id = dep.department_id
    INNER JOIN locations AS loc ON dep.location_id = loc.location_id
    WHERE dep.department_name = 'IT';
""")

print("{:40} {:40} {:10}".format("Last Name", "Department", "City"),)

for row in my_cursor:
    print(f"{row[0]:40} {row[1]:40} {row[2]:<4}")

print("\n")

# 2)
my_cursor.execute(""" 
    SELECT loc.city, COUNT(emp.employee_id)
    FROM locations loc
    INNER JOIN departments AS dep ON loc.location_id = dep.location_id
    INNER JOIN employees AS emp ON dep.department_id = emp.department_id
    GROUP BY loc.city
    ORDER BY loc.city DESC;
""")

print("{:24} {:16}".format("City ", "Number of Employees"))

for row in my_cursor:
    print(f"{row[0]:24} {row[1]:<16}")

print("\n")

# 3)
my_cursor.execute(""" 
    SELECT job.job_title, COUNT(emp.employee_id)
    FROM jobs AS job
    INNER JOIN employees AS emp ON job.job_id = emp.job_id
    GROUP BY job.job_title
    ORDER BY job.job_title DESC;
""")

print("{:48} {:16} ".format("Job Title", "Number of Employees"))

for row in my_cursor:
    print(f"{row[0]:48} {row[1]:<16} ")

print("\n")

# 4)
my_cursor.execute(""" 
    SELECT CONCAT(emp.first_name, ' ', emp.last_name), loc.city, cou.country_name
    FROM employees AS emp
    INNER JOIN departments AS dep ON emp.department_id = dep.department_id
    INNER JOIN locations AS loc ON dep.location_id = loc.location_id
    INNER JOIN countries AS cou ON loc.country_id = cou.country_id
    WHERE cou.country_name = 'United Kingdom' or cou.country_name = 'Canada'
""")

print("{:32} {:24} {:100}".format("First Name + Last Name", "City", "Country"))
for row in my_cursor:
    print(f"{row[0]:32} {row[1]:24} {row[2]:<100}")

print("\n")

# 5)
my_cursor.execute(""" 
    SELECT loc.city, AVG(emp.salary)
    FROM locations AS loc
    INNER JOIN departments AS dep ON loc.location_id = dep.location_id
    INNER JOIN employees AS emp ON dep.department_id = emp.department_id
    GROUP BY loc.city
    ORDER BY loc.city ASC;
""")

print("{:32} {:4}".format("City", "Average Salary"))
for row in my_cursor:
    print(f"{row[0]:32} {row[1]:<4}")

