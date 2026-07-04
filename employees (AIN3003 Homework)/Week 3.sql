SELECT * FROM   departments;
SELECT * FROM   employees;
SELECT department_id, location_id FROM   departments;
SELECT last_name, salary, salary + 300 FROM   employees;
SELECT last_name, salary, 12*salary+100
FROM   employees;
SELECT last_name, job_id, salary, commission_pct
FROM   employees;
SELECT last_name AS name, commission_pct comm
FROM   employees;
SET sql_mode=(SELECT CONCAT(@@sql_mode,',PIPES_AS_CONCAT')); 
SELECT	last_name|| first_name AS "Employees" FROM 	employees;
SELECT last_name ||' is a '||job_id AS "Employee Details" FROM   employees;
SELECT department_id FROM   employees;
SELECT DISTINCT department_id FROM   employees;
DESCRIBE employees;


SELECT employee_id, last_name, job_id, department_id
FROM   employees
WHERE  department_id = 90 ;

SELECT last_name, job_id, department_id
FROM   employees
WHERE  last_name = 'Whalen' ;


SELECT last_name, salary
FROM   employees
WHERE  salary <= 3000 ;

SELECT employee_id, last_name, salary, manager_id
FROM   employees
WHERE  manager_id IN (100, 101, 201) ;

SELECT last_name, salary
FROM   employees
WHERE  salary <= 3000 ;

SELECT last_name, salary
FROM   employees
WHERE  salary BETWEEN 2500 AND 3500 ;

SELECT employee_id, last_name, salary, manager_id
FROM   employees
WHERE  manager_id IN (100, 101, 201) ;


SELECT	first_name
FROM 	employees
WHERE	first_name LIKE 'S%' ;



SELECT last_name
FROM   employees
WHERE  last_name LIKE '_o%' ;


SELECT last_name, manager_id
FROM   employees
WHERE  manager_id IS NULL ;


SELECT employee_id, last_name, job_id, salary
FROM   employees
WHERE  salary >= 10000
AND    job_id LIKE '%MAN%' ;

SELECT employee_id, last_name, job_id, salary
FROM   employees
WHERE  salary >= 10000
OR     job_id LIKE '%MAN%' ;

SELECT last_name, job_id
FROM   employees
WHERE  job_id 
       NOT IN ('IT_PROG', 'ST_CLERK', 'SA_REP') ;

SELECT last_name, job_id, salary
FROM   employees
WHERE  job_id = 'SA_REP'
OR     job_id = 'AD_PRES'
AND    salary > 15000;



SELECT   last_name, job_id, department_id, hire_date
FROM     employees
ORDER BY hire_date ;

SELECT   last_name, job_id, department_id, hire_date
FROM     employees
ORDER BY hire_date DESC ;

SELECT employee_id, last_name, salary*12 annsal
FROM   employees
ORDER BY annsal ;


SELECT   last_name, job_id, department_id, hire_date
FROM     employees
ORDER BY 3;

SELECT last_name, department_id, salary
FROM   employees
ORDER BY department_id, salary DESC;

SELECT employee_id, CONCAT(first_name, last_name) NAME, 
       job_id, LENGTH (last_name), 
       INSTR(last_name, 'a') "Contains 'a'?"
FROM   employees
WHERE  SUBSTR(job_id, 4) = 'REP';

SELECT ROUND(45.923,2), ROUND(45.923,0),
       ROUND(45.923,-1);

SELECT last_name, salary, MOD(salary, 5000)
FROM   employees
WHERE  job_id = 'SA_REP';

SELECT AVG(salary), MAX(salary),
       MIN(salary), SUM(salary)
FROM   employees
WHERE  job_id LIKE '%REP%';


SELECT MIN(hire_date), MAX(hire_date)
FROM	  employees;

SELECT COUNT(*)
FROM   employees
WHERE  department_id = 50;

SELECT COUNT(DISTINCT department_id)
FROM   employees;

SELECT   department_id, job_id, SUM(salary)
FROM     employees
WHERE	 department_id > 40
GROUP BY department_id, job_id 
ORDER BY department_id;


SELECT department_id, job_id, COUNT(last_name)
FROM   employees
GROUP BY department_id;



SELECT   department_id, AVG(salary)
FROM     employees
WHERE    AVG(salary) > 8000
GROUP BY department_id;
--  Should give an error 




SELECT   job_id, SUM(salary) PAYROLL
FROM     employees
WHERE    job_id NOT LIKE '%REP%'
GROUP BY job_id
HAVING   SUM(salary) > 13000
ORDER BY SUM(salary);


SELECT department_id, department_name,
       location_id, city
FROM   departments
NATURAL JOIN locations ;


SELECT l.city, d.department_name 
FROM   locations l JOIN departments d
USING (location_id)
WHERE d.location_id = 1400;

SELECT e.last_name, e.department_id, d.department_name
FROM   employees e LEFT OUTER JOIN departments d
ON   (e.department_id = d.department_id) ;

SELECT e.last_name, e.department_id, d.department_name
FROM   employees e RIGHT  OUTER JOIN departments d
ON   (e.department_id = d.department_id) ;

SELECT last_name, department_name
FROM   employees
CROSS JOIN departments 
ON department_name;



SELECT last_name, salary
FROM   employees
WHERE  salary >
               (SELECT salary
                FROM   employees
                WHERE  last_name = 'Abel');


SELECT last_name, job_id, salary
FROM   employees
WHERE  job_id =  
                (SELECT job_id
                 FROM   employees
                 WHERE  last_name = 'Taylor')
AND    salary >
                (SELECT salary
                 FROM   employees
                 WHERE  last_name = 'Taylor');


SELECT   department_id, MIN(salary)
FROM     employees
GROUP BY department_id
HAVING   min(salary) >
                       (SELECT min(salary)
                        FROM   employees
                        WHERE  department_id = 50);

SELECT min(salary)
                        FROM   employees
                        WHERE  department_id = 50;

SELECT * FROM departments
WHERE NOT EXISTS
(SELECT * FROM employees
 WHERE employees.department_id=departments.department_id);


SELECT employee_id, job_id, department_id
FROM   employees
UNION ALL
SELECT employee_id, job_id, department_id
FROM   job_history
ORDER BY  employee_id;


UPDATE  copy_emp
SET     department_id  =  (SELECT department_id
                           FROM employees
                           WHERE employee_id = 100)
WHERE   job_id         =  (SELECT job_id
                           FROM employees
                           WHERE employee_id = 200);

