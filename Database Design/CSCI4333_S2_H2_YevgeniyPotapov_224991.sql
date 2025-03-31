select course.rubric,
	course.number, course.title, class.classId,
	class.facId, class.year, class.semester
from class inner join course on class.courseId = course.courseId
where (rubric = "CSCI") OR (rubric = "CINF")
order by rubric desc
;

select concat(course.rubric, " " , course.number) as course, course.title, 
	class.classId, class.facId,
    faculty.deptCode as "instructor dept"
from course
	inner join class on course.courseId = class.courseId
	inner join faculty on class.facId = faculty.facId
where deptCode = "CSCI"
;

select stuId, fname, lname, major, minor, ach as "Accumulated credits",
case
	when ach > 90 then "senior"
    when ach <= 90 and ach >= 61 then "junior"
    when ach <= 60 and ach >= 0 then "lower"
	end as "status"
from student
where major = "CSCI" OR minor = "CSCI"
;

select s.stuId, s.fname, s.lname, e.classId, e.grade
from student as s
	inner join enroll as e on s.stuId = e.stuId
where (e.grade is null) and (e.n_alerts is null)
;

select s.stuId, s.fname, s.lname, e.classId, e.grade
from student as s
	join enroll as e on s.stuId = e.stuId
    left join grade as g on e.grade = g.grade
where
	e.grade is null or g.gradePoint < 1.5
order by s.stuId asc
;

select s.stuId, s.major, s.minor, e.classId, c.title as course,
	d.deptName as "Offered by", e.grade
from student as s
left join enroll as e on e.stuId = s.stuId
inner join class as cl on cl.classId = e.classId
inner join course as c on c.courseId = cl.courseId
inner join department as d on c.rubric = d.deptCode
where (s.major is not null) and (s.minor is not null)
order by s.stuId asc, e.classId asc
;