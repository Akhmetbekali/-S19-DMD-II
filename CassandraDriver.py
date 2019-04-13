from Randomizer import randomizeData
from create_tables import create_session
import coloredlogs, logging
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
        logging.info("Creating tables here please wait and be patient ...\n")
        create_session(session=self.session)
        logging.info("Table creation was successful")
        if flag:
            logging.info("Flag was sat to True Initiating randomizing data please wait for ~1 minute")
            randomizeData(session=self.session)
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

    def geospacial_search_get(self, list_of_subjects, age_list, plot_flag=False):
        rows = []

        for i in list_of_subjects:
            query = """SELECT * FROM ESAS.Grades WHERE subject = '%s' ALLOW FILTERING;""" \
                    % i
            temp_array = self.session.execute(query)
            for j in temp_array:
                rows.append(j)

        return rows


def showdata(data):
    for row in data:
        print(row)


obj = CassandraDriver(flag=False)

rowData = obj.geospacial_search_get(['Arabic', 'Math'], [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19])
for i in rowData:
    print(i)

# data = obj.students_in_birthdate_range('1900-10-10', '2010-01-01')
# showdata(data)
# print(data)
