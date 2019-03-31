from faker import Faker
from cassandra.cluster import Cluster
import random
from random import randint
import uuid
import math
import time

def strTimeProp(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def randomDate(start, end, prop):
    return strTimeProp(start, end, '%m/%d/%Y %I:%M %p', prop)


def random_phone_number():
    n = 10
    range_start = 10**(n-1)
    range_end = (10**n)-1
    countries = ['+963', '+7', '+1']
    zbr = randint(range_start, range_end)
    return random.choice(countries) + str(zbr)


def weighted_choice(weights, choices):
    totals = []
    running_total = 0

    for w in weights:
        running_total += w
        totals.append(running_total)

    rnd = random.random() * running_total
    for i, total in enumerate(totals):
        if rnd < total:
            return choices[i]


t1 = time.time()
cluster = Cluster()
session = cluster.connect()

KEYSPACE = 'ESAS'
TABLE_USERS = KEYSPACE + '.Users'
TABLE_STUDENTS = KEYSPACE + '.Students'
TABLE_GRADES = KEYSPACE + '.Grades'

session.execute('TRUNCATE TABLE ESAS.Users;')  # HERE I AM DELETING EVERYTHING
session.execute('TRUNCATE TABLE ESAS.Grades;')
session.execute('TRUNCATE TABLE ESAS.Students;')

fake = Faker()
MAX = 3  # Here you can set the max
typesOfUsers = ['null','school principal', 'clerk', 'class teacher']

for i in range(1, MAX+1):

    zbr = fake.profile()
    while not zbr['name'].find(' '):
        zbr = fake.profile()
    hPass = fake.password().__hash__()
    username = zbr['username']

    nomes = zbr['name'].split(' ')
    fname, sname = 0,0
    if len(nomes) == 3:
        fname = nomes[0]
        sname = nomes[1] + nomes[2]
    else:
        fname = nomes[0]
        sname = nomes[1]

    email = fake.email()
    userType = weighted_choice([97, 1, 1, 1],typesOfUsers)
    phone = random_phone_number()
    birthday = fake.date_of_birth(tzinfo=None, minimum_age=7, maximum_age=18)
    address = zbr['address']
    photo = fake.url() + username+'.PNG'
    pLVL = 1
    sId = uuid.uuid4()

    parent1 = fake.profile()
    p1FullName = parent1['name']
    p1Phone = random_phone_number()

    parent2 = fake.profile()
    p2FullName = parent2['name']
    p2Phone = random_phone_number()
    isFullFamily = weighted_choice([80,20],['true', 'false'])
    studyGroup = random.choice([1,2,3,4,5])
    financialCase = random.choice(['Intermediate class', 'Rich class', 'Poor class'])
    medicalConditions = weighted_choice([80,20], ['Healthy', 'Cancer stage 3'])
    studyYear = random.choice([1,2,3])

    subject = random.choice(['Math','Physics','Chemistry','Biology','Sexual Education','Informatics','Arabic','English','French'])
    midGrade = random.randint(20, 100)
    finalGrade = random.randint(20,100)
    overallGrade = int((midGrade +finalGrade )/2)
    teacher = fake.profile()['name']
    zinj = """INSERT INTO %s ( login, hashedPass, name, surname, userType, email, phone, birthday, address, photo, permissionLvl)
        VALUES ('%s', '%s', '%s','%s', '%s', '%s','%s', '%s', '%s', '%s', %s);""" % (TABLE_USERS, username, hPass, fname,
                                                                                     sname, userType, email, phone,
                                                                                     birthday, address, photo, pLVL)
    session.execute(zinj)

    zinj = """INSERT INTO %s ( sId,sName,sSurname,sAddress,sEmail,sPhone,sBirthday,sPhoto
    ,isFullFamily,p1FullName,p1Phone,p2FullName,p2Phone,financialCase
    ,medicalConditions,studyYear,studyGroup)
                VALUES (%s, '%s', '%s','%s', '%s', '%s','%s', '%s', %s, '%s','%s', '%s', '%s','%s', '%s', %s, '%s');""" \
           % (TABLE_STUDENTS, sId, fname, sname, address, email, phone, birthday, photo
              , isFullFamily, p1FullName, p1Phone, p2FullName, p2Phone, financialCase
              , medicalConditions, studyYear, studyGroup)
   # print(zinj)
    session.execute(zinj)

    zinj = """INSERT INTO %s ( sId,sName,sSurname,subject,midGrade,finalGrade, overallGrade
                ,teacher,p1FullName,p1Phone,p2FullName,p2Phone,studyYear,studyGroup)
                VALUES (%s, '%s', '%s','%s', '%s', '%s','%s', '%s', '%s', '%s','%s', '%s', %s,'%s');""" \
           % (TABLE_GRADES, sId,fname,sname,subject,midGrade,finalGrade, overallGrade
            ,teacher,p1FullName,p1Phone,p2FullName,p2Phone,studyYear,studyGroup)
    #print(zinj)
    session.execute(zinj)


print('Time taken to generate tests is : ' + str(time.time()-t1) + ' SECONDS')



'''

login, hashedPass, name, surname, userType,
email, phone, birthday, address, photo,
permissionLvl,sId,sName,sSurname,sAddress,sEmail,sPhone,sBirthday,sPhoto
,isFullFamily,p1FullName,p1Phone,p2FullName,p2Phone,financialCase
,medicalConditions,studyYear,studyGroup,sId,sName,sSurname,subject,midGrade,overallGrade
,teacher,p1FullName,p1Phone,p2FullName,p2Phone,studyYear,studyGroup
'''