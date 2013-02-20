from RooWjj2DFitterPars import Wjj2DFitterPars
from ROOT import kRed, kAzure, kGreen, kBlue, kCyan, kViolet, kGray, kYellow

def theConfig(Nj, mH, isElectron = False, initFile = [], includeSignal = True):
    pars = Wjj2DFitterPars()

    pars.MCDirectory = '/uscms_data/d2/andersj/Wjj/2012/data/Moriond2013/ReducedTrees/'
    pars.QCDDirectory = "/uscms_data/d3/ilyao/QCD8TeV/Moriond13/"
    # pars.MCDirectory = "root://cmseos:1094//eos/uscms/store/user/lnujj/HCP2012METfix/ReducedTrees/"
    pars.isElectron = isElectron
    pars.btagSelection = False
    pars.boostedSelection = False
    pars.initialParametersFile = initFile

    pars.Njets = Nj
    pars.mHiggs = 126.

    if isElectron:
        flavorString = 'el'
    else:
        flavorString = 'mu'

    pars.cuts = '(sqrt(JetPFCor_Pt[0]**2+JetPFCor_Pt[1]**2+2*JetPFCor_Pt[0]*JetPFCor_Pt[1]*cos(JetPFCor_Phi[0]-JetPFCor_Phi[1]))>70.)' + \
        '&&(abs(JetPFCor_Eta[0]-JetPFCor_Eta[1])<1.5)' + \
        '&&(abs(JetPFCor_dphiMET[0])>0.4)' + \
        '&&(W_mt>30.)'
    # pars.cuts += '&&(JetPFCor_Pt[1]>35.)' + \
    #     '&&(JetPFCor_Pt[0]>40.)' + \
    #     '&&(JetPFCor_Pt[2]<30.)'
    pars.cuts += '&&(JetPFCor_Pt[1]>35.)' + \
        '&&(JetPFCor_Pt[0]>40.)'



    #implement btagged or anti-btagged cuts
    startRange = 0
    if pars.btagSelection:
        startRange = 2
        for i in range(0, startRange):
            pars.cuts += '&&(JetPFCor_bDiscriminatorCSV[%i]>0.244)' % i
    pars.btagVeto = False
    for i in range(startRange, 6):
        pars.cuts += '&&((abs(JetPFCor_Eta[%i])>2.4)||' % i + \
                     '(JetPFCor_Pt[%i]<30.)||' % i + \
                     '(JetPFCor_bDiscriminatorCSV[%i]<0.244))' % i    

    # veto boosted topology
    # pars.cuts += '&&(ggdboostedWevt==0)&&(W_pt<200.)'
    pars.cuts += '&&(W_pt<200.)'

    # veto vbf
    pars.cuts += '&&(vbf_event==0)'

    pars.backgrounds = ['diboson', 'top', 'WpJ', 'ZpJ']
    pars.yieldConstraints = {'top' : 0.07, 'ZpJ' : 0.05, 'WpJ' : 0.05}
    pars.constrainShapes = ['WpJ']
    #pars.constrainShapes = []
    if pars.btagSelection:
        pars.backgrounds = ['diboson', 'top', 'WpJ']
        pars.yieldConstraints = {'top' : 0.5, 'WpJ' : 0.5 }
        pars.constrainShapes = []

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
    pars.dibosonModels = [22]
 
    pars.WpJFiles = [
        # (pars.MCDirectory + 'RD_%s_WpJ_CMSSW532.root' % (flavorString),
        #  18353019+50768992, 36257.2),
        # (pars.MCDirectory + 'RD_%s_W1Jets_CMSSW532.root' % (flavorString),
        #  19871598, 5400.0*1.2),
        (pars.MCDirectory + 'RD_%s_W2Jets_CMSSW532.root' % (flavorString),
         33004921, 1750.0*1.2),
        (pars.MCDirectory + 'RD_%s_W3Jets_CMSSW532.root' % (flavorString),
         15059503, 519.0*1.2),
        (pars.MCDirectory + 'RD_%s_W4Jets_CMSSW532.root' % (flavorString),
         12842803, 214.0*1.2),
        ]
    pars.WpJFracOfData = -1

    pars.ZpJFiles = [
        (pars.MCDirectory + 'RD_%s_ZpJ_CMSSW532.root' % (flavorString),
         30209426, 3503.71),
        ]
    pars.ZpJFracOfData = -1
    pars.ZpJModels = [23]
    pars.ZpJAuxModels = [4]


    # To implement Template Morphing set pars.WpJModels=[-2]
    # and be sure to edit the WpJ*InputParameters.txt file so that the
    # naming scheme corresponds to the correct components/subcomponents.
    # E.g. the parameters from the shape fit to WpJ default MC should
    # contain the suffix Nom, while the overall yield shouldn't, and the
    # lines
    # fMU_WpJ = 0.0 +/- 100.0 L(-1 - 1)
    # fSU_WpJ = 0.0 +/- 100.0 L(-1 - 1)
    # should be added to the .txt file

    # pars.WpJModels = [-2]

    if pars.btagSelection:
        pars.WpJModels = [17]
    else:
        #pars.WpJModels = [17]
        #pars.WpJModels = [-2]
        pars.WpJModels = [23]
        pars.WpJAuxModels = [5]
    
    pars.WpJNomFiles = pars.WpJFiles
    pars.WpJNomModels = [-1]
    pars.WpJMUFiles = [ (pars.MCDirectory + 'RD_%s_WpJmatchingup_CMSSW532.root' % (flavorString), 20976007, 36257.2), ]
    pars.WpJMUModels = [-1]
    pars.WpJMDFiles = [ (pars.MCDirectory + 'RD_%s_WpJmatchingdown_CMSSW532.root' % (flavorString), 21364575, 36257.2), ]
    pars.WpJMDModels = [-1]
    pars.WpJSUFiles = [ (pars.MCDirectory + 'RD_%s_WpJscaleup_CMSSW532.root' % (flavorString), 20784694, 36257.2), ]
    pars.WpJSUModels = [-1]
    pars.WpJSDFiles = [ (pars.MCDirectory + 'RD_%s_WpJscaledown_CMSSW532.root' % (flavorString), 20760830, 36257.2), ]
    pars.WpJSDModels = [-1]

    
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
    pars.topFracOfData = -1
    if pars.btagSelection:
        pars.topModels = [4] #btag selection
    else:
        pars.topModels = [13] #anti-btag selection

    
    pars.dibosonPlotting = {'color' : kAzure+8, 'title' : 'WW+WZ'}
    pars.WpJPlotting = { 'color' : kRed, 'title' : 'W+jets'}
    pars.ZpJPlotting = { 'color' : kYellow, 'title' : 'Z+jets'}
    pars.topPlotting = {'color' : kGreen+2, 'title' : 'top'}
    pars.QCDPlotting = {'color' : kGray, 'title' : 'multijet'}

    pars.var = ['Mass2j_PFCor']
    pars.varRanges = {'Mass2j_PFCor': (14, 48., 160., []),
                      }
    pars.varTitles = {'Mass2j_PFCor': 'm_{jj}',
                      }
    pars.varNames = {'Mass2j_PFCor': 'Mass2j_PFCor' }
    
    pars.exclude = {}
    pars.blind = False
    # pars.v1binEdges = [50, 55.,60.,65.,70.,75.,80.,85.,95.,
    #                    105.,115.,125.,135.,150.,165.,180.,200.]
    # pars.v1nbins = len(pars.v1binEdges)-1

    pars.integratedLumi = 19300.

    # pars.binData = False
    pars.binData = False

    #Standard vs QCD cuts:
    pars.QCDcuts = pars.cuts
    pars.cuts += '&&(event_met_pfmet>25)'
    pars.QCDcuts += '&&(event_met_pfmet>20)'


    pars.includeSignal = includeSignal
    pars.signals = []

    return customizeElectrons(pars) if isElectron else \
        customizeMuons(pars)

    
        
def customizeElectrons(pars):
    
    pars.DataFile = pars.MCDirectory + 'RD_WenuJets_DataAllSingleElectronTrigger_GoldenJSON_19p2invfb.root'
    
    pars.backgrounds.append('QCD')

    pars.QCDFracOfData = 0.1
    pars.QCDFiles = [
        (pars.QCDDirectory + 'RDQCD_WenuJets_Isog0p3NoElMVA_19p2invfb.root',
         1,1), #The events come from the data sideband
        ]
    pars.QCDModels = [-1]
    pars.yieldConstraints['QCD'] = 0.5

    pars.doEffCorrections = True
    pars.effToDo = ['lepton']
    pars.leptonEffFiles = {
        'id': ["EffTable2012/scaleFactor-Run2012ABC-GsfElectronToId.txt"],
        'reco': ["EffTable2012/scaleFactor-Run2012ABC-SCToElectron.txt"],
        'HLT': ["EffTable2012/efficiency-Run2012ABC-WP80ToHLTEle.txt"]
        }
    pars.lumiPerEpoch = [pars.integratedLumi]

    pars.integratedLumi = 19200.
    pars.QCDcuts += '&&(W_electron_pt>30)'
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

    pars.QCDcuts += '&&(abs(W_muon_eta)<2.1)&&(W_muon_pt>25.)'
    pars.cuts += '&&(abs(W_muon_eta)<2.1)&&(W_muon_pt>25.)'
    
    return pars
