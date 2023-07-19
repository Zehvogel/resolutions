#ParticleList = ["mu", "e"]
#ParticleList = ["mu", "e", "pi"]
#ParticleList = ["mu"]
ParticleList = ["e"]
ThetaList = ["10", "20", "30", "40", "50", "60", "70", "80", "89"]
#ThetaList = ["89"]
MomentumList = ["1", "2", "5", "10", "20", "50", "100", "200"]

processList = {f"REC_{particle}_{theta}deg_{momentum}GeV_1000evt_edm4hep":{"output":f"{particle}_{theta}deg_{momentum}GeV_1000evt"} for particle in ParticleList for theta in ThetaList for momentum in MomentumList}
#print(processList)
outputDir = "Output/stage1"

inputDir = "Output/REC"

#nCPUS = 6
nCPUS = 1

#USER DEFINED CODE
import ROOT
ROOT.gInterpreter.Declare("""
ROOT::VecOps::RVec<int> MCTruthTrackIndex(ROOT::VecOps::RVec<int> trackIndex,
                                          ROOT::VecOps::RVec<int> mcIndex,
                                          ROOT::VecOps::RVec<edm4hep::MCParticleData> mc)
{
    ROOT::VecOps::RVec<int> res;
    res.resize(mc.size(), -1);

    for (size_t i = 0; i < trackIndex.size(); i++) {
        res[mcIndex[i]] = trackIndex[i];
    }
    return res;
}
""")
#END USER DEFINED CODE

class RDFanalysis():

    def analysers(df):
        df2 = (df
            .Alias("MCTrackAssociations0", "MCTruthSiTracksLink#0.index")
            .Alias("MCTrackAssociations1", "MCTruthSiTracksLink#1.index")
            .Define("GunParticle_index", "MCParticles.generatorStatus == 1")
            .Define("GunParticle", "MCParticles[GunParticle_index][0]")
            .Define("trackStates_IP", "SiTracks_Refitted_1[SiTracks_Refitted_1.location == 1]")
            .Define("MC2TrackIndex", "MCTruthTrackIndex(MCTrackAssociations0, MCTrackAssociations1, MCParticles)")
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