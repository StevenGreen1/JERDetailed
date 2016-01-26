#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import re
import math

thisFile = sys.argv[0]

from collections import defaultdict
JER = defaultdict(dict)
JERError = defaultdict(dict)

pandoraSettings = ''
pandoraSettingsList = ['Default','PerfectPhoton','PerfectPhotonNK0L','PerfectPFA']
jetEnergyList = [30, 40, 50, 60, 70, 80, 91, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 220, 240, 260, 280, 300, 350, 400, 450, 500]
detectorModelList = [38]
recoVarList = range(69,77)

#===== What To Plot =====#

NameOfPlot = 'LCWS_Plot'

ToPlot = [
             ['Default', 38, 69, 2, 1],
#             ['Default', 38, 70],
             ['Default', 38, 71, 10003, 1],
#             ['Default', 38, 72],
             ['Default', 38, 73, 10004, 1],
#             ['Default', 38, 74],
#             ['Default', 38, 75],
             ['Default', 38, 76, 1, 1]
#             ['PerfectPFA', 38, 69],
#             ['PerfectPFA', 38, 70],
#             ['PerfectPFA', 38, 71],
#             ['PerfectPFA', 38, 72],
#             ['PerfectPFA', 38, 73],
#             ['PerfectPFA', 38, 74],
#             ['PerfectPFA', 38, 75],
#             ['PerfectPFA', 38, 76],
#             ['TotalConfusion', 38, 69],
#             ['TotalConfusion', 38, 70],
#             ['TotalConfusion', 38, 71],
#             ['TotalConfusion', 38, 72],
#             ['TotalConfusion', 38, 73],
#             ['TotalConfusion', 38, 74],
#             ['TotalConfusion', 38, 75],
#             ['TotalConfusion', 38, 76],
#             ['PhotonConfusion', 38, 69],
#             ['PhotonConfusion', 38, 70],
#             ['PhotonConfusion', 38, 71],
#             ['PhotonConfusion', 38, 72],
#             ['PhotonConfusion', 38, 73],
#             ['PhotonConfusion', 38, 74],
#             ['PhotonConfusion', 38, 75],
#             ['PhotonConfusion', 38, 76],
#             ['NeutralHadronConfusion', 38, 69],
#             ['NeutralHadronConfusion', 38, 70],
#             ['NeutralHadronConfusion', 38, 71],
#             ['NeutralHadronConfusion', 38, 72],
#             ['NeutralHadronConfusion', 38, 73],
#             ['NeutralHadronConfusion', 38, 74],
#             ['NeutralHadronConfusion', 38, 75],
#             ['NeutralHadronConfusion', 38, 76],
#             ['OtherConfusion', 38, 69],
#             ['OtherConfusion', 38, 70],
#             ['OtherConfusion', 38, 71],
#             ['OtherConfusion', 38, 72],
#             ['OtherConfusion', 38, 73],
#             ['OtherConfusion', 38, 74],
#             ['OtherConfusion', 38, 75],
#             ['OtherConfusion', 38, 76]
         ]

#===== Read data =====#

for detectorModel in detectorModelList:
    for recoVar in recoVarList:
        inputFileName = 'Detector_Model_' + str(detectorModel) + '_Reco_Var_' + str(recoVar) + '_Results.txt'
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
                JER[(pandoraSettings,energy,detectorModel,recoVar)] = float(r.group(3))
                JERError[(pandoraSettings,energy,detectorModel,recoVar)] = float(r.group(4))

#===== Calculate Confusion Terms =====#

for recoVar in recoVarList:
    # Total Confusion
    for energy in jetEnergyList:    
        JER[('TotalConfusion',energy,detectorModel,recoVar)] = math.sqrt( math.fabs( (JER[('Default',energy,detectorModel,recoVar)] * JER[('Default',energy,detectorModel,recoVar)]) - (JER[('PerfectPFA',energy,detectorModel,recoVar)] * JER[('PerfectPFA',energy,detectorModel,recoVar)]) ) )
        JERError[('TotalConfusion',energy,detectorModel,recoVar)] = math.sqrt( math.fabs( ( (JERError[('Default',energy,detectorModel,recoVar)] * JERError[('Default',energy,detectorModel,recoVar)] * JER[('Default',energy,detectorModel,recoVar)] * JER[('Default',energy,detectorModel,recoVar)]) / (JER[('TotalConfusion',energy,detectorModel,recoVar)] * JER[('TotalConfusion',energy,detectorModel,recoVar)]) ) - ( (JERError[('PerfectPFA',energy,detectorModel,recoVar)] * JERError[('PerfectPFA',energy,detectorModel,recoVar)] * JER[('PerfectPFA',energy,detectorModel,recoVar)] * JER[('PerfectPFA',energy,detectorModel,recoVar)]) / (JER[('TotalConfusion',energy,detectorModel,recoVar)] * JER[('TotalConfusion',energy,detectorModel,recoVar)]) ) ) )

    # Photon Confusion
    for energy in jetEnergyList:    
        JER[('PhotonConfusion',energy,detectorModel,recoVar)] = math.sqrt( math.fabs( (JER[('Default',energy,detectorModel,recoVar)] * JER[('Default',energy,detectorModel,recoVar)]) - (JER[('PerfectPhoton',energy,detectorModel,recoVar)] * JER[('PerfectPhoton',energy,detectorModel,recoVar)]) ) )
        JERError[('PhotonConfusion',energy,detectorModel,recoVar)] = math.sqrt( math.fabs( ( (JERError[('Default',energy,detectorModel,recoVar)] * JERError[('Default',energy,detectorModel,recoVar)] * JER[('Default',energy,detectorModel,recoVar)] * JER[('Default',energy,detectorModel,recoVar)]) / (JER[('PhotonConfusion',energy,detectorModel,recoVar)] * JER[('PhotonConfusion',energy,detectorModel,recoVar)]) ) - ( (JERError[('PerfectPhoton',energy,detectorModel,recoVar)] * JERError[('PerfectPhoton',energy,detectorModel,recoVar)] * JER[('PerfectPhoton',energy,detectorModel,recoVar)] * JER[('PerfectPhoton',energy,detectorModel,recoVar)]) / (JER[('PhotonConfusion',energy,detectorModel,recoVar)] * JER[('PhotonConfusion',energy,detectorModel,recoVar)]) ) ) )

    # Neutral Hadron Confusion
    for energy in jetEnergyList:
        JER[('NeutralHadronConfusion',energy,detectorModel,recoVar)] = math.sqrt( math.fabs( (JER[('PerfectPhoton',energy,detectorModel,recoVar)] * JER[('PerfectPhoton',energy,detectorModel,recoVar)]) - (JER[('PerfectPhotonNK0L',energy,detectorModel,recoVar)] * JER[('PerfectPhotonNK0L',energy,detectorModel,recoVar)]) ) )    
        JERError[('NeutralHadronConfusion',energy,detectorModel,recoVar)] = math.sqrt( math.fabs( ( (JERError[('PerfectPhoton',energy,detectorModel,recoVar)] * JERError[('PerfectPhoton',energy,detectorModel,recoVar)] * JER[('PerfectPhoton',energy,detectorModel,recoVar)] * JER[('PerfectPhoton',energy,detectorModel,recoVar)]) / (JER[('NeutralHadronConfusion',energy,detectorModel,recoVar)] * JER[('NeutralHadronConfusion',energy,detectorModel,recoVar)]) ) - ( (JERError[('PerfectPhotonNK0L',energy,detectorModel,recoVar)] * JERError[('PerfectPhotonNK0L',energy,detectorModel,recoVar)] * JER[('PerfectPhotonNK0L',energy,detectorModel,recoVar)] * JER[('PerfectPhotonNK0L',energy,detectorModel,recoVar)]) / (JER[('NeutralHadronConfusion',energy,detectorModel,recoVar)] * JER[('NeutralHadronConfusion',energy,detectorModel,recoVar)]) ) ) )

    # Other Confusion
    for energy in jetEnergyList:
        JER[('OtherConfusion',energy,detectorModel,recoVar)] = math.sqrt( math.fabs( (JER[('PerfectPhotonNK0L',energy,detectorModel,recoVar)] * JER[('PerfectPhotonNK0L',energy,detectorModel,recoVar)]) - (JER[('PerfectPFA',energy,detectorModel,recoVar)] * JER[('PerfectPFA',energy,detectorModel,recoVar)]) ) )    
        JERError[('OtherConfusion',energy,detectorModel,recoVar)] = math.sqrt( math.fabs( ( (JERError[('PerfectPhotonNK0L',energy,detectorModel,recoVar)] * JERError[('PerfectPhotonNK0L',energy,detectorModel,recoVar)] * JER[('PerfectPhotonNK0L',energy,detectorModel,recoVar)] * JER[('PerfectPhotonNK0L',energy,detectorModel,recoVar)]) / (JER[('OtherConfusion',energy,detectorModel,recoVar)] * JER[('OtherConfusion',energy,detectorModel,recoVar)]) ) - ( (JERError[('PerfectPFA',energy,detectorModel,recoVar)] * JERError[('PerfectPFA',energy,detectorModel,recoVar)] * JER[('PerfectPFA',energy,detectorModel,recoVar)] * JER[('PerfectPFA',energy,detectorModel,recoVar)]) / (JER[('OtherConfusion',energy,detectorModel,recoVar)] * JER[('OtherConfusion',energy,detectorModel,recoVar)]) ) ) )

#for x in JER.keys():print x,' : ',JER[x]
#for x in JERError.keys():print x,' : ',JERError[x]

#==== Tools ====#

def rootLineColor(pandora):
    colourDict = defaultdict(dict)
    colourDict = {'Default':'kBlack', 'PerfectPFA':'kBlue', 'TotalConfusion':'kRed', 'PhotonConfusion':'kOrange', 'NeutralHadronConfusion':'8', 'OtherConfusion':'kMagenta'}
    # Neutral had is green 
    return colourDict[(pandora)]

#rootLineStyle = ['1','2','3','4','5','6']

def rootMarkerStyle(recoVar):
    markerDict = defaultdict(dict)
    markerDict = {69:22, 70:21, 71:20, 72:23, 73:26, 74:28, 75:25, 76:24}
    return markerDict[(recoVar)]

def truncationFromRecoVar(recoVar):
    truncDict = defaultdict(dict)
    truncDict = {69:0.5, 70:0.75, 71:1, 72:1.5, 73:2, 74:5, 75:10, 76:1000000}
    return truncDict[(recoVar)]

#==== Make JER_vs_Ej =====#

saveString = '{\n'
saveString += 'gStyle->SetOptStat(0);\n'
saveString += 'TCanvas *pCanvasEj = new TCanvas();\n'
saveString += 'pCanvasEj->cd();\n'

saveString += 'TH2F *pAxesEj = new TH2F("axesEj","",1200,0,300,12000,2,5);\n'
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

saveString += 'TLegend *pLegend = new TLegend(0.6, 0.6, 0.9, 0.9);\n'

for item in ToPlot:
    pandoraToPlot = item[0]
    detectorModelToPlot = item[1]
    recoVarToPlot = item[2]
    colour = item[3]
    style = item[4]

    saveString += 'float ' + pandoraToPlot + '_' + str(detectorModelToPlot) + '_' + str(recoVarToPlot) + '_JER[' + str(len(jetEnergyList)) + '] = {'
    for energy in jetEnergyList:
        saveString += str(JER[(pandoraToPlot,energy,detectorModelToPlot,recoVarToPlot)])
        if energy is not jetEnergyList[-1]:
            saveString += ','
    saveString += '};\n'

    saveString += 'float ' + pandoraToPlot + '_' + str(detectorModelToPlot) + '_' + str(recoVarToPlot) + '_JERError[' + str(len(jetEnergyList)) + '] = {'
    for energy in jetEnergyList:
        saveString += str(JERError[(pandoraToPlot,energy,detectorModelToPlot,recoVarToPlot)])
        if energy is not jetEnergyList[-1]:
            saveString += ','
    saveString += '};\n'

    saveString += 'TGraphErrors *pTGraphErrors_' + pandoraToPlot + '_' + str(detectorModelToPlot) + '_' + str(recoVarToPlot) + ' = new TGraphErrors(' + str(len(jetEnergyList)) + ',jetEnergy,' + pandoraToPlot + '_' + str(detectorModelToPlot) + '_' + str(recoVarToPlot) + '_JER,jetEnergyError,' + pandoraToPlot + '_' + str(detectorModelToPlot) + '_' + str(recoVarToPlot) + '_JERError);\n'
    saveString += 'pTGraphErrors_' + pandoraToPlot + '_' + str(detectorModelToPlot) + '_' + str(recoVarToPlot) + '->SetLineColor(' + str(colour) + ');\n'
    saveString += 'pTGraphErrors_' + pandoraToPlot + '_' + str(detectorModelToPlot) + '_' + str(recoVarToPlot) + '->SetMarkerColor(' + str(colour) + ');\n'
    saveString += 'pTGraphErrors_' + pandoraToPlot + '_' + str(detectorModelToPlot) + '_' + str(recoVarToPlot) + '->SetMarkerStyle(' + str(style) + ');\n'
    saveString += 'pTGraphErrors_' + pandoraToPlot + '_' + str(detectorModelToPlot) + '_' + str(recoVarToPlot) + '->Draw("lp,same");\n'
    legendDescription = '#splitline{Timing Cut in ECal and HCal 100 ns,}{Hadronic Energy Truncation ' + str(truncationFromRecoVar(recoVarToPlot)) + ' GeV}'
    saveString += 'pLegend->AddEntry(pTGraphErrors_' + pandoraToPlot + '_' + str(detectorModelToPlot) + '_' + str(recoVarToPlot) + ', "' + legendDescription + '", "l");\n'

saveString += 'pLegend->SetFillStyle(0);\n'
saveString += 'pLegend->Draw("same");\n'

fileName  = 'JER_vs_Ej_' + NameOfPlot + '.pdf'
if os.path.isfile(fileName): 
    print 'File ' + fileName + ' already exists!'
    sys.exit()

saveString += 'pCanvasEj->SaveAs("' + fileName + '");\n'
saveString += '}\n'

#===== Write out file =====#

fileName  = 'JER_vs_Ej_' + NameOfPlot + '.C'
if os.path.isfile(fileName):
    print 'File ' + fileName + ' already exists!'
    sys.exit()

resultsFile = open('JER_vs_Ej_' + NameOfPlot + '.C', 'w')
resultsFile.write(saveString)
resultsFile.close()

