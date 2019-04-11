from cassandra.cluster import Cluster


class CassandraDriver:
    def __init__(self):
        cluster = Cluster()
        self.session = cluster.connect()

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


def showdata(data):
    for row in data:
        print(row)


obj = CassandraDriver()

data = obj.students_in_birthdate_range('1900-10-10', '2010-01-01')
showdata(data)
# print(data)
