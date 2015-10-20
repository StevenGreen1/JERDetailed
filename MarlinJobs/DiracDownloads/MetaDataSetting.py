import os

from DIRAC.Core.Base import Script
Script.parseCommandLine()
from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient

evtType = 'Z_uds'
jobDescription = 'JERDetailed'
detNumber = 38
recoStage = 43
fileType = 'Rec'

#energies = [91,100,110,120,130,140,150,160,170,180,190,200,220,240,260,280,300,350,400,450,500]
energies = [30,40,50,60,70,80]

fc = FileCatalogClient()
for energy in energies:
    path = '/ilc/user/s/sgreen/' + jobDescription + '/MarlinJobs/Detector_Model_' + str(detNumber) + '/Reco_Stage_' + str(recoStage) + '/' + evtType + '/' + str(energy) + 'GeV'
    pathdict = {'path':path, 'meta':{'Energy':energy, 'EvtType':evtType, 'JobDescription':jobDescription, 'MokkaJobNumber':detNumber, 'ReconstructionVariant':recoStage, 'Type':fileType}}
    res = fc.setMetadata(pathdict['path'], pathdict['meta'])
