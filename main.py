import coloredlogs, logging

coloredlogs.install()

import warnings

warnings.filterwarnings("ignore",
                        category=DeprecationWarning)  # some cassandra shit is deprecated in python 3.7, suspend it

from cassandra.cluster import Cluster

cluster = Cluster()
session = cluster.connect()

KEYSPACE = 'ESAS'
TABLE_USERS = KEYSPACE + '.Users'
TABLE_STUDENTS = KEYSPACE + '.Students'
TABLE_GRADES = KEYSPACE + '.Grades'

# Keyspace
'''
session.execute("DROP TABLE ESAS.Grades;")
session.execute("DROP TABLE ESAS.Students;")
session.execute("DROP TABLE ESAS.Users;")
'''

logging.info("Creating keyspace %s ..." % KEYSPACE)
session.execute("""
        CREATE KEYSPACE IF NOT EXISTS %s
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
        """ % KEYSPACE)

logging.info("Setting keyspace %s ..." % KEYSPACE)
session.execute('USE %s' % KEYSPACE)

# Users

logging.info("Creating table %s ..." % TABLE_USERS)
session.execute("""
        CREATE TABLE IF NOT EXISTS %s (
            login text, 
            hashedPass text, 
            name ascii, 
            surname ascii, 
            userType text,
            email text,
            phone text,
            birthday date,
            address ascii,
            photo ascii,
            permissionLvl tinyint,
            PRIMARY KEY ((userType), surname, name)
        );
        """ % TABLE_USERS)

logging.info("Creating indexes for %s ..." % TABLE_USERS)
session.execute('CREATE INDEX IF NOT EXISTS i_login ON %s (login);' % TABLE_USERS)
session.execute('CREATE INDEX IF NOT EXISTS i_hashedPass ON %s (hashedPass);' % TABLE_USERS)

# Students

logging.info("Creating table %s ..." % TABLE_STUDENTS)
session.execute("""
        CREATE TABLE IF NOT EXISTS %s (
            sId uuid, 
            sName ascii, 
            sSurname ascii, 
            sAddress ascii, 
            sEmail text,
            sPhone text,
            sBirthday date,
            sPhoto ascii,
            isFullFamily boolean,
            p1FullName ascii,
            p1Phone text,
            p2FullName ascii,
            p2Phone text,
            financialCase text,
            medicalConditions text,
            studyYear tinyint,
            studyGroup text,

            PRIMARY KEY ((studyYear, studyGroup), sSurname, sName)
        );
        """ % TABLE_STUDENTS)

logging.info("Creating indexes for %s ..." % TABLE_STUDENTS)
session.execute('CREATE INDEX IF NOT EXISTS i_sId ON %s (sId);' % TABLE_STUDENTS)
session.execute('CREATE INDEX IF NOT EXISTS i_isFullFamily ON %s (isFullFamily);' % TABLE_STUDENTS)
session.execute('CREATE INDEX IF NOT EXISTS i_financialCase ON %s (financialCase);' % TABLE_STUDENTS)

# Grades

logging.info("Creating table %s ..." % TABLE_GRADES)
session.execute("""
        CREATE TABLE IF NOT EXISTS %s (
            sId uuid, 
            sName ascii, 
            sSurname ascii, 
            subject ascii, 
            midGrade int,
            finalGrade int,
            overallGrade int,
            teacher ascii,
            p1FullName ascii,
            p1Phone text,
            p2FullName ascii,
            p2Phone text,
            studyYear tinyint,
            studyGroup text,
            PRIMARY KEY ((studyYear, studyGroup), subject, overallGrade, sSurname, sName)
        );
        """ % TABLE_GRADES)

logging.info("Creating indexes for %s ..." % TABLE_GRADES)
session.execute('CREATE INDEX IF NOT EXISTS i_midGrade ON %s (midGrade);' % TABLE_GRADES)
session.execute('CREATE INDEX IF NOT EXISTS i_finalGrade ON %s (finalGrade);' % TABLE_GRADES)
session.execute('CREATE INDEX IF NOT EXISTS i_teacher ON %s (teacher);' % TABLE_GRADES)

# That's examples for you:

# Key fields must be inserted

session.execute("""
    INSERT INTO %s (login, hashedPass, userType, surname, name)
    VALUES ('%s', '%s', '%s', 'Name', 'Surname')
    """ % (TABLE_USERS, 'John', 123, 'SuperType')
                )

rows = session.execute('SELECT * FROM %s;' % TABLE_USERS)
for row in rows:
    print(row.login, row.hashedpass)  # p in hashedpass must not be capital for some reason...

# session.execute("""
#     TRUNCATE TABLE %s;
#     """ % (TABLE_USERS)
# )