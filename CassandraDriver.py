import coloredlogs, logging
from Randomizer import randomizeData
from create_tables import create_session
import matplotlib.pyplot as plt
from datetime import date

coloredlogs.install()

import warnings

warnings.filterwarnings("ignore",
                        category=DeprecationWarning)  # some cassandra shit is deprecated in python 3.7, suspend it
from cassandra.cluster import Cluster


class CassandraDriver:
    def __init__(self, flag=True):  # Flag is sat to true if user wants to call randomizer
        cluster = Cluster()
        self.session = cluster.connect()
        print("Creating tables here please wait and be patient ...")
        create_session(session=self.session)
        print("Table creation was successful")
        if flag:
            print("Flag was sat to True Initiating randomizing data please wait for ~2 minute")
            randomizeData(session=self.session)
        else:
            print("Flag was sat to False there will be no randomizing data")

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
                    cnt = hash_map.get(name)
                    if not cnt:
                        cnt = 0
                        hash_map.update({name: cnt + 1})
                    else:
                        cnt = cnt + 1
                        hash_map.update(name=cnt)
        res = []
        for i in rows:
            if hash_map.get(i[0]) == len(list_of_subjects):
                res.append(i)
        return res

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
        print("""Creating new table %s please wait ...""" % name)
        self.session.execute(query)
        logging.info("Creating indexes for %s ..." % name)
        self.session.execute('CREATE INDEX IF NOT EXISTS i_age ON %s (Age);' % name)
        self.session.execute('CREATE INDEX IF NOT EXISTS i_spacial_distance ON %s (Spacial_Distance);' % name)

    def geospacial_search_get(self, list_of_subjects, age_list, plot_flag=False):
        rows = self.get_data_from_tables(list_of_subjects, age_list)
        N = len(rows)
        self.create_table('Spacial_Table',
                          [['Student1', 'text'], ['Student2', 'text'], ['Spacial_Distance', 'double'], ['Age', 'int']])
        normalized_array = [[] for i in range(N)]
        students_list = []
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
                normalized_array[ind].append([i[2], i[3]])

        for i in range(0, N):
            for j in range(i + 1, N):
                sid = i * N + j
                row1 = rows[i]
                row2 = rows[j]
                student1 = row1[0]
                age1 = row1[1]
                grade1 = row1[2]
                student2 = row2[0]
                age2 = row2[1]
                grade2 = row2[2]

        return rows


def showdata(data):
    for row in data:
        print(row)


obj = CassandraDriver(flag=False)

rowData = obj.geospacial_search_get(['Arabic', 'Math'], [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18])

# data = obj.students_in_birthdate_range('1900-10-10', '2010-01-01')
# showdata(data)
# print(data)
