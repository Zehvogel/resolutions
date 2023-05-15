class RDFanalysis():

    def analysers(df):
        df2 = (
            df
            .Alias("MCRecoAssociations0", "RecoMCTruthLink#0.index")
            .Alias("MCRecoAssociations1", "RecoMCTruthLink#1.index")
            .Alias("ReconstructedParticles", "PandoraPFOs")
            # plan for this stage: create new columns for reco and mc electrons
            .Define("RP_MC_p",
                    "ReconstructedParticle2MC::getRP2MC_p(MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, MCParticles)")
            # not this easy because the NaNs will be inside the RVec :(
            #.Define("RP_MC_p_clean", "std::isnan(RP_MC_p) ? -1 : RP_MC_p")


        )
        return df2

    def output():
        branchList = [
                "RP_MC_p",
        ]
        return branchList