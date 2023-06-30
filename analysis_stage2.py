#ParticleList = ["mu", "e", "pi"]
ParticleList = ["mu"]
#ThetaList = ["10", "20", "30", "40", "50", "60", "70", "80", "89"]
ThetaList = ["10"]
MomentumList = ["1", "2", "5", "10", "20", "50", "100", "200"]

processList = {f"{particle}_{theta}deg_{momentum}GeV_1000evt":{} for particle in ParticleList for theta in ThetaList for momentum in MomentumList}
#print(processList)
outputDir = "Output/stage2"

inputDir = "Output/stage1"

nCPUS = 1

#USER DEFINED CODE
import ROOT
ROOT.gSystem.Load("/cvmfs/sw-nightlies.hsf.org/key4hep/releases/2023-05-30/x86_64-almalinux9-gcc11.3.1-opt/marlinutil/4bba4d10fc1c448213e83251f689370fc2d43c9e=develop-zhkc6e/lib/libMarlinUtil.so")
ROOT.gROOT.ProcessLine(".include /cvmfs/sw-nightlies.hsf.org/key4hep/releases/2023-05-30/x86_64-almalinux9-gcc11.3.1-opt/ced/56f3bc90862e7bd4fa5657e638cceea50b368ed7=develop-lhxqn2/include")
ROOT.gInterpreter.Declare("#include <marlinutil/HelixClass_double.h>")
#END USER DEFINED CODE

class RDFanalysis():

    def analysers(df):
        df2 = (df
               .Define("GunParticleTSIPHelix", "auto h = HelixClass_double(); h.Initialize_Canonical(GunParticleTSIP.phi, GunParticleTSIP.D0, GunParticleTSIP.Z0, GunParticleTSIP.omega, GunParticleTSIP.tanLambda, 2); return h;")
               .Define("reco_pt", "GunParticleTSIPHelix.getPXY()")
               .Define("reco_d0", "GunParticleTSIP.D0")
               .Define("reco_z0", "GunParticleTSIP.Z0")
               .Define("reco_phi0", "GunParticleTSIP.phi")
               .Define("reco_omega", "GunParticleTSIP.omega")
               .Define("reco_tanLambda", "GunParticleTSIP.tanLambda")
               .Define("reco_pvec", "auto p = GunParticleTSIPHelix.getMomentum(); return ROOT::Math::XYZVector(p[0], p[1], p[2]);")
               .Define("reco_p", "reco_pvec.R()") # sorry I didn't choose this method name
               .Define("reco_phi", "reco_pvec.Phi()")
               .Define("reco_theta", "reco_pvec.Theta()")

               .Define("GunParticleMCMom", "std::vector<double> v = {GunParticle.momentum.x, GunParticle.momentum.y, GunParticle.momentum.z}; return v;")
               .Define("GunParticleMCPos", "std::vector<double> v = {GunParticle.vertex.x, GunParticle.vertex.y, GunParticle.vertex.z}; return v;")
               .Define("GunParticleMCHelix", "auto h = HelixClass_double(); h.Initialize_VP(GunParticleMCPos.data(), GunParticleMCMom.data(), -1, 2); return h;")
               .Define("true_pt", "GunParticleMCHelix.getPXY()")
               .Define("true_d0", "GunParticleMCHelix.getD0()")
               .Define("true_z0", "GunParticleMCHelix.getZ0()")
               .Define("true_phi0", "GunParticleMCHelix.getPhi0()")
               .Define("true_omega", "GunParticleMCHelix.getOmega()")
               .Define("true_tanLambda", "GunParticleMCHelix.getTanLambda()")
               .Define("true_pvec", "ROOT::Math::XYZVector(GunParticleMCMom[0], GunParticleMCMom[1], GunParticleMCMom[2])")
               .Define("true_p", "true_pvec.R()") # sorry I didn't choose this method name
               .Define("true_phi", "true_pvec.Phi()")
               .Define("true_theta", "true_pvec.Theta()")
        )
        return df2

    def output():
        branchList = [
            "reco_pt",
            "reco_d0",
            "reco_z0",
            "reco_phi0",
            "reco_omega",
            "reco_tanLambda",
            "reco_p",
            "reco_phi",
            "reco_theta",

            "true_pt",
            "true_d0",
            "true_z0",
            "true_phi0",
            "true_omega",
            "true_tanLambda",
            "true_p",
            "true_phi",
            "true_theta",
        ]
        return branchList