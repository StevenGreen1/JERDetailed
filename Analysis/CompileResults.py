#-----------------------------------------------------------------------------------------------------------------------------------
#Detector Model 43
#-----------------------------------------------------------------------------------------------------------------------------------
#Muon
#30 GeV Di Jet Energy:fPFA_L7A (6146 entries), rawrms: 1.6879, rms90: 1.2342 (26.6-32.05), mean: 29.3011, sigma: 0.402254+-0.00513102, sE/E: 5.95687+-0.0759839
#40 GeV Di Jet Energy:fPFA_L7A (6033 entries), rawrms: 1.97695, rms90: 1.42556 (36.1-42.55), mean: 39.2789, sigma: 0.346597+-0.00446229, sE/E: 5.13266+-0.0660808
#50 GeV Di Jet Energy:fPFA_L7A (6161 entries), rawrms: 2.25623, rms90: 1.62838 (45.6-52.95), mean: 49.2553, sigma: 0.315718+-0.00402229, sE/E: 4.67538+-0.059565

import os

detectorModel = 38
energyList = [30, 40, 50, 60, 70, 80, 91, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 220, 240, 260, 280, 300, 350, 400, 450, 500]
pandoraSettingsList = ['Default','PerfectPFA','PerfectPhoton','PerfectPhotonNK0L']
recoStageList = range(69,77)

for recoStage in recoStageList: 
    compiledFileName = 'Detector_Model_' + str(detectorModel) + '_Reco_Var_' + str(recoStage) + '_Results.txt'
    compiledFile = open(compiledFileName,'a')
    compiledFile.write('-----------------------------------------------------------------------------------------------------------------------------------\n')
    compiledFile.write('Reconstruction Variant ' + str(recoStage) + '\n')
    compiledFile.write('-----------------------------------------------------------------------------------------------------------------------------------\n')
    for pandora in pandoraSettingsList:
        compiledFile.write(pandora + '\n')
        for energy in energyList:
            fileName = '/r06/lc/sg568/JERDetailed/AnalysePerformanceResults/Detector_Model_' + str(detectorModel) + '/Reco_Stage_' + str(recoStage) + '/Z_uds/' + str(energy) + 'GeV/AnalysePerformance_PandoraSettings' + pandora + '_DetectorModel_' + str(detectorModel) + '_Reco_Stage_' + str(recoStage) + '_Z_uds_' + str(energy) + 'GeV.txt'            
            if os.path.isfile(fileName):
                resultsFile = open(fileName,'r')
                for line in resultsFile:
                    if 'fPFA_L7A' in line:
                        compiledFile.write(str(energy) + ' GeV Di Jet Energy:' + line)                     
            else:
                redoFileName = 'Redo.txt'
                redoFile = open(redoFileName,'a')
                redoFile.write(str(detectorModel) + ' ' + str(recoStage) + ' ' + str(energy) + ' ' + pandora + '\n')
                redoFile.close()
                #print 'Please redo the following sample:'
                #print 'Detector Model       : ' + str(detectorModel)
                #print 'Reconstruction Stage : ' + str(recoStage)
                #print 'Energy               : ' + str(energy)
                #print 'Pandora Settings     : ' + pandora
    compiledFile.close()

