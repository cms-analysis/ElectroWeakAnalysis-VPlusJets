from RooWjj2DFitterPars import Wjj2DFitterPars
from ROOT import kRed, kAzure, kGreen, kBlue, kCyan, kViolet, kGray

def theConfig(Nj, mH, isElectron = False, initFile = [], includeSignal = True):
    pars = Wjj2DFitterPars()

    pars.MCDirectory = '/uscms_data/d2/andersj/Wjj/2012/data/Moriond2013/ReducedTrees/'
    # pars.MCDirectory = "root://cmseos:1094//eos/uscms/store/user/lnujj/Moriond2013/RD_includingDiboson/"
    # pars.MCDirectory = "root://cmseos:1094//eos/uscms/store/user/lnujj/HCP2012METfix/ReducedTrees/"
    pars.isElectron = isElectron
    pars.initialParametersFile = initFile

    pars.backgrounds = ['diboson', 'top', 'WpJ']
    pars.includeSignal = includeSignal
    pars.signals = []
    pars.yieldConstraints = {'top' : 0.07, 
                             'WpJ' : 0.05 
                             }
    #pars.yieldConstraints = {}
    #pars.constrainShapes = []
    pars.constrainShapes = ['WpJ']

    pars.Njets = Nj
    pars.mHiggs = 126.

    if isElectron:
        flavorString = 'el'
    else:
        flavorString = 'mu'

    pars.cuts = '(sqrt(JetPFCor_Pt[0]**2+JetPFCor_Pt[1]**2+2*JetPFCor_Pt[0]*JetPFCor_Pt[1]*cos(JetPFCor_Phi[0]-JetPFCor_Phi[1]))>70.)' + \
        '&&(abs(JetPFCor_Eta[0]-JetPFCor_Eta[1])<1.5)' + \
        '&&(abs(JetPFCor_dphiMET[0])>0.4)' + \
        '&&(event_met_pfmet>25)' + \
        '&&(W_mt>30.)'
    # pars.cuts += '&&(JetPFCor_Pt[1]>35.)' + \
    #     '&&(JetPFCor_Pt[0]>40.)' + \
    #     '&&(JetPFCor_Pt[2]<30.)'
    pars.cuts += '&&(JetPFCor_Pt[1]>35.)' + \
        '&&(JetPFCor_Pt[0]>40.)'
    #btag veto
    pars.btagVeto = False
    for i in range(0, 6):
        pars.cuts += '&&((abs(JetPFCor_Eta[%i])>2.4)||' % i + \
            '(JetPFCor_Pt[%i]<30.)||' % i + \
            '(JetPFCor_bDiscriminatorCSV[%i]<0.244))' % i

    # veto boosted topology
    # pars.cuts += '&&(ggdboostedWevt==0)&&(W_pt<200.)'
    pars.cuts += '&&(W_pt<200.)'

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
    pars.dibosonModels = [13]
 
    pars.WpJFiles = [
        (pars.MCDirectory + 'RD_%s_WpJ_CMSSW532.root' % (flavorString),
         18353019+50768992, 36257.2),
         # 18353019, 36257.2),
        (pars.MCDirectory + 'RD_%s_ZpJ_CMSSW532.root' % (flavorString),
         30209426, 3503.71),
        ]
    pars.WpJModels = [17]

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
    pars.topModels = [5]

    pars.dibosonPlotting = {'color' : kAzure+8, 'title' : 'WW+WZ'}
    pars.WpJPlotting = { 'color' : kRed, 'title' : 'V+jets'}
    pars.topPlotting = {'color' : kGreen+2, 'title' : 'top'}
    pars.ggHPlotting = {'color' : kBlue, 'title' : "ggH(%i) #rightarrow WW" % mH}

    pars.var = ['Mass2j_PFCor']
    pars.varRanges = {'Mass2j_PFCor': (12, 50., 146., []),
                      }
    pars.varTitles = {'Mass2j_PFCor': 'm_{jj}',
                      }
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
    # pars.backgrounds.append('multijet')

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

    pars.cuts += '&&(W_electron_pt>30)'
    return pars

def customizeMuons(pars):
    pars.DataFile = pars.MCDirectory + 'RD_WmunuJets_DataAll_GoldenJSON_19p3invfb.root'

    pars.doEffCorrections = True
    pars.effToDo = ['lepton']
    pars.leptonEffFiles = {
        'id': ["EffTable2012/scaleFactor-Run2012ABC-RecoToIso.txt"],
        'HLT': ["EffTable2012/efficiency-Run2012ABC-IsoToIsoMuHLT.txt"]
        }
    pars.lumiPerEpoch = [pars.integratedLumi]

    pars.cuts += '&&(abs(W_muon_eta)<2.1)&&(W_muon_pt>25.)'
    
    return pars
