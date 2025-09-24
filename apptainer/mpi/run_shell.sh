#
# This script runs a container using the apptainer parflow_mpi.sif image with /bin/sh shell.
# This can be used for debugging and looking inside the container.
#
apptainer shell --shell /bin/sh parflow_mpi.sif
