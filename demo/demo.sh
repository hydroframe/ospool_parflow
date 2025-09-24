# It runs parflow using python and the demo.py program.
# The demo.py program uses subsettools to download input files for a HUC and runs parflow.
#
# The parflow input and output files are stored in the directory called demo in this dirctory.

export HF_EMAIL=
export HF_PIN=
python demo.py
tar -czf output.tar.gz demo/*.out.*

