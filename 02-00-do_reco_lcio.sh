#! /usr/bin/bash
set -e

mkdir reco_output || true

k4run fccRec_lcio_input.py -n 1000 --LcioEvent.Files sim_output/single_e-_10GeV_90deg.slcio --filename.PodioOutput reco_output/single_e-_10GeV_90deg_lcio_rec_edm4hep.root
