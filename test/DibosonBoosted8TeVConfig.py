from RooWjj2DFitterPars import Wjj2DFitterPars
from ROOT import kRed, kAzure, kGreen, kBlue, kCyan, kViolet, kGray

def theConfig(Nj, mH, isElectron = False, initFile = [], includeSignal = True):
    pars = Wjj2DFitterPars()

    pars.MCDirectory = '/uscms_data/d2/andersj/Wjj/2012/data/Moriond2013/ReducedTrees/'
    pars.isElectron = isElectron
    pars.btagSelection = False
    pars.boostedSelection = True
    pars.useTopSideband = False
    pars.initialParametersFile = initFile

    pars.backgrounds = ['diboson', 'top', 'WpJ']
    pars.includeSignal = includeSignal
    pars.signals = []
    if pars.btagSelection:
        pars.yieldConstraints = {'top' : 0.50, 'WpJ' : 0.50 }
    else:
        pars.yieldConstraints = {'top' : 0.07, 'WpJ' : 0.05 }
        pars.constrainShapes = ['WpJ']

    #pars.yieldConstraints = {}

#    pars.yieldConstraints = {'top' : 0.50, 'WpJ' : 0.50 }
#    pars.constrainShapes = []
    #pars.constrainShapes = ['WpJ']

    pars.Njets = Nj
    pars.mHiggs = mH

    if isElectron:
        flavorString = 'el'
    else:
        flavorString = 'mu'


    pars.cuts = \
              '(W_pt>200.)&&(GroomedJet_CA8_pt[0]>200)&&(ggdboostedWevt==1)' +\
              '&&(abs(GroomedJet_CA8_eta[0])<2.4)' +\
              '&&(GroomedJet_CA8_mass_pr[0]>40)' +\
              '&&(GroomedJet_CA8_tau2tau1[0]<0.55)'

    pars.btagVeto = False
    if pars.btagSelection:
        pars.cuts += '&&(JetPFCor_bDiscriminatorCSV[0]>0.244)'
    else:
        pars.cuts += '&&(JetPFCor_bDiscriminatorCSV[0]<0.244)'

    if pars.useTopSideband:
        pars.cuts += '&&(GroomedJet_numberbjets > 1)'
    else:
        pars.cuts += '&&(GroomedJet_numberbjets < 1)'

        

    # for i in range(0, 6):
    #     pars.cuts += '&&((abs(JetPFCor_Eta[%i])>2.4)||' % i + \
    #         '(JetPFCor_Pt[%i]<30.)||' % i + \
    #         '(JetPFCor_bDiscriminatorCSV[%i]<0.679))' % i

    # veto boosted topology
    # if mH >= 600:
    #     pars.cuts += '&&(W_pt<200.)'

    # veto vbf
    pars.cuts += '&&(vbf_event==0)'

    # you need a files entry and a models entry for each of the fit 
    # compoents in backgrounds and signals
    # the files should a list with entries like (filename, Ngen, xsec)

    pars.dibosonFiles = [
        (pars.MCDirectory + 'RD_%s_WW_CMSSW532.root' % (flavorString),
         9450414, 57.1097),
        (pars.MCDirectory + 'RD_%s_WZ_CMSSW532.root' % (flavorString),
         10000267, 32.3161),
        ]
    pars.dibosonFracOfData = -1
    #pars.dibosonModels = [5]
    pars.dibosonModels = [22]



    pars.WpJFiles = [
        (pars.MCDirectory + 'RD_%s_WJets_madgraph_CMSSW532.root' % (flavorString),
         8955318, 1.3*228.9),
        ]
    if pars.btagSelection:
        pars.WpJFracOfData = 0.332
    else:
        if isElectron:
            pars.WpJFracOfData = 0.71
        else:
            pars.WpJFracOfData = 0.72

    pars.WpJModels = [8]

    pars.topFiles = [
        (pars.MCDirectory + 'RD_%s_TTbar_CMSSW532.root' % (flavorString),
         6893735, 225.197),
        (pars.MCDirectory + 'RD_%s_STopS_Tbar_CMSSW532.root' % (flavorString),
         139974, 1.75776),
        (pars.MCDirectory + 'RD_%s_STopS_T_CMSSW532.root' % (flavorString),
         259960, 3.89394),
        (pars.MCDirectory + 'RD_%s_STopT_Tbar_CMSSW532.root' % (flavorString),
         1935066, 30.0042),
        (pars.MCDirectory + 'RD_%s_STopT_T_CMSSW532.root' % (flavorString),
         3758221, 55.531),
        (pars.MCDirectory + 'RD_%s_STopTW_Tbar_CMSSW532.root' % (flavorString),
         493458, 11.1773),
        (pars.MCDirectory + 'RD_%s_STopTW_T_CMSSW532.root' % (flavorString),
         497657, 11.1773),
        ]
    
    if pars.btagSelection:
        pars.topFracOfData = 0.616
##         if isElectron:
##             pars.topModels = [5]
##         else:
##             pars.topModels = [13]
    else:  
        pars.topFracOfData = 0.22


    pars.topModels = [5]


    pars.dibosonPlotting = {'color' : kAzure+8, 'title' : 'WW+WZ'}
    pars.WpJPlotting = { 'color' : kRed, 'title' : 'V+jets'}
    pars.topPlotting = {'color' : kGreen+2, 'title' : 'top'}
    pars.ggHPlotting = {'color' : kBlue, 'title' : "ggH(%i) #rightarrow WW" % mH}

    pars.var = ['GroomedJet_CA8_mass_pr[0]']
    pars.varRanges = {'GroomedJet_CA8_mass_pr[0]': (20, 40., 140., []),}
    pars.varTitles = {'GroomedJet_CA8_mass_pr[0]': 'm_{J}',
                      }
    pars.varNames = {'GroomedJet_CA8_mass_pr[0]': 'GroomedJet_CA8_mass_pr' }

    
    pars.exclude = {}
    pars.blind = False
    # pars.v1binEdges = [50, 55.,60.,65.,70.,75.,80.,85.,95.,
    #                    105.,115.,125.,135.,150.,165.,180.,200.]
    # pars.v1nbins = len(pars.v1binEdges)-1

    pars.integratedLumi = 19300.

    pars.binData = False
    # pars.binData = True

    return customizeElectrons(pars) if isElectron else \
        customizeMuons(pars)

def customizeElectrons(pars):
    pars.DataFile = pars.MCDirectory + 'RD_WenuJets_DataAllSingleElectronTrigger_GoldenJSON_19p2invfb.root'
    if pars.useTopSideband:
        pars.topFiles = [(pars.DataFile,1,1),]
    
    #pars.backgrounds.append('multijet')

    # pars.multijetFraction = 0.0637
    # pars.multijetFiles = [
    #     (pars.MCDirectory + 'RDQCD_WenuJets_Isog0p3NoElMVA_11p9invfb.root',
    #      1, pars.multijetFraction/pars.integratedLumi)
    #     ]
    # pars.multijetModels = (11, 1)
    # pars.yieldConstraints['multijet'] = 0.2
    # pars.multijetPlotting = {'color' : kGray+1, 'title' : 'multijet'}

    # pars.multijet_cuts = '(ggdevt==%i)&&(fit_status==0)&&(W_mt>30)' % pars.Njets
    # pars.multijet_cuts += '&&(abs(JetPFCor_dphiMET[0])>0.8)' + \
    #     '&&(W_electron_pt>35)' + \
    #     '&&(W_electron_pfIsoEA>0.3)'

    pars.doEffCorrections = True
    pars.effToDo = ['lepton']
    pars.leptonEffFiles = {
        'id': ["EffTable2012/scaleFactor-Run2012ABC-GsfElectronToId.txt"],
        'reco': ["EffTable2012/scaleFactor-Run2012ABC-SCToElectron.txt"],
        'HLT': ["EffTable2012/efficiency-Run2012ABC-WP80ToHLTEle.txt"]
        }
    pars.lumiPerEpoch = [pars.integratedLumi]

##     pars.cuts += '&&(W_electron_pt>30)'
    pars.cuts += '&&(event_met_pfmet >70)&&(W_electron_pt>35)'
    return pars

def customizeMuons(pars):
    pars.DataFile = pars.MCDirectory + 'RD_WmunuJets_DataAll_GoldenJSON_19p3invfb.root'
    if pars.useTopSideband:
        pars.topFiles = [(pars.DataFile,1,1),]
    
    pars.doEffCorrections = True
    pars.effToDo = ['lepton']
    pars.leptonEffFiles = {
        'id': ["EffTable2012/scaleFactor-Run2012ABC-RecoToIso.txt"],
        'HLT': ["EffTable2012/efficiency-Run2012ABC-IsoToIsoMuHLT.txt"]
        }
    pars.lumiPerEpoch = [pars.integratedLumi]

    pars.cuts += '&&(event_met_pfmet >50)&&(abs(W_muon_eta)<2.1)&&(W_muon_pt>30.)'
    
    return pars
