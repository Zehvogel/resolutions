#! /usr/bin/bash
set -e

mkdir reco_output || true

k4run fccRec_e4h_input.py -n 1000 --input.EventDataSvc sim_output/single_e-_10GeV_90deg_edm4hep.root --filename.PodioOutput reco_output/single_e-_10GeV_90deg_rec_edm4hep.root