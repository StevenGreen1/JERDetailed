# Example to submit Marlin job: MarlinExample.py
import os
import sys

from DIRAC.Core.Base import Script
Script.parseCommandLine()
from ILCDIRAC.Interfaces.API.DiracILC import  DiracILC
from ILCDIRAC.Interfaces.API.NewInterface.UserJob import *
from ILCDIRAC.Interfaces.API.NewInterface.Applications import *

from MarlinGridJobs import *

#===== User Input =====

jobDescription = 'JERDetailed'
mokkaJobNumber = sys.argv[1] # Default detector model
recoStageNumber = sys.argv[2] # MHHHE off and large timing cuts 

#eventsToSimulate = [ { 'EventType': "Z_uds"  , 'EventsPerFile' : 1000 , 'Energies':  [91,100,110,120,130,140,150,160,170,180,190,200,220,240,260,280,300,350,400,450,500] } ]
eventsToSimulate = [ { 'EventType': "Z_uds"  , 'EventsPerFile' : 1000 , 'Energies':  [30,40,50,60,70,80,91,100,110,120,130,140,150,160,170,180,190,200,220,240,260,280,300,350,400,450,500] } ]

baseXmlFile = 'TemplateRepository/MarlinSteeringFileTemplate_Jets_1.xml'

pandoraSettingsFiles = {}
pandoraSettingsFiles['Default'] = 'PandoraSettings/PandoraSettingsDefault_SiW_5x5.xml' 
pandoraSettingsFiles['Default_LikelihoodData'] = 'PandoraSettings/PandoraLikelihoodData9EBin_SiW_5x5.xml' 
pandoraSettingsFiles['Muon'] = 'PandoraSettings/PandoraSettingsMuon.xml'
pandoraSettingsFiles['PerfectPhoton'] = 'PandoraSettings/PandoraSettingsPerfectPhoton.xml'
pandoraSettingsFiles['PerfectPhotonNK0L'] = 'PandoraSettings/PandoraSettingsPerfectPhotonNeutronK0L.xml'
pandoraSettingsFiles['PerfectPFA'] = 'PandoraSettings/PandoraSettingsPerfectPFA.xml'

#===== Second level user input =====
# If using naming scheme doesn't need changing 

#gearFile = '/usera/xu/ILCSOFT/myGridDownload/ILD_o1_v06_SiW_5x5.gear'
#gearFile = '/usera/sg568/ilcsoft_v01_17_07/HCalToEMCalibrationTesting/MokkaJobs/GearFiles/ILD_o1_v06_Detector_Model_' + str(mokkaJobNumber) + '.gear'
#calibConfigFile = 'CalibrationConfigFiles/Stage' + str(recoStageNumber) + 'Config_5x5_30x30.py'
gearFile = '/r04/lc/sg568/HCAL_Optimisation_Studies/GridSandboxes/GJN' + str(mokkaJobNumber) + '_OutputSandbox/ILD_o1_v06_GJN' + str(mokkaJobNumber) + '.gear'
calibConfigFile = '/r04/lc/sg568/HCAL_Optimisation_Studies/CalibrationResults/Detector_Model_' + str(mokkaJobNumber) + '/Reco_Stage_' + str(recoStageNumber) + '/CalibConfig_DetModel' + str(mokkaJobNumber) + '_RecoStage' + str(recoStageNumber) + '.py'

#=====

# Copy gear file and pandora settings files to local directory as is needed for submission.
os.system('cp ' + gearFile + ' .')
gearFileLocal = os.path.basename(gearFile)

pandoraSettingsFilesLocal = {}
for key, value in pandoraSettingsFiles.iteritems():
    os.system('cp ' + value + ' .')
    pandoraSettingsFilesLocal[key] = os.path.basename(value)

# Start submission
JobIdentificationString = jobDescription + '_Detector_Model_' + str(mokkaJobNumber) + '_Reco_' + str(recoStageNumber)
diracInstance = DiracILC(withRepo=True,repoLocation="%s.cfg" %( JobIdentificationString))

for eventSelection in eventsToSimulate:
    eventType = eventSelection['EventType']
    for energy in eventSelection['Energies']:
        slcioFilesToProcess = getSlcioFiles(jobDescription,38,energy,eventType)
        for slcioFile in slcioFilesToProcess:
            print 'Submitting ' + eventType + ' ' + str(energy) + 'GeV jobs.  Detector model ' + str(mokkaJobNumber) + '.  Reconstruction stage ' + str(recoStageNumber) + '.'  
            marlinSteeringTemplate = ''
            marlinSteeringTemplate = getMarlinSteeringFileTemplate(baseXmlFile,calibConfigFile)
            marlinSteeringTemplate = setPandoraSettingsFile(marlinSteeringTemplate,pandoraSettingsFilesLocal)
            marlinSteeringTemplate = setGearFile(marlinSteeringTemplate,gearFileLocal)

            slcioFileNoPath = os.path.basename(slcioFile)
            marlinSteeringTemplate = setInputSlcioFile(marlinSteeringTemplate,slcioFileNoPath)
            marlinSteeringTemplate = setOutputFiles(marlinSteeringTemplate,'MarlinReco_' + slcioFileNoPath[:-6])

            with open("MarlinSteering.steer" ,"w") as SteeringFile:
                SteeringFile.write(marlinSteeringTemplate)

            ma = Marlin()
            ma.setVersion('ILCSoft-01-17-07')
            ma.setSteeringFile('MarlinSteering.steer')
            ma.setGearFile(gearFileLocal)
            ma.setInputFile('lfn:' + slcioFile)

            outputFiles = []
            outputFiles.append('MarlinReco_' + slcioFileNoPath[:-6] + '_Default.root')
            outputFiles.append('MarlinReco_' + slcioFileNoPath[:-6] + '.slcio')
            if eventType == 'Z_uds':
                outputFiles.append('MarlinReco_' + slcioFileNoPath[:-6] + '_Muon.root')
                outputFiles.append('MarlinReco_' + slcioFileNoPath[:-6] + '_PerfectPhoton.root')
                outputFiles.append('MarlinReco_' + slcioFileNoPath[:-6] + '_PerfectPhotonNK0L.root')
                outputFiles.append('MarlinReco_' + slcioFileNoPath[:-6] + '_PerfectPFA.root')

            job = UserJob()
            job.setJobGroup(jobDescription)
            job.setInputSandbox(pandoraSettingsFilesLocal.values()) # Local files
            job.setOutputSandbox(['*.log','*.gear','*.mac','*.steer','*.xml'])
            job.setOutputData(outputFiles,OutputPath='/' + jobDescription + '/MarlinJobs/Detector_Model_' + str(mokkaJobNumber) + '/Reco_Stage_' + str(recoStageNumber) + '/' + eventType + '/' + str(energy) + 'GeV') # On grid
            job.setName(jobDescription + '_Detector_Model_' + str(mokkaJobNumber) + '_Reco_' + str(recoStageNumber))
            job.setBannedSites(['LCG.IN2P3-CC.fr','LCG.IN2P3-IRES.fr','LCG.KEK.jp'])
            job.dontPromptMe()
            res = job.append(ma)

            if not res['OK']:
                print res['Message']
                exit()
            job.submit(diracInstance)
            os.system('rm *.cfg')

# Tidy Up
os.system('rm MarlinSteering.steer')
os.system('rm ' + gearFileLocal)
for key, value in pandoraSettingsFilesLocal.iteritems():
    os.system('rm ' + value)

