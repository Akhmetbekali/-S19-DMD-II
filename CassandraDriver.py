 
import coloredlogs, logging

coloredlogs.install()

import warnings

warnings.filterwarnings("ignore",
                        category=DeprecationWarning)  # some cassandra shit is deprecated in python 3.7, suspend it

from cassandra.cluster import Cluster

class CassandraDriver:
    def __init__(self):
        cluster = Cluster()
        self.self.session = cluster.connect()

        KEYSPACE = 'ESAS'
        TABLE_USERS = KEYSPACE + '.Users'
        TABLE_STUDENTS = KEYSPACE + '.Students'
        TABLE_GRADES = KEYSPACE + '.Grades'

        # Keyspace
        '''
        self.session.execute("DROP TABLE ESAS.Grades;")
        self.session.execute("DROP TABLE ESAS.Students;")
        self.session.execute("DROP TABLE ESAS.Users;")
        '''

        logging.info("Creating keyspace %s ..." % KEYSPACE)
        self.session.execute("""
                CREATE KEYSPACE IF NOT EXISTS %s
                WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
                """ % KEYSPACE)

        logging.info("Setting keyspace %s ..." % KEYSPACE)
        self.session.execute('USE %s' % KEYSPACE)

        # Users

        logging.info("Creating table %s ..." % TABLE_USERS)
        self.session.execute("""
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
        self.session.execute('CREATE INDEX IF NOT EXISTS i_login ON %s (login);' % TABLE_USERS)
        self.session.execute('CREATE INDEX IF NOT EXISTS i_hashedPass ON %s (hashedPass);' % TABLE_USERS)

        # Students

        logging.info("Creating table %s ..." % TABLE_STUDENTS)
        self.session.execute("""
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
        self.session.execute('CREATE INDEX IF NOT EXISTS i_sId ON %s (sId);' % TABLE_STUDENTS)
        self.session.execute('CREATE INDEX IF NOT EXISTS i_isFullFamily ON %s (isFullFamily);' % TABLE_STUDENTS)
        self.session.execute('CREATE INDEX IF NOT EXISTS i_financialCase ON %s (financialCase);' % TABLE_STUDENTS)

        # Grades

        logging.info("Creating table %s ..." % TABLE_GRADES)
        self.session.execute("""
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
        self.session.execute('CREATE INDEX IF NOT EXISTS i_midGrade ON %s (midGrade);' % TABLE_GRADES)
        self.session.execute('CREATE INDEX IF NOT EXISTS i_finalGrade ON %s (finalGrade);' % TABLE_GRADES)
        self.session.execute('CREATE INDEX IF NOT EXISTS i_teacher ON %s (teacher);' % TABLE_GRADES)

        # That's examples for you:

        # Key fields must be inserted

        self.session.execute("""
            INSERT INTO %s (login, hashedPass, userType, surname, name)
            VALUES ('%s', '%s', '%s', 'Name', 'Surname')
            """ % (TABLE_USERS, 'John', 123, 'SuperType')
                        )

        rows = self.session.execute('SELECT * FROM %s;' % TABLE_USERS)
        #for row in rows:
           # print(row.login, row.hashedpass)  # p in hashedpass must not be capital for some reason...

    def get_near_by_grades(self, subject, grade, radius,
                           status='overallGrade'):  # this function returns the
        # student that have close grades to each other
        # status states if its final, or midterm
        assert (status == "overallGrade" or status == "finalGrade" or status == "midGrade")
        query = """SELECT * FROM ESAS.Grades WHERE %s >= %s and %s <= %s and subject = '%s' ALLOW FILTERING;""" \
                % (status, grade - radius, status, grade + radius, subject)
        result = self.self.session.execute(query)
        return result

    def students_in_birthdate_range(self, date1, date2):
        query = """SELECT * FROM ESAS.Students WHERE sBirthday >= '%s' and sBirthday <= '%s' ALLOW FILTERING;""" % \
                (date1, date2)
        result = self.self.session.execute(query)
        return result

    def geospacial_search_get(self, list_of_subjects, age_list, plot_flag=False):
        return
        




def showdata(data):
    for row in data:
        print(row)


obj = CassandraDriver()

data = obj.students_in_birthdate_range('1900-10-10', '2010-01-01')
showdata(data)
# print(data)
