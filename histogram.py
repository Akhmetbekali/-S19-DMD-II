import time

import coloredlogs, logging
from mpl_toolkits.mplot3d import Axes3D
from Randomizer import randomizeData
from create_tables import create_session
import matplotlib.pyplot as plt
from datetime import date
import math
from mpl_toolkits import mplot3d
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

        study_gr_avg = [0 for i in range(5)]
        cnt_ar = [0 for i in range(5)]
        for i in rows:
            ind = int(i['studygroup'])
            study_gr_avg[i['studygroup']] += i['overallgrade']
            cnt_ar[i['studygroup']] = cnt_ar[i['studygroup']] + 1

        for i in range(5):
            study_gr_avg[i] = study_gr_avg[i] / cnt_ar[i]


obj = Histo(flag=False)
obj.plot_histo(2, 'Arabic')
