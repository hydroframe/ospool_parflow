# Run Parflow using OSPool

This repo contains instructions how to run parflow using OSPool servers.


## Introduction
The OSPool is a source of computing capacity that is accessible to any researcher affiliated with a US academic institution.
<code> https://portal.osg-htc.org</code>

OSPool is pool of compute servers contributed by over 78 institutions. You use it by using
ssh to connect to a Access Point server (like the head node in an HPC cluster). From the
access point you can submit jobs using a scheduler to run on execution nodes.

OSPool is an HTC cluster of server (see [HTC vs HPC](https://www.geeksforgeeks.org/mobile-computing/difference-between-high-performance-computing-and-high-throughput-computing/)). This is similar
to an HPC cluster, but there is no slurm and no MPI between nodes. There is a scheduler (Condor)
and you can distribute execution of jobs using mutiple execution nodes like HPC. You can run MPI
on a single execution node which may have up to 50+ cpus. 

When parflow runs in OSPool it can use those cpus and MPI in the same way as an HPC cluster, but only
using a single execution node. You can submit jobs to run using multiple execution nodes, but there is no MPI between those nodes.

OSPool is free for accademic researchers and can be useful for researchers that want to use
parflow for medium sized simulations, but do not have access to an HPC.

The support email from the OSPool team is: support@osg-htc.org.

They have office hours.
Signup for OSPool office hours [here](https://docs.google.com/forms/d/e/1FAIpQLSd3K78Xx1Vo-KjqW_2y0YKcUMXrEsKXWk3I1Aww64RL22QpnQ/viewform).

    Tuesdays, 4-5:30pm ET / 1-2:30pm PT
    Thursdays, 11:30am-1pm ET / 8:30-10am PT
    

## Signup For OSPool
To get an account to use OSPool you start by registering with the 
[signup]( https://portal.osg-htc.org/application#:~:text=If%20you%20are%20a%20researcher%20affiliated%20with,for%20you%20to%20harness%2C%20just%20sign%20up!) web site.

After submitted the signup request you will asked to signup for a consultation with
OSPool. This is a zoom meeting where an OSPool support engineer will give you an
overview of OSPool and ask you how you are trying to use it. They will also help you with
getting started questions. 

The email response after you submit your signup request will have instructions. It will tell
you go to this link [schedule appointment](https://osgfacilitation.setmore.com/?utm_source=email&utm_medium=bookingpage). You select "Reseacher Consultation for OSG Access Point" and
pick a day and time for your appointment.

You will get a reminder about your appointment and eventually (probably day of your appointment)
they will send you a zoom link or a google meet link.

After your consultation they will send you an email with your ssh connection information
for the access point. The connection information will be:

    * accesspointname
    * username

The access point name they sent me was:
   ap40.uw.osg-htc.org
However, you may be assigned a different access point.

I was given 41 GB of disk space quota when I signed up. You could negotiate for more with a good reason I think.

## Connecting to Access Point

The first time you use ssh to the OSPool access point you must use browser based authentication.
After you are connected the first time you can setup your certificates in your .ssh directory
so you can later use public/private key authentication.

### Browser based Connection

Connect from using the command line.

    ssh <username>@<accesspointname>

This will respond with a message like:

Authenticate at
   https://cilogon.org/device/?user_code=FF4-ZX6-9LK
   Type 'Enter' when you authenticate.

Browse to that url. Enter your credentials from your own instition. You use the account
associated with the email address you provided when you originally signup.

Then press Enter in the shell script command you started with "ssh".

After this you should be connected to the access point.

You should then create files on the access point server in the .ssh folder the home directory of your access point.

    mkdir ~/.ssh
    touch ~/.ssh/id_ed25519.pub
    touch ~/.ssh/id_ed25519

Copy the contents of the files id_ed25519.pub and id_ed25519 from your laptop or linux server .ssh folder to
the files in the OSPool access point.

One way to copy the files is to put the contents of the ~/.ssh/id_ed25519.pub file from your laptop or linux server into your clipboard. Then execute:

    cat > ~/.ssh_id_ed25519.pub
    <right click>
    ^D

Note: ^D means control D key. This is the end of file character.

Then copy the contents of the ~/.ssh/id_ed25519 file from your laptop or linux server into your clip board. Then execute:

    cat > ~/.ssh_id_ed25519
    <right click>
    ^D


After you copy the files then copy the public key to the authorized_keys file

    cd ~/.ssh
    cp id_ed25519.pub authorized_keys

Finally make sure all the files have the correct permissions:

    cd ~/.ssh
    chmod 700 *

### Certificate based Connection

After you added all the ssh keys and logout of the access point you should now be be able
to ssh from your laptop or linux server to the access point using the command:

    ssh <username>@<accesspoint>

And it should not prompt you for password since your public key is in the authorized_keys file.

### Copying Files to the Access Point Server

Once you have setup certificate based connection
you should also be able to copy files to the access point from your laptop or linux server using scp.

    scp <file> <username>@<accesspoint>:/user/<username>/<file>

You should also be able to use Visual Studio code to remote connect to the access point.

You should also be able to use git clone while logged on the access point to pull code to the
access point. In particular you should be able to pull a copy of this repo with the examples
to the access point.

    git clone git@github.com:hydroframe/ospool_parflow.git

# Apptainer

OSPool uses apptainer to support users to deploy software to their servers.
Apptainer is the same as singularity, and is similar to docker.
Although it is similar to docker the definition files are very different and
the model of how it is used is quite different.

This repo contains a folder containing code to create an apptainer image that contains
parflow. There are two subfolders to create two different builds of parflow.

    1. Parflow build with OpenMPI.
    2. Parflow built with the sequential (non-mpi) version of parflow.

Although OSPool does support some execution nodes with GPUs the servers may contain different
versions of GPU so it is difficult to create parflow GPU builds for all possible GPU types
so the GPU apptainer image was not create yet.

All OSPool nodes are installed with apptainer so if you copy an apptainer image to
the OSPool access point it can be used to run parflow in OSPool.

# Building a Parflow Apptainer Image

You can build your own apptainer image of parflow from any linux server that has apptainer installed.
You can build it with scripts from this repo. Below shows how to build the MPI image.

    cd apptainer/mpi
    bash build_mpi.sh

This can take several minutes. It displays the log to stdout and also writes the log of the build
into the file parflow_mpi.log that you can use to see errors if the build fails.

When the build succeeeds it creates a file called parflow_mpi.sif. The .sif file is an
apptainer image.

In princeton there is an already built parflow_mpi.sif on the server named verde.princeton.edu in the
folder below. The .sif files is about 800 MB.

    /home/SHARED/virtual_environments/parflow_mpi.sif

# Copy .sif file to OSPool access point

You can run a demonstration of using parflow on an OSPool server by cloning this repo to your
access point and then copying the .sif file to the demo folder of that cloned workspaces and
then run the parflow demo on the OSPool server.

First ssh to your access point server and clone this repo using this command on the access point.

    mkdir ~/workspaces
    cd ~/workspaces
    git clone git@github.com:hydroframe/ospool_parflow.git

Then from your linux server where you have the sif file use scp to copy the .sif file to the demo directory of the clone workspace.

    cd /home/SHARED/virtual-environments
    scp parflow_mpi.sif <username>@<accesspointname>:/user/<username>/workspaces/ospool_parflow/demo

Then you can run parflow directly on the OSPool access point server with the command.
You must first set your hf_hydrodata email and pin that is used by demo.py


    export HF_EMAIL=xxxx
    export HF_PIN=nnnn
    cd ~/workspaces/ospool_parflow/demo
    bash run_demo.sh

The run_demo.sh script runs a python script "demo.py" (from this repo) that uses subsettools to pull input data of a HUC to a project directory and then runs parflow using that directory.

## Run Parflow on OSPool Execution Server
You can run parflow on an OSPool execution server using Condor.
You need to first edit the demo.sh file with your hf_hydrodata email and pin so this is passed to the nodes.

    condor_submit demo.submit

The condor_submit command is provided by OSPool on the access point server. It can be
used to submit a job just like the sbatch command on HPC using slurm.

The demo.submit file is provided in the ospool_parflow workspace in the demo folder.
The demo.submit specifies the executable as the demo.sh file that runs our python demo.py.
The parflow_mpi.sif container to use on the nodes is also specified in the demo.submit file.

You can check the queue status of a submitted job using the command.

    condor_q

If the Idle column is "1" then the job is still in the queue and not executing. It typically
takes 2 minutes or so until a job starts running. If the Hold column is "1" the job is on hold
and not running yet. If the Run column is "1" then the job is still running.

The selected files in your current directory are copied to the execution server when the job runs.
These files are specified in the demo.submit file.

You can cancel a job using the job Id of the job using.

    condor_rm <job_id>

After the job is complete the selected files are copied back to the access point so you can see the results.
These files are also specified in the demo.submit file. In the demo this is output.tar.gz.

See [documentation](https://portal.osg-htc.org/documentation/htc_workloads/managing_data/file-transfer-via-htcondor/).

The stdout of the executing job is also copied back into the file demo.output and any errors
are copied back into the file demo.errors. This is specified in the demo.submit file we
used to create the job.

## Run Parflow Using Your Own Project

You can run parflow with your own project in the same way except provide your own demo.py demo.submit and demo.sh file.

You do not need to use the project.py or the template_runscripts used in this example, but your project
must collect the input files in your version of demo.py and you must list the source files you need in your
version of demo.py in your version of demo.submit file.


If you need to install your own custom python components you need to pip install them into the
container loaded from parflow_mpi.sif. You can do that in your version of demo.sh such as myjob.sh.

    myjob.sh
        python -m pip install mycomponent1 mycomponent2
        python myproject.py

If you do use project.py and the create_project() function to create your parflow directory you
can set custom values of any parflow setting file from the runscript that is initialized by the
parflow template used for the project. For example, you can set the initial pressure head with
this code in your demo.py file after calling create_project() to create the runscript_path:

    runscript_path = project.create_project(parflow_options, directory_path)
    model = parflow.Run.from_definition(runscript_path)
    model.domain.ICPressure.FileName = "my_ss_pressure_head.pfb"
    model.write(file_format="yaml")

You can add code in your version of demo.py to construct or download your my_ss_pressure_head.pfb
using substtools or hf_hydrodata or some other code to construct a custom initial pressure head
for the parflow run. You could also add a "template" option to the parflow_options to specify
a custom version of parflow.yaml with custom values for all the parflow settings values if you wish.

Then use condor_submit to submit your job.

    condor_submit myjob.submit

This will execute your parflow run on an OSPool execution node and download the result files back
to your access node as specified in your version of demo.submit.


