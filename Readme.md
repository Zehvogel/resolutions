At the moment this is a bit of a playground for me to figure out how to best generate, reconstruct and analyse single particle (and other) samples for detector optimisation studies for CLD

Currently the following things are possible:

### Simulating single electrons with a particle gun
```
./01-00-sim_single_electrons.sh
```
creates the folder `sim_output` and save the simulated electrons there.

It is also possible to create a ROOT tree containing energy and momentum of the generated electrons via

```
./01-01-create_tree.sh
```
The created tree can be analysed with the `validate_output.ipynb` jupyter notebook, so far this only plots a histogram of the energy.

### Reconstruction
```
02-00-do_reco.sh
```
does the reconstruction and saves edm4hep output into the folder `reco_ouput`

FIXME: currently also still writes REC file slcio output