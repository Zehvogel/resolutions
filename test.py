class RDFanalysis():

    def analysers(df):
        df2 = (
            df
            .Define("GunParticles", "MCParticles[MCParticle::get_genStatus(MCParticles) == 1]")
            .Define("GunParticles_p", "MCParticle::get_p(GunParticles)")
            .Define("GunParticles_e", "MCParticle::get_e(GunParticles)")
        )
        return df2

    def output():
        branchList = [
                "GunParticles_p",
                "GunParticles_e"
        ]
        return branchList