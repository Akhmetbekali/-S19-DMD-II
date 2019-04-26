import time

import coloredlogs, logging
from mpl_toolkits.mplot3d import Axes3D
from Randomizer import randomizeData
from create_tables import create_session
import matplotlib.pyplot as plt

plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import numpy as np

coloredlogs.install()

import warnings

warnings.filterwarnings("ignore",
                        category=DeprecationWarning)  # some cassandra features are deprecated in python 3.7, suspend it
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider


class Histo:
    def __init__(self, flag=True):  # Flag is sat to true if user wants to call randomizer
        logging.info("Logging in ...\n")
        auth_provider = PlainTextAuthProvider(username='cassandra', password='cassandra')
        cluster = Cluster(auth_provider=auth_provider)
        self.session = cluster.connect()
        self.plot_array = []
        self.chosen_one = []
        logging.info("Creating tables here please wait and be patient ...\n")
        create_session(session=self.session)
        logging.info("Table creation was successful")

    def plot_histo(self, study_year, subject):
        # query = """select studygroup, overallgrade from esas.grades where studyyear = %s and studygroup in ('1', '2', '3', '4', '5') and subject = '%s';""" % (study_year, subject)
        rows = self.session.execute(
            "select studygroup, overallgrade from esas.grades where studyyear = %s and studygroup in ('1', '2', '3', '4', '5') and subject = '%s';" % (
                study_year,
                subject))

        study_gr_avg = [0 for i in range(6)]
        cnt_ar = [0 for i in range(6)]
        for i in rows:
            s = i.studygroup
            grade = i.overallgrade
            ind = int(s)
            study_gr_avg[ind] += grade
            cnt_ar[ind] = cnt_ar[ind] + 1

        for i in range(6):
            if cnt_ar[i] == 0:
                continue
            study_gr_avg[i] = 5 * study_gr_avg[i] / (100 * cnt_ar[i])
        print(study_gr_avg)
        out = []
        for i in study_gr_avg:
            if i == 0:
                continue
            out.append(i)

        objects = ('1st group', '2nd group', '3rd group', '4th group', '5th group')
        y_pos = np.arange(len(objects))
        performance = out

        plt.bar(y_pos, performance, align='center', alpha=0.5)
        plt.xticks(y_pos, objects)
        plt.ylabel('Performance')
        plt.title('Average performance of each study group')

        plt.show()


obj = Histo(flag=False)
obj.plot_histo(2, 'Arabic')
