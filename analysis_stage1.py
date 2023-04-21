class RDFanalysis():

    def analysers(df):
        df2 = (
            df
            .Alias("MCRecoAssociations0", "RecoMCTruthLink#0.index")
            .Alias("MCRecoAssociations1", "RecoMCTruthLink#1.index")
            .Alias("ReconstructedParticles", "PandoraPFOs")
            .Define("MC_genStat",
                    "ReconstructedParticle2MC::getRP2MC_genStat(MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, MCParticles)")
            .Define("MC_p",
                    "ReconstructedParticle2MC::getRP2MC_p(MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, MCParticles)")
            .Define("e_mc_p", "MC_p[MC_genStat == 1]")
        )
        return df2

    def output():
        branchList = [
                "MC_genStat",
                "MC_p",
                "e_mc_p"
        ]
        return branchList