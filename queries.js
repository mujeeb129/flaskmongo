
// Aggrigation queries
db.persons.aggregate([
    { $match: { "dob.age": { $gte: 50 } } },
    { $group: { _id: "$gender", totalGender: { $sum: 1 }, averageAge: { $avg: "$dob.age" } } },
    { $sort: { totalGender: -1 } }
])

db.persons.aggregate([
    {
        $project: {
            _id: 0, fullName:
            {
                $concat: [
                    { $toUpper: { $substrCP: ["$name.first", 0, 1] } },
                    { $substrCP: ["$name.first", 1, { $subtract: [{ $strLenCP: "$name.first" }, 1] }] },
                    " ",
                    { $toUpper: { $substrCP: ["$name.last", 0, 1] } },
                    { $substrCP: ["$name.last", 1, { $subtract: [{ $strLenCP: "$name.last" }, 1] }] }
                ]
            }
        }
    }
])