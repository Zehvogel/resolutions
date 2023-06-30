#!/usr/bin/env python

import os
import subprocess
from multiprocessing import Pool

DetectorModel = "FCCee_o1_v04"
Nevts = "1000"

# Get the name of the current Python script
script_filename = os.path.basename(__file__)
print(f"-----> running {script_filename} with Detector Model = {DetectorModel}, Nevts = {Nevts}")

# Get the value of $LCGEO
LCGEO = os.environ.get("LCGEO")

# Define lists
ParticleList = ["mu", "e", "pi"]
MomentumList = ["1", "2", "5", "10", "20", "50", "100", "200"]
ThetaList = ["10", "20", "30", "40", "50", "60", "70", "80", "89"]

def run(Particle, theta, momentum):
    print(f"running ddsim with Particle {Particle}-, Theta = {theta} deg, Momentum = {momentum} Gev")

    command = [
        "ddsim",
        "--compactFile",
        f"{LCGEO}/FCCee/compact/FCCee_o2_v02/FCCee_o2_v02.xml",
        "--outputFile", f"Output/SIM/SIM_{Particle}_{theta}deg_{momentum}GeV_1000evt.slcio",
        "--steeringFile", "CLICPerformance/fcceeConfig/fcc_steer.py",
        "--random.seed", "0123456789",
        "--enableGun",
        "--gun.particle", f"{Particle}-",
        "--gun.energy", f"{momentum}*GeV",
        "--gun.distribution", "uniform",
        "--gun.thetaMin", f"{theta}*deg",
        "--gun.thetaMax", f"{theta}*deg",
        "--crossingAngleBoost", "0",
        "--numberOfEvents", "1000"
    ]
    subprocess.run(command)

# Iterate over the lists
args = [(Particle, theta, momentum) for Particle in ParticleList for momentum in MomentumList for theta in ThetaList]
#print(args)
with Pool(6) as p:
    p.starmap(run, args, 1)
