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
    print(f"running reconstruction with Particle {Particle}-, Theta = {theta} deg, Momentum = {momentum} Gev")

    command = [
        "k4run",
        "fccRec_lcio_input.py",
        "-n", "1000",
        "--LcioEvent.Files", f"Output/SIM/SIM_{Particle}_{theta}deg_{momentum}GeV_1000evt.slcio",
        "--filename.PodioOutput", f"Output/REC/REC_{Particle}_{theta}deg_{momentum}GeV_1000evt_edm4hep.root",
    ]
    subprocess.run(command)

# Iterate over the lists
args = [(Particle, theta, momentum) for Particle in ParticleList for momentum in MomentumList for theta in ThetaList]
#print(args)
with Pool(6) as p:
    p.starmap(run, args, 1)
