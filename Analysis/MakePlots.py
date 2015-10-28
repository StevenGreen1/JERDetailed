#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
import math

thisFile = sys.argv[0]

from collections import defaultdict
JER = defaultdict(dict)
JERError = defaultdict(dict)

pandoraSettings = ''
pandoraSettingsList = ['Default','PerfectPhoton','PerfectPhotonNK0L','PerfectPFA','Muon']
jetEnergyList = [30, 40, 50, 60, 70, 80, 91, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 220, 240, 260, 280, 300, 350, 400, 450, 500]
detectorModel = sys.argv[1]
recoVar = sys.argv[2]
inputFileName = 'Detector_Model_' + str(detectorModel) + '_Reco_Var_' + str(recoVar) + '_Results.txt'

#===== Read data =====#

file = open(inputFileName)
allLines = file.readlines()
for line in allLines:
    regex = re.compile("Detector Model (\d+)")
    q = regex.search(line.strip()) 
    if q is not None:
        detectorModel = int(q.group(1))

    if line.rstrip() in pandoraSettingsList:
        pandoraSettings = line.rstrip() 

    regex = re.compile("(\d+) GeV Di Jet Energy:fPFA_L7A(.*?)sE\/E: (\d\.\d+)\+\-(\d\.\d+)")
    r = regex.search(line)
    if r is not None:
        energy = int(r.group(1))
        JER[(pandoraSettings,energy,detectorModel)] = float(r.group(3))
        JERError[(pandoraSettings,energy,detectorModel)] = float(r.group(4))

#===== Calculate Confusion Terms =====#

# Total Confusion
for energy in jetEnergyList:    
    JER[('TotalConfusion',energy,detectorModel)] = math.sqrt( math.fabs( (JER[('Default',energy,detectorModel)] * JER[('Default',energy,detectorModel)]) - (JER[('PerfectPFA',energy,detectorModel)] * JER[('PerfectPFA',energy,detectorModel)]) ) )
    JERError[('TotalConfusion',energy,detectorModel)] = math.sqrt( math.fabs( ( (JERError[('Default',energy,detectorModel)] * JERError[('Default',energy,detectorModel)] * JER[('Default',energy,detectorModel)] * JER[('Default',energy,detectorModel)]) / (JER[('TotalConfusion',energy,detectorModel)] * JER[('TotalConfusion',energy,detectorModel)]) ) - ( (JERError[('PerfectPFA',energy,detectorModel)] * JERError[('PerfectPFA',energy,detectorModel)] * JER[('PerfectPFA',energy,detectorModel)] * JER[('PerfectPFA',energy,detectorModel)]) / (JER[('TotalConfusion',energy,detectorModel)] * JER[('TotalConfusion',energy,detectorModel)]) ) ) )

# Photon Confusion
for energy in jetEnergyList:    
    JER[('PhotonConfusion',energy,detectorModel)] = math.sqrt( math.fabs( (JER[('Default',energy,detectorModel)] * JER[('Default',energy,detectorModel)]) - (JER[('PerfectPhoton',energy,detectorModel)] * JER[('PerfectPhoton',energy,detectorModel)]) ) )
    JERError[('PhotonConfusion',energy,detectorModel)] = math.sqrt( math.fabs( ( (JERError[('Default',energy,detectorModel)] * JERError[('Default',energy,detectorModel)] * JER[('Default',energy,detectorModel)] * JER[('Default',energy,detectorModel)]) / (JER[('PhotonConfusion',energy,detectorModel)] * JER[('PhotonConfusion',energy,detectorModel)]) ) - ( (JERError[('PerfectPhoton',energy,detectorModel)] * JERError[('PerfectPhoton',energy,detectorModel)] * JER[('PerfectPhoton',energy,detectorModel)] * JER[('PerfectPhoton',energy,detectorModel)]) / (JER[('PhotonConfusion',energy,detectorModel)] * JER[('PhotonConfusion',energy,detectorModel)]) ) ) )

# Neutral Hadron Confusion
for energy in jetEnergyList:
    JER[('NeutralHadronConfusion',energy,detectorModel)] = math.sqrt( math.fabs( (JER[('PerfectPhoton',energy,detectorModel)] * JER[('PerfectPhoton',energy,detectorModel)]) - (JER[('PerfectPhotonNK0L',energy,detectorModel)] * JER[('PerfectPhotonNK0L',energy,detectorModel)]) ) )    
    JERError[('NeutralHadronConfusion',energy,detectorModel)] = math.sqrt( math.fabs( ( (JERError[('PerfectPhoton',energy,detectorModel)] * JERError[('PerfectPhoton',energy,detectorModel)] * JER[('PerfectPhoton',energy,detectorModel)] * JER[('PerfectPhoton',energy,detectorModel)]) / (JER[('NeutralHadronConfusion',energy,detectorModel)] * JER[('NeutralHadronConfusion',energy,detectorModel)]) ) - ( (JERError[('PerfectPhotonNK0L',energy,detectorModel)] * JERError[('PerfectPhotonNK0L',energy,detectorModel)] * JER[('PerfectPhotonNK0L',energy,detectorModel)] * JER[('PerfectPhotonNK0L',energy,detectorModel)]) / (JER[('NeutralHadronConfusion',energy,detectorModel)] * JER[('NeutralHadronConfusion',energy,detectorModel)]) ) ) )

# Other Confusion
for energy in jetEnergyList:
    JER[('OtherConfusion',energy,detectorModel)] = math.sqrt( math.fabs( (JER[('PerfectPhotonNK0L',energy,detectorModel)] * JER[('PerfectPhotonNK0L',energy,detectorModel)]) - (JER[('PerfectPFA',energy,detectorModel)] * JER[('PerfectPFA',energy,detectorModel)]) ) )    
    JERError[('OtherConfusion',energy,detectorModel)] = math.sqrt( math.fabs( ( (JERError[('PerfectPhotonNK0L',energy,detectorModel)] * JERError[('PerfectPhotonNK0L',energy,detectorModel)] * JER[('PerfectPhotonNK0L',energy,detectorModel)] * JER[('PerfectPhotonNK0L',energy,detectorModel)]) / (JER[('OtherConfusion',energy,detectorModel)] * JER[('OtherConfusion',energy,detectorModel)]) ) - ( (JERError[('PerfectPFA',energy,detectorModel)] * JERError[('PerfectPFA',energy,detectorModel)] * JER[('PerfectPFA',energy,detectorModel)] * JER[('PerfectPFA',energy,detectorModel)]) / (JER[('OtherConfusion',energy,detectorModel)] * JER[('OtherConfusion',energy,detectorModel)]) ) ) )

#for x in JER.keys():print x,' : ',JER[x]
#for x in JERError.keys():print x,' : ',JERError[x]

#==== Make JER_vs_Ej =====#

saveString = '{\n'
saveString += 'gStyle->SetOptStat(0);\n'
saveString += 'TCanvas *pCanvasEj = new TCanvas();\n'
saveString += 'pCanvasEj->cd();\n'

saveString += 'TH2F *pAxesEj = new TH2F("axesEj","",1200,0,300,12000,0,6.5);\n'
saveString += 'pAxesEj->GetYaxis()->SetTitle("RMS_{90}(E_{j}) / Mean_{90}(E_{j}) [%]");\n'
saveString += 'pAxesEj->GetXaxis()->SetTitle("E_{j} [GeV]");\n'
saveString += 'pAxesEj->Draw();\n'

# Set jet energies
saveString += 'float jetEnergy[' + str(len(jetEnergyList)) + '] = {'
for energy in jetEnergyList:
    saveString += str(float(energy)/2.0)
    if energy is not '500':
        saveString += ','
saveString += '};\n'

# Set jet energy errors (all zeros but needed for TGraphErrors)
saveString += 'float jetEnergyError[' + str(len(jetEnergyList)) + '] = {'
for energy in jetEnergyList:
    saveString += str(0)
    if energy is not '500':
        saveString += ','
saveString += '};\n'

for pandoraSettings in ['Default','PerfectPFA','TotalConfusion','PhotonConfusion','NeutralHadronConfusion','OtherConfusion']:
    saveString += 'float ' + pandoraSettings + '_' + str(detectorModel) + '_JER[' + str(len(jetEnergyList)) + '] = {'
    for energy in jetEnergyList:
        saveString += str(JER[(pandoraSettings,energy,detectorModel)])
        if energy is not jetEnergyList[-1]:
            saveString += ','
    saveString += '};\n'
    saveString += 'float ' + pandoraSettings + '_' + str(detectorModel) + '_JERError[' + str(len(jetEnergyList)) + '] = {'
    for energy in jetEnergyList:
        saveString += str(JERError[(pandoraSettings,energy,detectorModel)])
        if energy is not jetEnergyList[-1]:
            saveString += ','
    saveString += '};\n'

rootLineColor = ['1','4','2','kOrange','8','6']
rootLineStyle = ['1','2','3','4','5','6']

saveString += 'TLegend *pLegend = new TLegend(0.6, 0.6, 0.9, 0.9);\n'

settingsCounter = 0
for pandoraSettings in ['Default','PerfectPFA','TotalConfusion','PhotonConfusion','NeutralHadronConfusion','OtherConfusion']:
    saveString += 'TGraphErrors *pTGraphErrors_' + pandoraSettings + '_' + str(detectorModel) + ' = new TGraphErrors(' + str(len(jetEnergyList)) + ',jetEnergy,' + pandoraSettings + '_' + str(detectorModel) + '_JER,jetEnergyError,' + pandoraSettings + '_' + str(detectorModel) + '_JERError);\n'
    saveString += 'pTGraphErrors_' + pandoraSettings + '_' + str(detectorModel) + '->SetLineColor(' + rootLineColor[settingsCounter] + ');\n'
    saveString += 'pTGraphErrors_' + pandoraSettings + '_' + str(detectorModel) + '->SetMarkerColor(' + rootLineColor[settingsCounter] + ');\n'
    saveString += 'pTGraphErrors_' + pandoraSettings + '_' + str(detectorModel) + '->Draw("lp,same");\n'
    settingsCounter = settingsCounter + 1

for pandoraSettings in ['Default','PerfectPFA','TotalConfusion','PhotonConfusion','NeutralHadronConfusion','OtherConfusion']:
    saveString += 'pLegend->AddEntry(pTGraphErrors_' + pandoraSettings + '_' + str(detectorModel) + ', "' + pandoraSettings + '", "lp");\n'

saveString += 'pLegend->SetFillStyle(0);\n'
saveString += 'pLegend->Draw("same");\n'

saveString += 'pCanvasEj->SaveAs("JER_vs_Ej_Detector_Model_' + str(detectorModel) + '_Reco_Var_' + str(recoVar) + '.pdf");\n'
saveString += '}\n'

#===== Write out file =====#
resultsFile = open('JER_vs_Ej_Detector_Model_' + str(detectorModel) + '_Reco_Var_' + str(recoVar) + '.C', 'w')
resultsFile.write(saveString)
resultsFile.close()

detectorModel = 38
recoVar = 69


