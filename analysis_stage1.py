class RDFanalysis():

    def analysers(df):
        df2 = (
            df
            .Alias("MCRecoAssociations0", "RecoMCTruthLink#0.index")
            .Alias("MCRecoAssociations1", "RecoMCTruthLink#1.index")
            .Alias("ReconstructedParticles", "PandoraPFOs")
            # plan for this stage: create new columns for reco and mc electrons
            .Define("RP_MC_index",
                    "ReconstructedParticle2MC::getRP2MC_index(MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, MCParticles)")

        )
        return df2

    def output():
        branchList = [
                "MC_p",
        ]
        return branchList