import coloredlogs, logging
coloredlogs.install()


def create_session(session):
    # session.execute("DROP ROLE IF EXISTS principal")
    # session.execute("DROP ROLE IF EXISTS teacher")
    # session.execute("DROP ROLE IF EXISTS clerk")
    # session.execute("DROP ROLE IF EXISTS admin")

    session.execute("CREATE ROLE IF NOT EXISTS admin WITH PASSWORD = 'admin' AND LOGIN = true AND SUPERUSER = true")
    session.execute("CREATE ROLE IF NOT EXISTS principal WITH PASSWORD = 'principal' AND LOGIN = true")
    session.execute("CREATE ROLE IF NOT EXISTS clerk WITH PASSWORD = 'clerk' AND LOGIN = true")
    session.execute("CREATE ROLE IF NOT EXISTS teacher WITH PASSWORD = 'teacher' AND LOGIN = true")

    KEYSPACE = 'ESAS'
    TABLE_USERS = KEYSPACE + '.Users'
    TABLE_STUDENTS = KEYSPACE + '.Students'
    TABLE_GRADES = KEYSPACE + '.Grades'

    # session.execute("DROP TABLE ESAS.Grades;")
    # session.execute("DROP TABLE ESAS.Students;")
    # session.execute("DROP TABLE ESAS.Users;")

    # Keyspace

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

    logging.info("Creating indexes for %s ...\n" % TABLE_GRADES)
    session.execute('CREATE INDEX IF NOT EXISTS i_midGrade ON %s (midGrade);' % TABLE_GRADES)
    session.execute('CREATE INDEX IF NOT EXISTS i_finalGrade ON %s (finalGrade);' % TABLE_GRADES)
    session.execute('CREATE INDEX IF NOT EXISTS i_teacher ON %s (teacher);' % TABLE_GRADES)

    # Permissions
    logging.info("Granting permissions...\n")

    session.execute('GRANT SELECT ON %s to teacher;' % TABLE_STUDENTS)
    session.execute('GRANT SELECT ON %s to teacher;' % TABLE_GRADES)
    session.execute('GRANT MODIFY ON %s to teacher;' % TABLE_GRADES)

    session.execute('GRANT SELECT ON KEYSPACE %s TO clerk;' % KEYSPACE)
    session.execute('GRANT MODIFY ON KEYSPACE %s TO clerk;' % KEYSPACE)

    session.execute('GRANT SELECT ON KEYSPACE %s TO principal;' % KEYSPACE)
    session.execute('GRANT MODIFY ON KEYSPACE %s TO principal;' % KEYSPACE)

    for perm in list(session.execute('LIST ALL PERMISSIONS'))[-7:]:
        logging.info(perm)

    # Example of queries:

    # session.execute("""
    #     INSERT INTO %s (login, hashedPass, userType, surname, name)
    #     VALUES ('%s', '%s', '%s', 'Name', 'Surname')
    #     """ % (TABLE_USERS, 'John', 123, 'SuperType')
    # )

    # rows = session.execute('SELECT * FROM %s;' % TABLE_USERS)
    #for row in rows:
        #print(row.login, row.hashedpass)  # p in hashedpass must not be capital for some reason...

    # session.execute("""
    #     TRUNCATE TABLE %s;
    #     """ % (TABLE_USERS)
    # )