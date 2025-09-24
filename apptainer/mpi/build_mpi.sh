#
# Script to build the parflow_mpi.sif apptainer image containing parflow with MPI.
#
rm -rf parflow_mpi.sif parflow_mpi.log
apptainer build parflow_mpi.sif parflow_mpi.def 2>&1 | tee parflow_mpi.log

