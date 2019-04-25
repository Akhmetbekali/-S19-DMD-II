import coloredlogs, logging
from Randomizer import randomizeData
from create_tables import create_session
from datetime import date
import math
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

coloredlogs.install()

import warnings
warnings.filterwarnings("ignore",
                        category=DeprecationWarning)  # some cassandra features are deprecated in python 3.7, suspend it
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider


class CassandraDriver:
    def __init__(self, flag=True):  # Flag is sat to true if user wants to call randomizer
        logging.info("Logging in ...\n")

        auth_provider = PlainTextAuthProvider(username='cassandra', password='cassandra')
        cluster = Cluster(auth_provider=auth_provider)
        self.session = cluster.connect()
        self.plot_array = []

        logging.info("Creating tables here please wait and be patient ...\n")
        create_session(session=self.session)
        logging.info("Table creation was successful")

        auth_provider = PlainTextAuthProvider(username='admin', password='admin')
        cluster = Cluster(auth_provider=auth_provider)
        self.session = cluster.connect()
        self.session.execute('USE ESAS')
        self.session.execute('DROP ROLE IF EXISTS cassandra')
        self.session.execute("CREATE ROLE IF NOT EXISTS cassandra WITH PASSWORD = 'cassandra' AND LOGIN = true AND SUPERUSER = true")

        if flag:
            logging.info("Flag was sat to True Initiating randomizing data please wait for ~1 minute")
            randomizeData(session=self.session, MAX=10)
        else:
            logging.info("Flag was sat to False there will be no randomizing data\n")

    def get_near_by_grades(self, subject, grade, radius,
                           status='overallGrade'):  # this function returns the
        # student that have close grades to each other
        # status states if its final, or midterm
        assert (status == "overallGrade" or status == "finalGrade" or status == "midGrade")
        query = """SELECT * FROM ESAS.Grades WHERE %s >= %s and %s <= %s and subject = '%s' ALLOW FILTERING;""" \
                % (status, grade - radius, status, grade + radius, subject)
        result = self.session.execute(query)
        return result

    def students_in_birthdate_range(self, date1, date2):
        query = """SELECT * FROM ESAS.Students WHERE sBirthday >= '%s' and sBirthday <= '%s' ALLOW FILTERING;""" % \
                (date1, date2)
        result = self.session.execute(query)
        return result

    def get_age(self, sid):
        rows = self.session.execute("""SELECT sBirthday from ESAS.Students WHERE sId = %s ALLOW FILTERING;""" % sid)
        # print(rows)
        # assert (len(rows.current_rows) == 1)
        bb = str(rows[0].sbirthday)
        y, m, d = bb.split('-')
        y = -int(y) + int(date.today().strftime("%Y"))
        # print(y)
        return y

    def search_in_list(self, some_list, var):
        for i in some_list:
            if i == var:
                return True
        return False

    def get_index(self, some_list, var):
        N = len(some_list)
        for i in range(N):
            if some_list[i] == var:
                return i
        return -1

    def get_data_from_tables(self, list_of_subjects, age_list):
        rows = []
        hash_map = {'name': 0}
        for i in list_of_subjects:
            query = """SELECT ssurname, sname, overallGrade, 
                    sid FROM ESAS.Grades WHERE subject = '%s' ALLOW FILTERING;""" \
                    % i
            temp_array = self.session.execute(query)
            for j in temp_array:
                name = j.sname + " " + j.ssurname
                age = self.get_age(j.sid)
                if self.search_in_list(age_list, age):
                    # print(self.get_age(j.sid))
                    rows.append([name, age, i, j.overallgrade, j.sid])
                    cnt = hash_map.get(j.sid)
                    if not cnt:
                        cnt = 0
                        hash_map.update({j.sid: cnt + 1})
                    else:
                        cnt = cnt + 1

        return rows

    def create_table(self, name, cols):
        temp = ""
        for i in cols:
            temp += i[0] + " " + i[1] + ",\n"
        query = """
                    CREATE TABLE IF NOT EXISTS ESAS.%s (
                       %s
                       sId int, 
                        PRIMARY KEY (sId)
                    );
                    """ % (name, temp)
        self.session.execute('GRANT SELECT ON ESAS.%s TO clerk;' % name)
        self.session.execute('GRANT SELECT ON ESAS.%s TO principal;' % name)
        self.session.execute('GRANT SELECT ON ESAS.%s TO teacher;' % name)
        logging.info("Creating new table %s please wait ..." % name)

        self.session.execute(query)
        logging.info("Creating indexes for %s ..." % name)
        self.session.execute('CREATE INDEX IF NOT EXISTS i_spacial_distance ON %s (Spacial_Distance);' % name)
        self.session.execute("TRUNCATE TABLE ESAS.Spacial_Table;")

    def geospacial_search_get(self, list_of_subjects, age_list, plot_flag=False):
        rows = self.get_data_from_tables(list_of_subjects, age_list)
        N = len(rows)
        self.create_table('Spacial_Table',
                          [['Student1', 'text'], ['Student2', 'text'], ['Spacial_Distance', 'double']])
        normalized_array = [[] for i in range(N)]
        students_list = []
        counter = 0
        if plot_flag == True and len(list_of_subjects) != 2:
            print("You cannot plot if you have more than 3 dimensions, age, subj1, subj2")
            assert 0
        X = []
        Y = []
        Z = []
        for i in rows:
            sid = i[4]
            name = i[0]
            age = i[1]
            if not self.search_in_list(students_list, sid):
                students_list.append(sid)
            ind = self.get_index(students_list, sid)
            if len(normalized_array[ind]) == 0:
                normalized_array[ind].append(name)
                normalized_array[ind].append(age)
                normalized_array[ind].append(sid)
                normalized_array[ind].append([i[2], i[3]])
            else:
                normalized_array[ind].append([i[2], i[3]])

        for i in normalized_array:
            if len(i) == 0:
                break
            for j in range(3, len(i)):
                element = i[j]
                if element[0] == list_of_subjects[0]:
                    X.append(element[1])
                elif element[0] == list_of_subjects[1]:
                    Y.append(element[1])
            Z.append(i[1])
        self.plot_array = [X, Y, Z]

        for st1 in normalized_array:
            if len(st1) == 0:
                break
            for st2 in normalized_array:
                if len(st2) == 0:
                    break
                res = 0
                if st1[2] == st2[2]:
                    continue
                for i in range(3, len(st1)):
                    # print(st1[i][1])
                    # print(st1[i][0])
                    # input()
                    res += abs(st1[i][1] - st2[i][1]) * abs(st1[i][1] - st2[i][1])
                counter += 1
                self.insert_into('Spacial_Table', counter, st1[0], st2[0], math.sqrt(res))

        return self.session.execute("SELECT * FROM ESAS.spacial_table;")

    def insert_into(self, table_name, sid, name1, name2, distance):
        query = """INSERT INTO ESAS.%s (sid, Student1, Student2, Spacial_Distance) VALUES (%s, '%s', 
        '%s',  %s);""" \
                % (table_name, sid, name1, name2, distance)

        self.session.execute(query)

    def show_graph(self, list_of_subjects):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        # Data for a three-dimensional line
        X, Y, Z = self.plot_array
        ax.scatter(X, Y, Z, c='r', marker='o')
        ax.set_xlabel(list_of_subjects[0] + " grade")
        ax.set_ylabel(list_of_subjects[1] + " grade")
        ax.set_zlabel("age")
        plt.show()


def showdata(data):
    for row in data:
        print(row)


obj = CassandraDriver(flag=False)

rowData = obj.geospacial_search_get(['Arabic', 'Math'], [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18])
obj.show_graph(['Arabic', 'Math'])
# data = obj.students_in_birthdate_range('1900-10-10', '2010-01-01')¶
# showdata(data)¶
# print(data)