# Submit Mokka jobs to the grid: MokkaSubmit.py
import os
import sys

from DIRAC.Core.Base import Script
Script.parseCommandLine()
from ILCDIRAC.Interfaces.API.DiracILC import  DiracILC
from ILCDIRAC.Interfaces.API.NewInterface.UserJob import *
from ILCDIRAC.Interfaces.API.NewInterface.Applications import *

from MokkaGridJobs import *

#===== User Input =====

detectorModelNumber = 38 # Default detector model

#eventsToSimulate = [ { 'EventType': "Z_uds"  , 'EventsPerFile' : 1000 , 'Energies':  ['91','100','110','120','130','140','150','160','170','180','190','200','220','240','260','280','300','350','400','450','500'] } ]
eventsToSimulate = [ { 'EventType': "Z_uds"  , 'EventsPerFile' : 1000 , 'Energies':  ['30','40','50','60','70','80'] } ]

baseXmlFile  = 'TemplateRepository/MokkaSteer.steer'
eventsPerJob = 1000

jobName = 'JERDetailed'

#===== Second level user input =====
# If using naming scheme doesn't need changing 

calibConfigFile = 'DetectorModelConfigFiles/Detector_Model_' + str(detectorModelNumber) + '_Config.py'
gearFile     = 'ILD_o1_v06_Detector_Model_' + str(detectorModelNumber) + '.gear'

#=====

# Start submission
JobIdentificationString = jobName + '_Default_Detector_Model_Reco_' + str(detectorModelNumber)
diracInstance = DiracILC(withRepo=True,repoLocation="%s.cfg" %( JobIdentificationString))

for eventSelection in eventsToSimulate:
    eventType = eventSelection['EventType']
    eventsPerFile = eventSelection['EventsPerFile']
    for energy in eventSelection['Energies']:
        hepevtFilesToProcess = getHEPEvtFiles(eventType,energy)
        jobNumber = 0
        #print hepevtFilesToProcess
        for hepevtFile in hepevtFilesToProcess:
            for startEvent in xrange(0, eventsPerFile, eventsPerJob):
                print 'Submitting ' + eventType + ' ' + energy + 'GeV jobs.  Detector model ' + str(detectorModelNumber) + '.  Start event number ' + str(startEvent) + '.'  

                jobNumber += eventsPerJob
                description = eventType + '_' + str(energy) + 'GeV'
                outputFile = 'MokkaSim_Detector_Model_' + str(detectorModelNumber) + '_' + description + '_' + str(eventsPerJob) + '_' + str(jobNumber) + '.slcio'
                outputPath = '/' + jobName + '/MokkaJobs/Detector_Model_' + str(detectorModelNumber) + '/' + eventType + '/' + str(energy) + 'GeV' 
                #outputPath = '/MokkaTesting' 

                mokkaSteeringTemplate = ''
                mokkaSteeringTemplate = getMokkaSteeringFileTemplate(baseXmlFile,calibConfigFile)
                mokkaSteeringTemplate = setGearFile(mokkaSteeringTemplate,gearFile)
                mokkaSteeringTemplate = setOutputFile(mokkaSteeringTemplate,outputFile)
                mokkaSteeringTemplate = setStartNumber(mokkaSteeringTemplate,startEvent)

                with open("MokkaSteering.steer" ,"w") as steeringFile:
                    steeringFile.write(mokkaSteeringTemplate)

                MokkaApplication = Mokka()
                MokkaApplication.setVersion(getMokkaVersion(calibConfigFile))
                MokkaApplication.setSteeringFile('MokkaSteering.steer')
                MokkaApplication.setNumberOfEvents(eventsPerJob)
                MokkaApplication.setStartFrom(startEvent)

                job = UserJob()
                job.setJobGroup(jobName)
                job.setOutputSandbox( ["*.log", "*.gear", "*.mac", "*.steer", "*.xml" ] )
                job.setOutputData(outputFile, OutputPath=outputPath)
                job.setInputData(hepevtFile)
                job.setName(jobName + '_Detector_Model_' + str(detectorModelNumber))
                job.setBannedSites(['LCG.IN2P3-CC.fr','LCG.IN2P3-IRES.fr','LCG.KEK.jp'])

                res = job.append(MokkaApplication)
                if not res['OK']:
                    print res['Message']
                    exit()
                job.dontPromptMe()
                job.submit(diracInstance)
                os.system('rm *.cfg')

# Tidy Up
os.system('rm MokkaSteering.steer')

