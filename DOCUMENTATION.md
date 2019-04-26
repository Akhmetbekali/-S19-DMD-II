# Documentation

## Table of Contents

- [Documentation](#documentation)
  * [KEYSPACE](#keyspace)
  * [TABLES](#tables)
    + [ESAS.Users](#esasusers)
      - [Columns](#columns)
      - [Primary Keys](#primary-keys)
    + [ESAS.Students](#esasstudents)
      - [Columns](#columns-1)
      - [Primary Keys](#primary-keys-1)
    + [ESAS.Grades](#esasgrades)
      - [Columns](#columns-2)
      - [Primary Keys](#primary-keys-2)
  * [PERMISSIONS](#permissions)




## KEYSPACE
A keyspace is the top-level database object that controls the replication for the object it contains. Keyspaces contain tables, materialized views and user-defined types, functions and aggregates.

The keyspace name in the project is ***ESAS***
## TABLES
Tables are also referred to as Column Families. Tables contain a set of columns and a primary key, and they store data in a set of rows.

There are 3 tables in the project

### ESAS.Users
#### Columns
| Field name  | Data type | Explanation |
| - | - | - |
| login  | text  | |
| hashedPass | text | |
| name | ascii | |
| surname | ascii | |
| userType | text | ['teacher', 'clerk', 'principal']
| email | text | |
| phone | text | |
| birthday | date | |
| address | ascii | |
| photo | ascii | a link to the photo
| permissionLvl | tinyint | [1,2,3,4,5] |
#### Primary Keys
| Field name  | Key type | Explanation |
| - | - | - |
| userType  | Partition Key | Store users of the same type in the same partioion to speed up Users search |
| surname | Clustering Key 1 |  |
| name | Clustering Key 2 | Sort users by surname and name inside a partition |

---

### ESAS.Students
#### Columns
| Field name  | Data type | Explanation |
| - | - | - |
|sId |uuid||
|sName |ascii||
|sSurname |ascii|| 
|sAddress |ascii||
|sEmail |text||
|sPhone |text||
|sBirthday |date||
|sPhoto |ascii||
|isFullFamily |boolean| True if has both parents, False otherwise|
|p1FullName |ascii||
|p1Phone |text||
|p2FullName |ascii||
|p2Phone |text||
|financialCase |text|['Intermediate class', 'Rich class', 'Poor class']|
|medicalConditions |text|['Healthy', 'Cancer stage 3']|
|studyYear |tinyint||
|studyGroup |text||
#### Primary Keys
| Field name  | Key type | Explanation |
| - | - | - |
| studyYear  | Partition Key 1 ||
| studyGroup  | Partition Key 2 | Store students of the same group and study year in the same partioion to speed up Students search |
| sSurname | Clustering Key 1 |  |
| sName | Clustering Key 2 | Sort students by surname and name inside a partition |

---

### ESAS.Grades
#### Columns
| Field name  | Data type | Explanation |
| - | - | - |
|sId |uuid||
|sName |ascii||
|sSurname |ascii||
|subject |ascii|['Math', 'Physics', 'Chemistry', 'Biology', ...]|
|midGrade |int||
|finalGrade |int||
|overallGrade |int||
|teacher |ascii||
|p1FullName |ascii||
|p1Phone |text||
|p2FullName |ascii||
|p2Phone |text||
|studyYear |tinyint||
|studyGroup |text||
#### Primary Keys
| Field name  | Key type | Explanation |
| - | - | - |
| studyYear  | Partition Key 1 ||
| studyGroup  | Partition Key 2 | Store students of the same group and study year in the same partioion to speed up Grades search |
| subject | Clustering Key 1 ||
| overallGrade | Clustering Key 2 ||
| sSurname | Clustering Key 3 ||
| sName | Clustering Key 4 | Sort users by subject, overallGrade, sSurname and sName inside a partition |

---

## PERMISSIONS
Cassandra has internal permissions implementation. A developer can define roles and grant permissions to them. If a user of a certain role tries to access a resourse that his role does not provide, he will get an error.

| Role | Permission | Explanation |
| - | - | - |
|admin |Superuser|Has access to the whole db|
|teacher |SELECT/MODIFY ON ESAS.Students|Can see and change Student table|
|teacher |SELECT/MODIFY ON ESAS.Grades|Can see and change Grades table|
|clerk |SELECT/MODIFY ON ESAS.Students|Can see and change Student table|
|clerk |SELECT/MODIFY ON ESAS.Users|Can see and change Users table|
|principal |SELECT ON ESAS.Grades|Can see Grades table|
|principal |SELECT ON ESAS.Students|Can see Students table|

## Geospatial table creation

In this project we define a way of creating table that defines the relative academic preformance by each pair of students which represents the distance between the pair (academically speaking). We'll talk briefly about the logic behind this float number.

#### Geospatial distance function

Spatial distance is calculated as square root of the sum of squares of differences of grades between two students, check the following formula that summerize the spatial distance. 

 <img src="https://github.com/Akhmetbekali/-S19-DMD-II/blob/master/spatial%20formula.PNG" />



## Geospatial search


