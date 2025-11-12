import pandas as pd

from eccDiffsHorizontal import *
from eccDiffsAsynchronous import *
from eccDiffsUpScaledAsynchronous import *


def recalculateDistances(task):


    log = pd.read_csv('../data/%s/calibration_log.csv'%(task))

    participants = log['ID'].unique()

    # for ppno in range(1):
    for ppno in range(len(participants)):
        participant = participants[ppno]

        plog = log[log['ID'] == participant]
        # print(plog)

        for hemifield in ['LH', 'RH']:
        # for hemifield in ['LH']:

            hlog = plog[plog['hemifield'] == hemifield]

            ntrials = hlog.shape[0]

            filename = hlog['file'].unique()

            # print([participant, hemifield, ntrials])
            if task == 'distHorizontal':
                getHorizontalRunDistanceDifferences(ID=participant, hemifield={'LH':'left', 'RH':'right'}[hemifield], location='toronto', runtrials=ntrials, log=hlog)

            if task == 'distAsynchronous':
                getAsynchronouseRunDistanceDifferences(ID=participant, hemifield={'LH':'left', 'RH':'right'}[hemifield], location='toronto', runtrials=ntrials, log=hlog)

            if task == 'distUpScaledAsynchronous':
                getUpScaledAsynchronousRunDistanceDifferences(ID=participant, hemifield={'LH':'left', 'RH':'right'}[hemifield], location='toronto', runtrials=ntrials, log=hlog)
            # print('done?\n')

