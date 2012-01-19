#! /usr/bin/env python
import pyroot_logon

def plot2BodyDist(theFitter, pars, chi2, ndf, 
                  Err = -1, NP = False):
    from ROOT import gPad, TLatex, TCanvas, kRed, kCyan, kBlue, \
         RooFit, RooPlot, RooCurve, RooAbsReal, TGraphErrors, NULL

    if pars.includeMuons and pars.includeElectrons:
        modeString = ''
    elif pars.includeMuons:
        modeString = 'Muon'
    elif pars.includeElectrons:
        modeString = 'Electron'
    else:
        modeString = ''

    mf = theFitter.stackedPlot()
    mf.SetName("Mjj_Stacked");
    sf = theFitter.residualPlot(mf, "h_background", "dibosonPdf", False)
    sf.SetName("Mjj_Subtracted");
    pf = theFitter.residualPlot(mf, "h_total", "", True)
    pf.SetName("Mjj_Pull")
    lf = theFitter.stackedPlot(True)
    lf.SetName("Mjj_Stacked_Log");

    if Err > 0:
        totalPdf = theFitter.getWorkSpace().pdf('totalPdf')
        ## Ntotal = totalPdf.expectedEvents(iset)

        ## print 'Ntotal:',Ntotal
        h_dibosonPdf = sf.getCurve('h_dibosonPdf')
        totalPdf.plotOn(sf,
                        RooFit.ProjWData(theFitter.getWorkSpace().data('data')),
                        RooFit.Normalization(Err, RooAbsReal.Raw),
                        #RooFit.AddTo('h_dibosonPdf', 1., 1.),
                        #RooFit.Invisible(),
                        RooFit.Name('h_ErrUp'),
                        RooFit.Range('RangeForPlot'),
                        RooFit.NormRange('RangeForPlot'),
                        RooFit.LineColor(kRed), RooFit.LineStyle(3))
        h_ErrUp = sf.getCurve('h_ErrUp')
        sf.remove('h_ErrUp', False)

        ErrBand = TGraphErrors(h_dibosonPdf.GetN(), h_dibosonPdf.GetX(),
                               h_dibosonPdf.GetY())
        for pt in range(1, ErrBand.GetN()):
            ErrBand.SetPointError(pt, 0, h_ErrUp.GetY()[pt-1])
        ErrBand.SetName("ErrBand")
        ErrBand.SetTitle("Uncertainty")
        ErrBand.SetLineColor(kRed+1)
##         ErrBand.SetLineWidth(0)
##         ErrBand.SetLineStyle(0)
        ErrBand.SetFillColor(kRed+1)
        ErrBand.SetFillStyle(3002)

        #ErrBand.Draw('ap3')
        #h_ErrUp.Draw('lp')
        #gPad.Update()
        #gPad.WaitPrimitive()
##         h_ErrUp.Draw("al")
##         h_ErrUp.GetXaxis().Set(36, 40., 400.)
##         gPad.Update()
##         gPad.WaitPrimitive()
##         h_UpBand = RooCurve("h_UpBand", "Uncertainty", h_dibosonPdf, h_ErrUp,
##                             1., 1.)
##         h_UpBand.SetLineStyle(3)
##         h_UpBand.SetLineColor(kBlue+1)
##         h_DownBand = RooCurve("h_DownBand", "Uncertainty", h_dibosonPdf, h_ErrUp,
##                               1., -1.)
##         h_DownBand.SetLineStyle(3)
##         h_DownBand.SetLineColor(kBlue+1)

##         sf.addPlotable(h_UpBand, "L")
##         sf.addPlotable(h_DownBand, "L")
        sf.addObject(ErrBand, "3")
        #sf.Print("v")
        sf.drawAfter('h_dibosonPdf', 'ErrBand')
        #sf.Print("v")
        sf.drawAfter('ErrBand', 'theData')
        #sf.Print("v")
        sf.findObject('theLegend').AddEntry(ErrBand, 'Uncertainty', 'f')

    if NP:
        NPPdf = theFitter.makeNPPdf();
        NPNorm = 4.*0.11*46.8/12.*pars.intLumi

        if (modeString == 'Electron'):
            if pars.njets == 2:
                NPNorm *= 0.0381
            elif pars.njets == 3:
                NPNorm *= 0.0123
        else:
            if pars.njets == 2:
                NPNorm *= 0.0550
            elif pars.njets == 3:
                NPNorm *= 0.0176

        print '**** N_NP:', NPNorm,'****'

        NPPdf.plotOn(sf, RooFit.ProjWData(theFitter.getWorkSpace().data('data')),
                     RooFit.Normalization(NPNorm, RooAbsReal.Raw),
                     RooFit.AddTo('h_dibosonPdf', 1., 1.),
                     RooFit.Name('h_NP'),
                     RooFit.Range('RangeForPlot'),
                     RooFit.NormRange('RangeForPlot'),
                     RooFit.LineColor(kCyan+2), RooFit.LineStyle(2))

        h_NP = sf.getCurve('h_NP')

        sf.drawBefore('h_dibosonPdf', 'h_NP')
        #sf.Print("v")
        sf.findObject('theLegend').AddEntry(h_NP, "CDF-like Signal", "L")

    l = TLatex()
    l.SetNDC()
    l.SetTextSize(0.035)
    l.SetTextFont(42)

    cstacked = TCanvas("cstacked", "stacked")
    mf.Draw()
    if (chi2 > 0):
        l.DrawLatex(0.55, 0.55,
                    '#chi^{2}/dof = %0.3f/%d = %0.3f' % (chi2, ndf, chi2/ndf)
                    )
    pyroot_logon.cmsPrelim(cstacked, pars.intLumi/1000)
    cstacked.Print('Wjj_Mjj_%s_%ijets_Stacked.pdf' % (modeString, pars.njets))
    cstacked.Print('Wjj_Mjj_%s_%ijets_Stacked.png' % (modeString, pars.njets))
    c2 = TCanvas("c2", "stacked_log")
    c2.SetLogy()
    lf.Draw()
    pyroot_logon.cmsPrelim(c2, pars.intLumi/1000)
    c2.Print('Wjj_Mjj_%s_%ijets_Stacked_log.pdf' % (modeString, pars.njets))
    c2.Print('Wjj_Mjj_%s_%ijets_Stacked_log.png' % (modeString, pars.njets))
    c3 = TCanvas("c3", "subtracted")
    sf.Draw()
    pyroot_logon.cmsPrelim(c3, pars.intLumi/1000)
    c3.Print('Wjj_Mjj_%s_%ijets_Subtracted.pdf' % (modeString, pars.njets))
    c3.Print('Wjj_Mjj_%s_%ijets_Subtracted.png' % (modeString, pars.njets))
    c4 = TCanvas("c4", "pull")
    pf.Draw()
    pyroot_logon.cmsPrelim(c4, pars.intLumi/1000)
    c4.Print('Wjj_Mjj_%s_%ijets_Pull.pdf' % (modeString, pars.njets))
    c4.Print('Wjj_Mjj_%s_%ijets_Pull.png' % (modeString, pars.njets))

    return ([mf,sf,pf,lf],[cstacked,c2,c3,c4])

if __name__ == '__main__':
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option('-b', action='store_true', dest='noX', default=False,
                      help='no X11 windows')
    parser.add_option('-j', '--Njets', dest='Nj', default=2, type='int',
                      help='Number of jets.')
    parser.add_option('--TD', dest='toydataFile', default='',
                      help='a file corresponding to a toy dataset')
    parser.add_option('-i', '--init', dest='startingFile',
                      default='MjjNominal2Jets.txt',
                      help='File to use as the initial template')
    parser.add_option('-d', '--dir', dest='mcdir', default='',
                      help='directory to pick up the W+jets shapes')
    parser.add_option('-m', '--mode', default="MjjOptimizeConfig",
                      dest='modeConfig',
                      help='which config to select look at HWWconfig.py for '+\
                      'an example.  Use the file name minus the .py extension.')
    parser.add_option('--NP', action='store_true', dest='NP', default=False,
                      help='put NP on the plot')
    parser.add_option('--Err', dest='Err', default=-1., type='float',
                      help='error band level')
    (opts, args) = parser.parse_args()

    import pyroot_logon
    config = __import__(opts.modeConfig)

    from ROOT import TFile, Double, Long, gROOT, TCanvas
    ## gROOT.ProcessLine('.L RooWjjFitterParams.h+');
    gROOT.ProcessLine('.L EffTableReader.cc+')
    gROOT.ProcessLine('.L EffTableLoader.cc+')
    gROOT.ProcessLine('.L RooWjjFitterUtils.cc+')
    gROOT.ProcessLine('.L RooWjjMjjFitter.cc+')
    from ROOT import RooWjjMjjFitter, RooFit, \
         RooMsgService, RooArgList, RooArgSet
    from math import sqrt

    RooMsgService.instance().setGlobalKillBelow(RooFit.WARNING)

    fitterPars = config.theConfig(opts.Nj, opts.mcdir, opts.startingFile,
                                  opts.toydataFile )

    theFitter = RooWjjMjjFitter(fitterPars)

    theFitter.makeFitter(False)
    theFitter.loadData()

    theFitter.loadParameters(opts.startingFile)

    (frames, cans) = plot2BodyDist(theFitter, fitterPars,
                                   0, 3, opts.Err, opts.NP)
