 /*****************************************************************************
 * Project: CMS detector at the CERN
 *
 * Package: ElectroWeakAnalysis/VPlusJets
 *
 *
 * Authors:
 *
 *   Kalanand Mishra, Fermilab - kalanand@fnal.gov
 *
 * Description:
 *   To fill jet related quantities into a specified TTree
 *   Can work with CaloJet, GenJet, JPT jet, PF jet.
 *   Can work with jets in RECO/AOD/PAT data formats.
 * History:
 *   
 *
 * Copyright (C) 2010 FNAL 
 *****************************************************************************/


// user include files
#include "ElectroWeakAnalysis/VPlusJets/interface/VplusJetsAnalysis.h" 

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/METReco/interface/CaloMET.h"
#include "DataFormats/METReco/interface/CaloMETCollection.h"



ewk::VplusJetsAnalysis::VplusJetsAnalysis(const edm::ParameterSet& iConfig) :
  fOutputFileName ( iConfig.getParameter<std::string>("HistOutFile") ),
  hOutputFile ( new TFile( fOutputFileName.c_str(), "RECREATE" ) ), 
  myTree ( new TTree(iConfig.getParameter<std::string>("TreeName").c_str(),"V+jets Tree") ),
  CaloJetFiller (  new JetTreeFiller("CaloJetFiller", myTree, "Calo", iConfig) ),
  CorrectedCaloJetFiller (  new JetTreeFiller("CorrectedCaloJetFiller", 
					      myTree, "Cor", iConfig) ),
  GenJetFiller ( new JetTreeFiller("GenJetFiller", myTree, "Gen", iConfig) ),
  PFJetFiller (  new JetTreeFiller("PFJetFiller", myTree, "PF", iConfig) ),
  JPTJetFiller ( new JetTreeFiller("JPTJetFiller", myTree, "JPT", iConfig) ),
  recoBosonFiller( new VtoElectronTreeFiller(iConfig.getParameter<std::string>("VBosonType").c_str(), myTree, iConfig) ),
  // recoBosonFiller( new VtoMuonTreeFiller(iConfig.getParameter<std::string>("VBosonType").c_str(), myTree, iConfig) ),
  genBosonFiller( new MCTreeFiller(iConfig.getParameter<std::string>("VBosonType").c_str(), myTree, iConfig) )

{
  // Are we running over Monte Carlo ?
  runningOverMC_=iConfig.getUntrackedParameter< bool >("runningOverMC",true);
  
}



ewk::VplusJetsAnalysis::~VplusJetsAnalysis() {}



void ewk::VplusJetsAnalysis::beginJob()
{
  // Declare all the branches of the tree
  declareTreeBranches();
}



// ------------ method called to produce the data  ------------
void ewk::VplusJetsAnalysis::analyze(const edm::Event& iEvent, 
				const edm::EventSetup& iSetup) {

  // write event information
  run   = 0;
  event = 0;
  lumi  = 0;
  bunch = 0;
  nPV   = 0; 
 
  // run, event, bunch crossing, ....
  run   = iEvent.id().run();
  event = iEvent.id().event();
  lumi  = iEvent.luminosityBlock();
  bunch = iEvent.bunchCrossing();


  // primary/secondary vertices
  edm::Handle<reco::VertexCollection> recVtxs;
  iEvent.getByLabel("offlinePrimaryVertices",recVtxs);
  for(unsigned int ind=0;ind<recVtxs->size();ind++) 
    {
      if(nPV>20) continue;
	mPVx[ind] =   -10000.0;
	mPVy[ind] =   -10000.0;
	mPVz[ind] =   -10000.0;

      if (!((*recVtxs)[ind].isFake())) {
	nPV += 1;
	mPVx[ind] =  (*recVtxs)[ind].x() ;
	mPVy[ind] =  (*recVtxs)[ind].y() ;
	mPVz[ind] =  (*recVtxs)[ind].z() ;
      }
    }



  ////////////// MET //////
  edm::Handle<CaloMETCollection> met;
  iEvent.getByLabel("met",met);
  if (met->size() == 0) {
    mMET   = -1.0;
    mSumET = -1.0;
  }
  else {
    mMET   = (*met)[0].et();
    mSumET = (*met)[0].sumEt();
  }

  edm::Handle<CaloMETCollection> metNoHF;
  iEvent.getByLabel("metNoHF",metNoHF);
  if (metNoHF->size() == 0) {
    mMETnoHF   = -1.0;
    mSumETnoHF = -1.0;
  }
  else {
    mMETnoHF   = (*metNoHF)[0].et();
    mSumETnoHF = (*metNoHF)[0].sumEt();
  }






  // fill jet branches
  CaloJetFiller->fill(iEvent);
  CorrectedCaloJetFiller->fill(iEvent);
  GenJetFiller->fill(iEvent);
  PFJetFiller->fill(iEvent);
  JPTJetFiller->fill(iEvent);


  /**  Store reconstructed vector boson information */
  recoBosonFiller->fill(iEvent);

  /**  Store generated vector boson information */
  if( runningOverMC_ ) genBosonFiller->fill(iEvent);
  
  myTree->Fill();

} // analyze method






void ewk::VplusJetsAnalysis::endJob()
{
  hOutputFile->SetCompressionLevel(2);
  hOutputFile->cd();
  myTree->Write();

  delete myTree;
  hOutputFile->Close();
  delete hOutputFile;
}




//  **** Utility: declare TTree branches for ntuple variables ***
void ewk::VplusJetsAnalysis::declareTreeBranches() {

  myTree->Branch("event_runNo",  &run,   "event_runNo/I");
  myTree->Branch("event_evtNo",  &event, "event_evtNo/I");
  myTree->Branch("event_lumi",   &lumi,  "event_lumi/I"); 
  myTree->Branch("event_bunch",  &bunch, "event_bunch/I"); 
  myTree->Branch("event_nPV",    &nPV,   "event_nPV/I"); 
  myTree->Branch("event_PVx",    mPVx,   "event_PVx[20]/F"); 
  myTree->Branch("event_PVy",    mPVy,   "event_PVy[20]/F"); 
  myTree->Branch("event_PVz",    mPVz,   "event_PVz[20]/F"); 
  myTree->Branch("event_met",    &mMET,  "event_met/F"); 
  myTree->Branch("event_sumet",  &mSumET,"event_sumet/F"); 
  myTree->Branch("event_metnoHF",    &mMETnoHF,  "event_metnoHF/F"); 
  myTree->Branch("event_sumetnoHF",  &mSumETnoHF,"event_sumetnoHF/F"); 
}





// declare this class as a plugin
#include "FWCore/PluginManager/interface/ModuleDef.h"
#include "FWCore/Framework/interface/MakerMacros.h"
using ewk::VplusJetsAnalysis;
DEFINE_FWK_MODULE(VplusJetsAnalysis);