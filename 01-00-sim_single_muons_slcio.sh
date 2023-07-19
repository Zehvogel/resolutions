#! /usr/bin/bash
set -e

mkdir sim_output || true

# decide on detector model up here
# newest released with smaller beampipe?
#COMPACT_FILE=$FCCDETECTORS/Detector/DetFCCeeCLD/compact/FCCee_o2_v02/FCCee_o2_v02.xml
# same as above?
#COMPACT_FILE=$LCGEO/FCCee/compact/FCCee_o2_v02/FCCee_o2_v02.xml
# even newer because it also has the fix for TrackerEndcapSupport...
#COMPACT_FILE=$LCGEO/FCCee/compact/FCCee_o2_v03/FCCee_o2_v03.xml
# used for CLD det note (says the note)
#COMPACT_FILE=$LCGEO/FCCee/compact/FCCee_o1_v04/FCCee_o1_v04.xml
COMPACT_FILE=$K4GEO/FCCee/CLD/compact/FCCee_o1_v04/FCCee_o1_v04.xml
# latest with bigger beampipe, and fixed TrackerEndcapSupport
#COMPACT_FILE=$LCGEO/FCCee/compact/FCCee_o1_v05/FCCee_o1_v05.xml

ddsim --compactFile $COMPACT_FILE \
      --outputFile sim_output/single_mu-_10GeV_89deg.slcio \
      --steeringFile CLICPerformance/fcceeConfig/fcc_steer.py \
      --random.seed 0123456789 \
      --enableGun \
      --gun.particle mu- \
      --gun.energy "10*GeV" \
      --gun.distribution uniform \
      --gun.thetaMin 89 \
      --gun.thetaMax 89 \
      --crossingAngleBoost 0 \
      --numberOfEvents 1000