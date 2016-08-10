import os
import re
import time
import threading

from DIRAC.Core.Base import Script
Script.parseCommandLine()
from DIRAC.DataManagementSystem.Client.DataManager import DataManager
from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient
from DIRAC.Core.Utilities.ReturnValues import returnSingleResult

#=================================

jobDescription = 'JERDetailed'

eventsToDownload = [
                       { 'EventType': "Kaon0L" , 'Energies':  ['10', '20', '30', '40', '50', '60', '70', '80', '90', '100', '200', '500'], 'DetectorModel': 'clic_ild_cdr' }
                       { 'EventType': "Photon" , 'Energies':  ['10'], 'DetectorModel': 'clic_ild_cdr' }
                       { 'EventType': "Muon" , 'Energies':  ['10'], 'DetectorModel': 'clic_ild_cdr' }
                   ]

maxThread = 100
fileType = 'Sim'

#=================================

def downloadFile(dm, lfn, localFolder):
    res = returnSingleResult(dm.getFile(lfn, localFolder))
    if not res or not res['OK']:
        print "Error with file %s"%lfn
        print res
    else:
        print "Downloaded %s"%lfn

class ActivePool(object):
    def __init__(self):
        super(ActivePool, self).__init__()
        self.active = []
        self.lock = threading.Lock()
    def makeActive(self, name):
        with self.lock:
            self.active.append(name)
    def makeInactive(self, name):
        with self.lock:
            self.active.remove(name)

def worker(threadingSemaphore, pool, dm, lfn, localFolder):
    with threadingSemaphore:
        name = threading.currentThread().getName()
        pool.makeActive(name)
        downloadFile(dm, lfn, localFolder)
        pool.makeInactive(name)

#=================================

fc = FileCatalogClient()
dm = DataManager()

pool = ActivePool()
threadingSemaphore = threading.Semaphore(maxThread)

for eventSelection in eventsToDownload:
    eventType = eventSelection['EventType']
    detectorModel = eventSelection['DetectorModel']

    for energy in eventSelection['Energies']:
        path = '/r06/lc/sg568/' + jobDescription + '/Slcio/Detector_Model_' + str(detectorModel) 

        if not os.path.exists(path):
            os.makedirs(path)

        meta = {}
        meta['JobDescription'] = jobDescription
        meta['Type'] = fileType
        meta['DetectorModel'] = str(detectorModel)
        meta['Energy'] = str(energy)
        meta['EvtType'] = eventType

        res = fc.findFilesByMetadata(meta)
        if not res['OK']:
            print res['Message']

        lfns = res['Value']

        for lfn in lfns:
            localFile = os.path.basename(lfn)
            if not os.path.isfile(localFile):
                while threading.activeCount() > (maxThread * 2):
                    time.sleep(5)

                downloadThread = threading.Thread(target=worker, name=str(localFile), args=(threadingSemaphore, pool, dm, lfn, path))
                downloadThread.start()

currentThread = threading.currentThread()

for thread in threading.enumerate():
    if thread is currentThread:
        continue
    thread.join(500)

print 'Download script has finished.'
