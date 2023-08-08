/*SQL SECTION*/

/* Each time a rocket is launched, one or more cores (first stages) are involved. Sometimes, cores are recovered after the launch 
and they are reused posteriorly in another launch. Which is the maximum number of times a core has been used? Write a SQL query to
find the result*/
SELECT core, COUNT(*) as count_times
FROM cores as c
JOIN launches l on c.launch_id = l.id
WHERE c.core is not NULL and l.upcoming = false
GROUP BY c.core
ORDER BY count_times DESC;



/*Which cores have been reused in less than 50 days after the previous launch? Write a SQL query to find the result.*/
SELECT c.core, l.date_utc AS current_launch_date, l_prev.date_utc AS previous_launch_date
FROM cores c
JOIN launches l ON c.launch_id = l.id
JOIN cores c_prev ON c.core = c_prev.core AND c.launch_id <> c_prev.launch_id
JOIN launches l_prev ON c_prev.launch_id = l_prev.id
AND l.date_utc - l_prev.date_utc < INTERVAL '50 days'
AND l.date_utc > l_prev.date_utc
WHERE l.upcoming = false and l_prev.upcoming = false;


/*List the months in which there has been more than one launch. Write a SQL query to find the results.*/
SELECT EXTRACT(MONTH FROM date_utc) as month, COUNT(EXTRACT(MONTH FROM date_utc)) AS count_launches
FROM launches
WHERE upcoming = false
GROUP BY EXTRACT(MONTH FROM date_utc)
HAVING  COUNT(EXTRACT(MONTH FROM date_utc)) > 1
ORDER BY COUNT(EXTRACT(MONTH FROM date_utc)) desc;
