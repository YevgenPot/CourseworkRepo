
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

DROP SCHEMA IF EXISTS toyu;
CREATE SCHEMA toyu;
USE toyu;

DROP TABLE IF EXISTS Enroll;
DROP TABLE IF EXISTS Student;
DROP TABLE IF EXISTS Class;
DROP TABLE IF EXISTS Course;
DROP TABLE IF EXISTS Faculty;
DROP TABLE IF EXISTS Department;
DROP TABLE IF EXISTS school;
DROP TABLE IF EXISTS Grade;

--
--

CREATE TABLE IF NOT EXISTS Grade (
    grade CHAR(2) NOT NULL,
    gradePoint DECIMAL(5,4) NULL,
    CONSTRAINT Grade_grade_pk PRIMARY KEY (grade)
);

CREATE TABLE IF NOT EXISTS School (
    schoolCode CHAR(3) NOT NULL,
    schoolName VARCHAR(30) NOT NULL,
    CONSTRAINT School_schoolCode_pk PRIMARY KEY (schoolCode), 
	-- alternate keys: [1] schoolName
    CONSTRAINT School_name_ck UNIQUE (schoolName)
);

CREATE TABLE IF NOT EXISTS Department (
    deptCode    CHAR(4) NOT NULL,
    deptName    VARCHAR(30) NOT NULL,
    schoolCode  CHAR(3) NULL,
    numStaff  TINYINT NULL,
    CONSTRAINT Department_deptCode_pk PRIMARY KEY (deptCode),
	-- alternate keys: [1] deptName	
    CONSTRAINT Department_name_ck UNIQUE (deptName),
    CONSTRAINT Department_schoolCode_fk FOREIGN KEY (schoolCode) 
        REFERENCES School(schoolCode)
);

CREATE TABLE IF NOT EXISTS Faculty    (
    facId       INT NOT NULL,
    fname       VARCHAR(30) NOT NULL,
    lname       VARCHAR(30) NOT NULL,
    deptCode    CHAR(4) NOT NULL,
    `rank`      VARCHAR(25) NULL,
    CONSTRAINT Faculty_facId_pk PRIMARY KEY (facId),
    CONSTRAINT Faculty_deptCode_fk FOREIGN KEY (deptCode) 
        REFERENCES Department(deptCode));

CREATE TABLE IF NOT EXISTS Course (
    courseId    INT NOT NULL,
    rubric      CHAR(4) NOT NULL,
    number      CHAR(4) NOT NULL,
    title       VARCHAR(80) NOT NULL,
    credits     TINYINT NULL,
    CONSTRAINT Course_courseId_pk PRIMARY KEY (courseId),
    CONSTRAINT Course_deptCode_fk FOREIGN KEY (rubric) 
        REFERENCES Department(deptCode));
    
CREATE TABLE IF NOT EXISTS Class (
    classId     INT NOT NULL AUTO_INCREMENT,
    courseId    INT NOT NULL,
    semester    VARCHAR(10) NOT NULL,
    year        DECIMAL(4,0) NOT NULL,
    facId       INT NOT NULL,
    room        VARCHAR(6) NULL,
    CONSTRAINT Class_classId_pk PRIMARY KEY (classId),
    CONSTRAINT Class_courseId_fk FOREIGN KEY (courseId) 
        REFERENCES Course(courseId) ON DELETE CASCADE,
    CONSTRAINT Class_facId_fk FOREIGN KEY (facId) 
        REFERENCES Faculty (facId) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Student    (
    stuId        INT NOT NULL,
    fname        VARCHAR(30) NOT NULL,
    lname        VARCHAR(30) NOT NULL,
    major        CHAR(4) NULL,
    minor        CHAR(4) NULL,
	-- ach: accumulated credit hours, including transferred credits.
    ach      	 INTEGER(3) NULL DEFAULT 0,
    advisor      INT NULL,
    CONSTRAINT Student_stuId_pk PRIMARY KEY(stuId),
	-- an artificial example of a CHECK constraint.
    CONSTRAINT Student_ach_cc CHECK ((ach>=0) AND (ach < 250)),
    CONSTRAINT Student_major_fk FOREIGN KEY (major) 
        REFERENCES Department(deptCode) ON DELETE CASCADE,
    CONSTRAINT Student_minor_fk FOREIGN KEY (minor) 
        REFERENCES Department(deptCode) ON DELETE CASCADE,
    CONSTRAINT Student_advisor_fk FOREIGN KEY (advisor) 
        REFERENCES Faculty(facId)
); 
    
CREATE TABLE IF NOT EXISTS Enroll(
    stuId      INT NOT NULL,
    classId    INT NOT NULL,
    grade      VARCHAR(2) NULL,
    n_alerts   INT NULL,
    CONSTRAINT Enroll_classId_stuId_pk PRIMARY KEY (classId, stuId),
    CONSTRAINT Enroll_classNumber_fk FOREIGN KEY (classId) 
        REFERENCES Class(classId) ON DELETE CASCADE,    
    CONSTRAINT Enroll_stuId_fk FOREIGN KEY (stuId) 
        REFERENCES Student (stuId) ON DELETE CASCADE,
    CONSTRAINT Enroll_grade_fk FOREIGN KEY (grade) 
        REFERENCES Grade (grade) ON DELETE CASCADE
);

INSERT INTO Grade(grade, gradePoint) VALUES 
    ('A',4),('A-',3.6667),('B+',3.3333),('B',3),('B-',2.6667),
    ('C+',2.3333),('C',2),('C-',1.6667),
    ('D+',1.3333),('D',1),('D-',0.6667),('F',0),
	('P', NULL), ('IP', NULL), ('WX', NULL);
    
INSERT INTO School(schoolCode, schoolName) VALUES 
    ('BUS','Business'),
	('EDU','Education'),
    ('HSH','Human Sciences and Humanities'),
    ('CSE','Science and Engineering');

INSERT INTO Department(deptCode, deptName, schoolCode, numStaff) VALUES 
    ('ACCT','Accounting','BUS',10),
    ('ARTS','Arts','HSH',5),
    ('CINF','Computer Information Systems','CSE',5),
    ('CSCI','Computer Science','CSE',12),
    ('ENGL','English','HSH',12),
    ('ITEC','Information Technology','CSE',4),
    ('MATH','Mathematics','CSE',7);

INSERT INTO Faculty(facId, fname, lname, deptCode, `rank`) VALUES
    (1011,'Paul','Smith','CSCI','Professor'),
    (1012,'Mary','Tran','CSCI','Associate Professor'),
    (1013,'David','Love','CSCI',NULL),
    (1014,'Sharon','Mannes','CSCI','Assistant Professor'),
    (1015,'Daniel','Kim','CINF','Professor'),
    (1016,'Andrew','Byre','CINF','Associate Professor'),
    (1017,'Deborah','Gump','ITEC','Professor'),
    (1018,'Art','Allister','ARTS','Assistant Professor'),
    (1019,'Benjamin','Yu','ITEC','Lecturer'),
    (1020,'Katrina','Bajaj','ENGL','Lecturer'),
    (1021,'Jorginlo','Neymar','ACCT','Assistant Professor');

INSERT INTO Course(courseId, rubric, number, title, credits) VALUES
    (2000,'CSCI',3333,'Data Structures',3),
    (2001,'CSCI',4333,'Design of Database Systems',3),
    (2002,'CSCI',5333,'DBMS',3),
    (2020,'CINF',3321,'Introduction to Information Systems',3),
    (2021,'CINF',4320,'Web Application Development',3),
    (2040,'ITEC',3335,'Database Development',3),
    (2041,'ITEC',3312,'Introduction to Scripting',3),
    (2060,'ENGL',1410,'English I',4),
    (2061,'ENGL',1311,'English II',3),
    (2080,'ARTS',3311,'Hindu Arts',3),
    (2090,'ACCT',3333,'Managerial Accounting',3);

INSERT INTO Class(classId, courseId, semester, year, facId, room) VALUES
    (10000,2000,'Fall',2019,1011,'D241'),
    (10001,2001,'Fall',2019,1011,'D242'),
    (10002,2002,'Fall',2019,1012,'D136'),
    (10003,2020,'Fall',2019,1014,'D241'),
    (10004,2021,'Fall',2019,1014,'D241'),
    (10005,2040,'Fall',2019,1015,'D237'),
    (10006,2041,'Fall',2019,1019,'D217'),
    (10007,2060,'Fall',2019,1020,'B101'),
    (10008,2080,'Fall',2019,1018,'D241'),
    (11000,2000,'Spring',2020,1011,'D241'),
    (11001,2001,'Spring',2020,1012,'D242'),
    (11002,2002,'Spring',2020,1013,'D136'),
    (11003,2020,'Spring',2020,1016,'D217'),
    (11004,2061,'Spring',2020,1018,'B101');

INSERT INTO Student(stuId, fname, lname, major, minor, ach, advisor) VALUES
    (100000,'Tony','Hawk','CSCI','CINF',40,1011),
    (100001,'Mary','Hawk','CSCI','CINF',35,1011),
    (100002,'David','Hawk','CSCI','ITEC',66,1012),
    (100003,'Catherine','Lim','ITEC','CINF',20,NULL),
    (100004,'Larry','Johnson','ITEC',NULL,66,1017),
    (100005,'Linda','Johnson','CINF','ENGL',13,1015),
    (100006,'Lillian','Johnson','CINF','ITEC',18,1016),
    (100007,'Ben','Zico',NULL,NULL,16,NULL),
    (100008,'Bill','Ching','ARTS',NULL,90,NULL),
    (100009,'Linda','King','ARTS','CSCI',125,1018),
	(100111,'Cathy','Johanson',NULL,NULL,0,1018);
    
INSERT INTO Enroll(stuId, classId, grade, n_alerts) VALUES
    (100000,10000,'A',0),
    (100001,10000,NULL,NULL),
    (100002,10000,'B-',3),
    (100000,10001,'A',2),
    (100001,10001,'A-',0),
    (100000,10002,'B+',1),
    (100002,10002,'B+',2),
    (100000,10003,'C',0),
    (100002,10003,'D',4),
    (100004,10003,'A',0),
    (100005,10003,NULL,NULL),
    (100000,10004,'A-',1),
    (100004,10004,'B+',NULL),
    (100005,10004,'A-',0),
    (100006,10004,'C+',NULL),
    (100005,10005,'A-',0),
    (100006,10005,'A',NULL),
    (100005,10006,'B+',NULL),
    (100007,10007,'F',4),
    (100008,10007,'C-',0),
    (100007,10008,'A-',0),
    (100000,11001,'D',4);
    
SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
  