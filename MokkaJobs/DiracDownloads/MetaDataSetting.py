import os

from DIRAC.Core.Base import Script
Script.parseCommandLine()
from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient

evtType = 'Z_uds'
jobDescription = 'JERDetailed'
detNumber = 38
fileType = 'Sim'

energies = [550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800, 1850, 1900, 1950, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000]
#energies = [30,40,50,60,70,80]

fc = FileCatalogClient()
for energy in energies:
    path = '/ilc/user/s/sgreen/JERDetailed/MokkaJobs/Detector_Model_' + str(detNumber) + '/' + evtType + '/' + str(energy) + 'GeV' 
    pathdict = {'path':path, 'meta':{'Energy':energy, 'EvtType':evtType, 'JobDescription':jobDescription, 'MokkaJobNumber':detNumber, 'Type':fileType}}
    res = fc.setMetadata(pathdict['path'], pathdict['meta'])
