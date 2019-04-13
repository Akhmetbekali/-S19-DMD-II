import coloredlogs, logging
from Randomizer import randomizeData
from create_tables import create_session
coloredlogs.install()

import warnings
warnings.filterwarnings("ignore",
                        category=DeprecationWarning)  # some cassandra shit is deprecated in python 3.7, suspend it
from cassandra.cluster import Cluster


class CassandraDriver:
    def __init__(self,flag=True):
        cluster = Cluster()
        self.session = cluster.connect()
        print("Creating tables here please wait and be patient ...")
        create_session(session=self.session)
        print("Table creation was successful")
        if flag:
            print("Flag was sat to True Initiating randomizing data please wait for ~1 minute")
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

    def geospacial_search_get(self, list_of_subjects, age_list, plot_flag=False):
        rows = []
        query = "SELECT * FROM ESAS.Grades WHERE"
        ok = True
        for i in list_of_subjects:
            if not ok:
                query = query + " or "
            temp = """subject = '%s' """, i
            query += temp
        query += ";"

        return query


def showdata(data):
    for row in data:
        print(row)


obj = CassandraDriver()

#print(obj.geospacial_search_get(['Arabic'], [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]))

# data = obj.students_in_birthdate_range('1900-10-10', '2010-01-01')
# showdata(data)
# print(data)
