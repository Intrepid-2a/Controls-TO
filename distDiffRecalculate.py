import pandas as pd

from distDiffsHorizontal import *


def recalculateDistances():


    log = pd.read_csv('../data/distHorizontal/calibration_log.csv')

    participants = log['ID'].unique()

    for ppno in range(3):
    # for ppno in range(len(participants)):
        participant = participants[ppno]

        plog = log[log['ID'] == participant]

        for hemifield in ['LH', 'RH']:

            hlog = plog[plog['hemifield'] == hemifield]

            ntrials = hlog.shape[0]

            filename = hlog['file'].unique()

            print([participant, hemifield, ntrials])

            getHorizontalRunDistanceDifferences(ID=participant, hemifield={'LH':'left', 'RH':'right'}[hemifield], location='toronto', runtrials=ntrials, log=hlog)

            print('done?\n')

