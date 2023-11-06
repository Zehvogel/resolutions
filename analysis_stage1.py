ParticleList = ["mu-", "e-"]
#ParticleList = ["mu", "e", "pi"]
#ParticleList = ["mu"]
# ParticleList = ["e-"]
# ThetaList = ["20"]
ThetaList = ["10", "20", "30", "40", "50", "60", "70", "80", "89"]
# ThetaList = ["89"]
# MomentumList = ["1", "2", "5", "10", "20", "50", "100", "200"]
MomentumList = ["1", "2", "5", "10", "20", "50", "100"]

processList = {f"REC_{particle}_{theta}deg_{momentum}GeV_1000evt_edm4hep":{"output":f"{particle}_{theta}deg_{momentum}GeV_1000evt"} for particle in ParticleList for theta in ThetaList for momentum in MomentumList}

# detectorModel = "CLD_o2_v05"
detectorModel = "FCCee_o1_v04"

outputDir = f"Output/stage1/{detectorModel}"

# inputDir = "Output/REC"
# FCCAnalyses automatically rewrites this to access eos via root:
inputDir = f"/eos/experiment/clicdp/grid/ilc/user/L/LReichenbac/resolutions/rec_e4h/{detectorModel}"

#nCPUS = 6
nCPUS = 1

#USER DEFINED CODE
import ROOT
ROOT.gInterpreter.Declare("""
ROOT::VecOps::RVec<int> MCTruthTrackIndex_full(ROOT::VecOps::RVec<int> trackIndex,
                                               ROOT::VecOps::RVec<int> mcIndex,
                                               ROOT::VecOps::RVec<float> weight,
                                               ROOT::VecOps::RVec<edm4hep::MCParticleData> mc)
{
    ROOT::VecOps::RVec<int> res;
    res.resize(mc.size(), -1);
    ROOT::VecOps::RVec<float> trackWeights;
    trackWeights.resize(mc.size(), 0.0);

    for (size_t i = 0; i < trackIndex.size(); i++) {
        float trackWeight = weight[i];
        if (trackWeight > trackWeights[mcIndex[i]]) {
            trackWeights[mcIndex[i]] = trackWeight;
            res[mcIndex[i]] = trackIndex[i];
        }
    }
    return res;
}
""")
#END USER DEFINED CODE

class RDFanalysis():

    def analysers(df):
        df2 = (df
            .Alias("MCTrackAssociations0", "_MCTruthSiTracksLink_sim.index")
            .Alias("MCTrackAssociations1", "_MCTruthSiTracksLink_rec.index")
            .Define("GunParticle_index", "MCParticles.generatorStatus == 1")
            .Define("GunParticle", "MCParticles[GunParticle_index][0]")
            .Define("trackStates_IP", "_SiTracks_Refitted_trackStates[_SiTracks_Refitted_trackStates.location == 1]")
            .Define("MC2TrackIndex", "MCTruthTrackIndex_full(MCTrackAssociations0, MCTrackAssociations1, MCTruthSiTracksLink.weight, MCParticles)")
            .Define("GunParticleTrackIndex", "MC2TrackIndex[GunParticle_index][0]")
            .Define("GunParticleTSIP", "trackStates_IP[GunParticleTrackIndex]")
        )
        return df2

    def output():
        branchList = [
                "GunParticle",
                "GunParticleTSIP"
        ]
        return branchList