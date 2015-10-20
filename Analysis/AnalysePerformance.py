#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess

detModel = 38
recoVar = 43 

executable = "/usera/sg568/ilcsoft_Mod_v01_17_07/PandoraAnalysis/bin/AnalysePerformance"
results = ''

# Detailed JER

results += '-----------------------------------------------------------------------------------------------------------------------------------\n'
results += 'Detector Model ' + str(recoVar) + '\n'
results += '-----------------------------------------------------------------------------------------------------------------------------------\n'   

for pandoraSettings in ['Muon', 'Default', 'PerfectPhoton', 'PerfectPhotonNK0L', 'PerfectPFA']:
    results += pandoraSettings + '\n'

    for jetEnergy in ['30', '40', '50', '60', '70', '80', '91', '100', '110', '120', '130', '140', '150', '160', '170', '180', '190', '200', '220', '240', '260', '280', '300', '350', '400', '450', '500']:
        inputRootFileFolder = "/r06/lc/sg568/JERDetailed/RootFiles/Detector_Model_" + str(detModel) + "/Reco_Var_" + str(recoVar) + "/" + str(jetEnergy) + "GeV/"
        outputRootFileFolder = inputRootFileFolder
        inputRootFileFormat = "MarlinReco_MokkaSim_Detector_Model_" + str(detModel) + "_Z_uds_" + str(jetEnergy) + "GeV_*_" + pandoraSettings + ".root"
        outputRootFileName = "PfoAnalysisHistorgrams_Detector_Model_" + str(detModel) + "_Reco_Var_" + str(recoVar) + "_uds" + jetEnergy + "GeV_PandoraSettings" + pandoraSettings + ".root"

        argsString = executable + ' ' + inputRootFileFolder + inputRootFileFormat + ' ' + outputRootFileFolder + outputRootFileName 
        args = argsString.split()
        popen = subprocess.Popen(args, stdout=subprocess.PIPE)
        popen.wait()
        output = popen.stdout.read()

        resultsLine = ''
        for line in output.splitlines():
            if 'fPFA_L7A' in line:
                resultsLine = line

        results += jetEnergy + ' GeV Di Jet Energy:' + resultsLine + '\n'
results += '\n'

resultsFile = open("Detector_Model_" + str(detModel) + "_Reco_Var_" + str(recoVar) + "Results.txt", "w")
resultsFile.write(results)
resultsFile.close()

