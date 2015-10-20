import os

from DIRAC.Core.Base import Script
Script.parseCommandLine()
from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient

evtType = 'Z_uds'
jobDescription = 'JERDetailed'
detNumber = 38
fileType = 'Sim'

#energies = [91,100,110,120,130,140,150,160,170,180,190,200,220,240,260,280,300,350,400,450,500]
energies = [30,40,50,60,70,80]

fc = FileCatalogClient()
for energy in energies:
    path = '/ilc/user/s/sgreen/JERDetailed/MokkaJobs/Detector_Model_' + str(detNumber) + '/' + evtType + '/' + str(energy) + 'GeV' 
    pathdict = {'path':path, 'meta':{'Energy':energy, 'EvtType':evtType, 'JobDescription':jobDescription, 'MokkaJobNumber':detNumber, 'Type':fileType}}
    res = fc.setMetadata(pathdict['path'], pathdict['meta'])
