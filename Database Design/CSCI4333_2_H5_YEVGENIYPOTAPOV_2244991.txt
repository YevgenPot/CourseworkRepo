WITH commitTask AS
(SELECT CT_Id
FROM commitment
	inner join v_task on (commitment.VT_Id = v_task.VT_Id)
WHERE v_task.Name = 'Officiating')
SELECT DISTINCT c.CT_Id, c.LName, c.FName
FROM caretaker as c
WHERE c.CT_Id NOT IN(select * from commitTask)
;

SELECT DISTINCT c.CT_Id, c.LName, c.FName
FROM caretaker as c
	inner join commitment on (commitment.CT_Id = c.CT_Id)
	inner join v_task as vt on (commitment.VT_Id = vt.VT_Id)
WHERE vt.Name IS NOT NULL
;

SELECT c.CT_Id, CONCAT(c.FName, ' ', c.LName) as caretaker,
GROUP_CONCAT(commitment.VT_Id separator '; ') as 'task ids'
FROM caretaker as c
	inner join commitment on (commitment.CT_Id=c.CT_Id)
GROUP BY commitment.CT_Id
HAVING (COUNT(commitment.VT_Id) >= 2)
;

SELECT c.CT_Id, CONCAT(c.FName, ' ', c.LName) as caretaker,
GROUP_CONCAT(commitment.VT_Id separator '; ') as 'task ids'
FROM caretaker as c
	inner join commitment on (commitment.CT_Id=c.CT_Id)
WHERE c.CT_Id IN(SELECT CT_Id FROM othercaretaker)
AND c.CT_Id IN(SELECT Main_CT_Id FROM swimmer)
GROUP BY commitment.CT_Id
HAVING (COUNT(commitment.VT_Id) >= 2)
;

SELECT c.LName, c.FName, vt.Name as 'Task Name', m.Title as 'Meet Title'
FROM caretaker as c
	left join commitment on (c.CT_Id = commitment.CT_Id)
	left join v_task as vt on (vt.VT_Id = commitment.VT_Id)
	left join v_tasklist on (vt.VTL_Id = v_tasklist.VTL_Id)
	left join meet as m on (v_tasklist.MeetId = m.MeetId)
ORDER BY c.CT_Id asc
;

WITH CommitMeet AS
(SELECT c.CT_Id, vt.Name as 'Task Name', m.MeetId, m.Title
FROM caretaker as c
	left join commitment on (c.CT_Id = commitment.CT_Id)
	left join v_task as vt on (vt.VT_Id = commitment.VT_Id)
	left join v_tasklist on (vt.VTL_Id = v_tasklist.VTL_Id)
	left join meet as m on (v_tasklist.MeetId = m.MeetId)
WHERE (m.Title = 'UHCL Open') OR (m.MeetId IS NULL)
)
SELECT c.CT_Id, CONCAT(c.FName, ' ', c.LName) as caretaker, COUNT(CommitMeet.MeetId) as 'Number of committed tasks in UHCL Open'
FROM caretaker as c
	inner join CommitMeet on (CommitMeet.CT_Id = c.CT_Id)
GROUP BY CT_Id
ORDER BY COUNT(CommitMeet.MeetId) desc, c.CT_Id asc
;

WITH participationCount AS(
SELECT SwimmerId, COUNT(ParticipationId) as COUNTpart
FROM participation
GROUP BY SwimmerId
), 
levelhistoryCount AS(
SELECT SwimmerId, COUNT(LevelId) as COUNTlevel
FROM levelhistory
GROUP BY SwimmerId
),
othercaretakerCOUNT AS(
SELECT s.SwimmerId, COUNT(o.CT_Id) as COUNTct
FROM swimmer as s
	left join othercaretaker as o on (s.SwimmerId = o.SwimmerId)
GROUP BY SwimmerId
)
SELECT s.SwimmerId, CONCAT(s.FName, ' ', s.LName) as 'swimmer',
	levelhistoryCount.COUNTlevel as '# historical levels', 
    participationCount.COUNTpart as '# events participated', 
    othercaretakerCOUNT.COUNTct as '# secondary caretakers'
FROM swimmer as s
	left join participationCount on (s.SwimmerId = participationCount.SwimmerId)
    left join levelhistoryCount on (s.SwimmerId = levelhistoryCount.SwimmerId)
    left join othercaretakerCOUNT on (s.SwimmerId = othercaretakerCOUNT.SwimmerId)
;







