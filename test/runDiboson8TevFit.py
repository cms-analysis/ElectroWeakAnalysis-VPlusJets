from optparse import OptionParser

parser = OptionParser()
parser.add_option('-b', action='store_true', dest='noX', default=False,
                  help='no X11 windows')
parser.add_option('-m', '--mode', default="HWW2DConfig", dest='modeConfig',
                  help='which config to select look at HWW2DConfig.py for ' +\
                      'an example.  Use the file name minus the .py extension.'
                  )
parser.add_option('-H', '--mH', dest='mH', default=350, type='int',
                  help='Higgs Mass Point')
parser.add_option('-j', '--Njets', dest='Nj', default=2, type='int',
                  help='Number of jets.')
parser.add_option('--comp', dest='component', default='diboson',
                  help='name of component to fit')
parser.add_option('--electrons', dest='isElectron', action='store_true',
                  default=False, help='do electrons instead of muons')
parser.add_option('--nosig', dest='includeSignal', action='store_false',
                  default=True, help='include signal shape in fit')
parser.add_option('--toy', dest='toy', action='store_true',
                  help='use pseudo-data instead of data file')
parser.add_option('--toyOut', dest='toyOut', help='filename for toy output')
parser.add_option('--seed', dest='seed', type='int', help='random seed')
parser.add_option('--ws', dest='ws', 
                  help='filename that contains workspace to be used cloned ' +\
                      'for use')
parser.add_option('--debug', dest='debug', action='store_true', default=False,
                  help='turn on extra debugging information')

(opts, args) = parser.parse_args()

import pyroot_logon

#import HWW2DConfig
config = __import__(opts.modeConfig)
import RooWjj2DFitter

from ROOT import TCanvas, TLegend, RooFit, RooLinkedListIter, TMath, RooRandom, TFile, \
    RooDataHist, RooMsgService, TStopwatch
import pulls

timer = TStopwatch()
timer.Start()

if not opts.debug:
    RooMsgService.instance().setGlobalKillBelow(RooFit.WARNING)

if hasattr(opts, "seed") and (opts.seed >= 0):
    print "random seed:", opts.seed
    RooRandom.randomGenerator().SetSeed(opts.seed)
pars = config.theConfig(Nj = opts.Nj, mH = opts.mH, 
                        isElectron = opts.isElectron, initFile = args,
                        includeSignal = opts.includeSignal)

fitter = RooWjj2DFitter.Wjj2DFitter(pars)

totalPdf = fitter.makeFitter()

if opts.ws:
    fitter.loadWorkspaceFromFile(opts.ws, getFloatPars = False)

#fitter.loadData()
fitter.readParametersFromFile()
fitter.expectedFromPars()
# fitter.WpJExpected = 25660.8
# fitter.topExpected = 3357.8
# fitter.dibosonExpected = 670.5
# fitter.HWWExpected = 225.1
fitter.resetYields()
# fitter.readParametersFromFile('WpJHWW350Parameters.txt')
# fitter.readParametersFromFile('topHWW350Parameters.txt')
# fitter.readParametersFromFile('dibosonHWW350Parameters.txt')
# fitter.readParametersFromFile('HWW350Parameters.txt')

startpars = totalPdf.getParameters(fitter.ws.set('obsSet'))
fitter.ws.defineSet("params", startpars)
fitter.ws.saveSnapshot("initPars", startpars)

if opts.toy:
    #generate toy dataset
    print 'Generated parameters'
    fitter.ws.set('params').Print('v')
    fitter.ws.saveSnapshot("genPars", startpars)

    data = totalPdf.generate(fitter.ws.set('obsSet'), RooFit.Name('data_obs'),
                             RooFit.Extended())
    if fitter.pars.binData:
        data = RooDataHist('data_obs', 'data_obs', fitter.ws.set('obsSet'),
                           data)
        data.Print('v')
    getattr(fitter.ws, 'import')(data)
else:    
    data = fitter.loadData()

fitter.setMultijetYield()
data.Print()
startpars.IsA().Destructor(startpars)

print 'Time elapsed: %.1f sec' % timer.RealTime()
print 'CPU time used: %.1f sec' % timer.CpuTime()
print 'starting fitting routine'
timer.Continue()
#fitter.ws.var('top_nrm').setConstant()
fitter.ws.var('r_signal').setVal(1.0)
fitter.ws.var('r_signal').setError(0.04)
fr = None
fr = fitter.fit()

plot1 = fitter.stackedPlot(pars.var[0])
leg1 = RooWjj2DFitter.Wjj2DFitter.legend4Plot(plot1)

c1 = TCanvas('c1', fitter.ws.var(pars.var[0]).GetTitle() + ' plot')
plot1.Draw()
leg1.Draw('same')
c1.Update()

#Make the Data-NonDiboson subtracted plot
print 'plot1 : '
plot1.Print()
xvar = fitter.ws.var(pars.var[0])
xvar.setRange('plotRange', xvar.getMin(), xvar.getMax())
dibosonSubtractedFrame = xvar.frame()
dibosonSubtractedFrame.SetName("%s_subtracted" % pars.var[0])
dibosonResidual = plot1.residHist('theData', pars.backgrounds[1], False, True)#The first background is the diboson
dibosonSubtractedFrame.addPlotable(dibosonResidual, 'p', False, True)
fitter.ws.pdf('diboson').plotOn(dibosonSubtractedFrame)
c2 = TCanvas('c2', fitter.ws.var(pars.var[0]).GetTitle() + ' Subtracted')
dibosonSubtractedFrame.GetYaxis().SetTitle(plot1.GetYaxis().GetTitle())
dibosonSubtractedFrame.Draw()
dibosonSubtractedLegend = TLegend(0.65, 0.72, 0.92, 0.89, '', 'NDC')
dibosonSubtractedLegend.AddEntry('diboson_Norm[Mass2j_PFCor]','Diboson Projection','l')
dibosonSubtractedLegend.AddEntry('resid_theData_top','Data - NonDiboson','p')
dibosonSubtractedLegend.Draw('same')
c2.Update()

ndf = 0

if fr:
    floatVars = [ fr.floatParsFinal().at(i).GetName() \
                      for i in range(0, fr.floatParsFinal().getSize()) ]
    fitter.ws.defineSet('floatingParams', ','.join(floatVars))
    fitter.ws.saveSnapshot("fitPars", ','.join(floatVars))
    ndf = fr.floatParsFinal().getSize() - \
        fitter.ws.set('constraintSet').getSize()
    fr.Print('v')

print '%i free parameters in the fit' % ndf

firstCurve1 = plot1.getObject(1)
# firstCurve1.Print()

(chi2_1, ndf_1) = pulls.computeChi2(plot1.getHist('theData'), firstCurve1)
pull1 = pulls.createPull(plot1.getHist('theData'), firstCurve1)

chi2 = chi2_1
ndf = ndf_1-ndf

cp1 = TCanvas("cp1", fitter.ws.var(pars.var[0]).GetTitle() + ' pull')
pull1.Draw('ap')
pull1.SetName(pars.var[0] + "_pull")
cp1.SetGridy()
cp1.Update()
pull1.GetXaxis().SetLimits(pars.varRanges[pars.var[0]][1], 
                           pars.varRanges[pars.var[0]][2])
pull1.GetXaxis().SetTitle(fitter.ws.var(pars.var[0]).getTitle(True).Data())
pull1.GetYaxis().SetTitle("pull (#sigma)")
cp1.Update()

if opts.toyOut:
    outFile = open(opts.toyOut, 'a', 1)
    fitter.ws.loadSnapshot("genPars")

    line = '%s %.6g %.6g %.6g '
    outFile.write('nll %f covQual %i edm %.4g ' % (fr.minNll(), fr.covQual(),
                                                   fr.edm())
                  )
    outFile.write('chi2Prob %f ' % (TMath.Prob(chi2, ndf)))
    for cycle in range(0, fr.numStatusHistory()):
        outFile.write('%s %i ' % (fr.statusLabelHistory(cycle),
                                  fr.statusCodeHistory(cycle))
                      )
    for i in range(0, fr.floatParsFinal().getSize()):
        outFile.write(line % (fr.floatParsFinal().at(i).GetName(),
                              fr.floatParsFinal().at(i).getVal(),
                              fr.floatParsFinal().at(i).getError(),
                              fitter.ws.var(fr.floatParsFinal().at(i).GetName()).getVal()
                              )
                      )
    outFile.write('\n')
    outFile.close()

mode = 'muon'
if opts.isElectron:
    mode = 'electron'

# WpJ_norm = fitter.ws.factory('WpJ_norm[1.0, -0.5, 5.]')
# if fr:
#     for par in floatVars:
#         # freeze all parameters as a starting point for the combine debugging.
#         #fitter.ws.var(par).setConstant(True)

#         floatVar = fitter.ws.var(par)
#         # if fitter.ws.set('constrainedSet').contains(floatVar):
#         #     floatVar.setVal(1.0)
#         #     floatVar.setConstant(True)
#         #     floatVar.SetName(floatVar.GetName() + '_old')
#         if par == 'WpJ_nrm':
#             WpJ_norm.setVal(floatVar.getVal())
#             WpJ_norm.setError(floatVar.getError())
#             WpJ_norm.setRange(WpJ_norm.getVal()-WpJ_norm.getError()*5.,
#                               WpJ_norm.getVal()+WpJ_norm.getError()*5)
            
#         floatVar.setRange(floatVar.getVal()-floatVar.getError()*5.,
#                           floatVar.getVal()+floatVar.getError()*5)


output = TFile("Dibosonlnujj_%s_%ijets_output.root" % (mode, opts.Nj),
               "recreate")

plot1.Write()
dibosonSubtractedFrame.Write()
pull1.Write()
fitter.ws.SetName("w")
fitter.ws.Write()
#fitter.ws.Print()
output.Close()

c1.SaveAs("Dibosonlnujj_%s_%ijets_Stacked.png" % (mode, opts.Nj))
c2.SaveAs("Dibosonlnujj_%s_%ijets_Subtracted.png" % (mode, opts.Nj))
cp1.SaveAs("Dibosonlnujj_%s_%ijets_Pull.png" % (mode, opts.Nj))
print 'Time elapsed: %.1f sec' % timer.RealTime()
print 'CPU time used: %.1f sec' % timer.CpuTime()

print '%i degrees of freedom' % ndf
print 'chi2: %.2f / %i = %.2f' % (chi2_1, ndf, (chi2/ndf))
print 'chi2 probability: %.4g' % (TMath.Prob(chi2, ndf))
