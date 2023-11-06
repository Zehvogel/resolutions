from DIRAC.Core.Base import Script
Script.parseCommandLine()

from ILCDIRAC.Interfaces.API.DiracILC import DiracILC
from ILCDIRAC.Interfaces.API.NewInterface.UserJob import UserJob
from ILCDIRAC.Interfaces.API.NewInterface.Applications import GaudiApp

import glob

dIlc = DiracILC()

# ParticleList = ["mu-", "e-", "pi-"]
ParticleList = ["mu-", "e-"]
# ParticleList = ["mu-"]
# MomentumList = ["1", "2", "5", "10", "20", "50", "100", "200"]
# 200 GeV events are really slow and big
MomentumList = ["1", "2", "5", "10", "20", "50", "100"]
# MomentumList = ["1", "2"]
ThetaList = ["10", "20", "30", "40", "50", "60", "70", "80", "89"]
# ThetaList = ["10", "20"]

args = [(Particle, theta, momentum) for Particle in ParticleList for momentum in MomentumList for theta in ThetaList]
outputBasenames = [f"REC_{arg[0]}_{arg[1]}deg_{arg[2]}GeV_1000evt" for arg in args]
outputFiles = [[f"{name}_aida.root", f"{name}_edm4hep.root"] for name in outputBasenames]
inputFiles = [f"SIM_{arg[0]}_{arg[1]}deg_{arg[2]}GeV_1000evt.edm4hep.root" for arg in args]

# TODO: use
detectorModel = "CLD_o2_v05"
detectorPath = f"$K4GEO/FCCee/CLD/compact/{detectorModel}/{detectorModel}.xml"


job = UserJob()
job.setSplitDoNotAlterOutputFilename()
job.setName('RecoSingleParticle_%n')
# job.setSplitParameter('particle', particles)
# job.setSplitParameter('energy', energies)
# job.setSplitParameter('theta', thetas)
job.setSplitParameter('outputBasename', outputBasenames)
job.setSplitParameter('inputFile', inputFiles)
job.setSplitInputData([f"LFN:/ilc/user/L/LReichenbac/resolutions/sim/{detectorModel}/{file}" for file in inputFiles])
job.setSplitOutputData(outputFiles, f'resolutions/rec_e4h/{detectorModel}', 'CERN-DST-EOS')
job.setOutputSandbox('*.log')
job.setInputSandbox(["CLDConfig/CLDConfig/PandoraSettingsCLD"])
# job.setInputSandbox(glob.glob("PandoraSettingsCLD/*"))

gaudi = GaudiApp()
gaudi.setExecutableName("k4run")
gaudi.setVersion("key4hep_nightly")
gaudi.setSteeringFile("CLDConfig/CLDConfig/CLDReconstruction.py")
gaudi.setInputFileFlag("--inputFiles")
gaudi.setOutputFileFlag("")
# TODO: turn on --trackingOnly
gaudi.setExtraCLIArguments(
    # "--inputFiles=%(inputFile)s "
    "--outputBasename=%(outputBasename)s "
    "-n 1000"
    f"geoservice.detectors={detectorPath}"
    )

job.append(gaudi)
job.submit(dIlc, mode="wms")