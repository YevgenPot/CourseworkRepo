//1
db.enroll.find(
{grade: {$in: ["A","A-","B+","B","B-"]} },{_id:0,n_alerts:0}).sort(
 {classId: 1} )

//2
db.enroll.aggregate(
   [  
      { $group: { "_id": "$classId", "count": {$sum:1}} },
      { $project: { "classId": "$_id" , "number of students": "$count",  "_id": 0}}
   ]
)

//3
db.faculty.aggregate([
{$match:{$or: [
{lname: {$regex: "an", $options: "i"}},
{fname: {$regex: "an", $options: "i"}}
]}
}, {$project:{_id:0, deptCode: 1, 
faculty:{$concat:["$fname"," ","$lname"]} }
}
])

//4
result1 = db.faculty.find(
{ $or: [
{lname: {$regex: "an", $options: "i"}},
{fname: {$regex: "an", $options: "i"}}
] }
).toArray()
console.log('Faculty with the substring "an" in their names.')
result.forEach((x,i) => console.log( 
"[" + String(i+1) + "]" + ' ' + x["fname"] + ' ' + x["lname"] + ":"
 + " " + x["deptCode"]))

//5
result1 = db.faculty.aggregate([
{$lookup: {from: "department",
let: {joinValue: '$deptCode'},
      pipeline: [
           { $match:
                 { $expr:
                    { $and:
                       [
                         { $eq: [ "$deptCode",  "$$joinValue" ] },
                       ]
                    }
                 }
            }    
        ],
        as: "depart"}} , {
      $replaceRoot: { newRoot: { $mergeObjects: [ { $arrayElemAt: [ "$depart", 0 ] }, "$$ROOT" ] } }},
{$match:{ $or: [
{lname: {$regex: "an", $options: "i"}},
{fname: {$regex: "an", $options: "i"}}
] }
}
]).toArray()
console.log('Faculty with the substring "an" in their names.')
result1.forEach((x,i) => console.log( 
"[" + String(i+1) + "]" + ' ' + x["fname"] + ' ' + x["lname"] + ":"
 + " " + x["deptName"] + " " + "(" + x["deptCode"] + ")" ))