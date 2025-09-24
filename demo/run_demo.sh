#
# This script runs parflow using the parflow_mpi.sif image
# It runs parflow using python and the demo.py program.
# The demo.py program uses subsettools to download input files for a HUC and runs parflow.
#
# The parflow input and output files are stored in the directory called demo in this dirctory.

apptainer exec ../apptainer/mpi/parflow_mpi.sif python demo.py
