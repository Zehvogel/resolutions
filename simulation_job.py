from DIRAC.Core.Base import Script
Script.parseCommandLine()

from ILCDIRAC.Interfaces.API.DiracILC import DiracILC
from ILCDIRAC.Interfaces.API.NewInterface.UserJob import UserJob
from ILCDIRAC.Interfaces.API.NewInterface.Applications import DDSim

dIlc = DiracILC()

# ParticleList = ["mu-", "e-", "pi-"]
ParticleList = ["mu-", "e-"]
#ParticleList = ["mu-"]
# MomentumList = ["1", "2", "5", "10", "20", "50", "100", "200"]
MomentumList = ["1", "2", "5", "10", "20", "50", "100"]
#MomentumList = ["1", "2"]
ThetaList = ["10", "20", "30", "40", "50", "60", "70", "80", "89"]
#ThetaList = ["10", "20"]

# all the split parameters need to be of equal length,
# so parse this set of arguments back into its components
args = [(Particle, theta, momentum) for Particle in ParticleList for momentum in MomentumList for theta in ThetaList]
particles = [arg[0] for arg in args]
thetas = [arg[1] for arg in args]
energies = [arg[2] for arg in args]
outputFiles = [f"SIM_{arg[0]}_{arg[1]}deg_{arg[2]}GeV_1000evt.edm4hep.root" for arg in args]

detectorModel = "FCCee_o1_v04"
# detectorModel = "CLD_o2_v05"

job = UserJob()
job.setSplitDoNotAlterOutputFilename()
job.setName('DDSimSingleParticle_%n')
job.setSplitParameter('particle', particles)
job.setSplitParameter('energy', energies)
job.setSplitParameter('theta', thetas)
job.setSplitParameter('outputFile', outputFiles)
job.setSplitOutputData(outputFiles, f'resolutions/sim/{detectorModel}', 'CERN-DST-EOS')
job.setOutputSandbox('*.log')

ddsim = DDSim()
ddsim.setVersion('key4hep_nightly')
ddsim.setDetectorModel(detectorModel)
ddsim.setNumberOfEvents(1000)
ddsim.setSteeringFile("CLDConfig/CLDConfig/cld_steer.py")
# 😠😠😠
#ddsim.setEnergy("%(energy)s")
# the named placeholder '%(particle)s' has the same name as the first argument of setSplitParameter
ddsim.setExtraCLIArguments(
    "--enableGun "
    "--gun.particle=%(particle)s "
    "--gun.distribution=uniform "
    "--gun.thetaMin=%(theta)s*deg "
    "--gun.thetaMax=%(theta)s*deg "
    "--crossingAngleBoost=0 "
    "--gun.energy=%(energy)s*GeV "
    )
ddsim.setOutputFile('%(outputFile)s')

job.append(ddsim)
job.submit(dIlc, mode="wms")