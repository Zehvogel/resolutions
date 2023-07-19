#! /usr/bin/bash
set -e

mkdir reco_output || true

k4run fccRec_lcio_input_new.py -n 1000 --LcioEvent.Files sim_output/single_mu-_10GeV_89deg.slcio --filename.PodioOutput reco_output/single_mu-_10GeV_89deg_lcio_rec_edm4hep.root
