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

### Certificate based Connection

The instruction from the OSPool email will tell you to click [here](https://portal.osg-htc.org/documentation/overview/account_setup/comanage-access/) for instructions to connect to OSPool.
These instructions give you options to connect with a browser based connection or an ssh key.
The best way to connect is with an ssh key. You probably have an ssh public/private key in your .ssh folder on your laptop and/or verde.princeton.edu. 

To register your ssh keys with OSPool their
instructions will have you go to a [registration page](https://registry.cilogon.org/registry).
You will need to authenticate with CILogin. Select "Princeton University" as the identity provider (or the identity provider of the email you used when you signed up with OSPool). This will take you to the registration page. On that page use the pull down menu at the top right "head" icon and pick "MY PROFILE (OSG)". 
From the next page select "Authenticators" and click "Manage" on the line with "SSH Keys".
There are pictures of this in the OSPool instructions [here](https://portal.osg-htc.org/documentation/overview/account_setup/comanage-access/).

From the Manage page press "Add SSH Key" and upload your public SSH key.
Your key should be on your machine in the directory:

    .ssh/id_ed25519.pub

After this you should now be be able 
to ssh from your laptop or linux server to the access point using the command below.
Use the username and accesspoint server name emailed to you by OSPool.

    ssh <username>@<accesspoint>

You also should be able to copy files to the access point server using scp.

Use this ability to copy your public/private keys to the access point server so you
can use GIT on OSPool server to clone workspaces and commit code from the OSPool access point.

From your laptop or linux machine.

    cd
    cd .ssh
    scp id_ed25519.pub <username>@<accesspoint>:/home/<username>/.ssh
    scp id_ed25519 <username>@<accesspoint>:/home/<username>/.ssh

With these keys on the OSPool access point you can clone and commit Git repos from the accesspoint.

### Visual Studio Code

Once you have setup the certificate based connection ability you should be
able to use Visual Studio Code to connect to the OSPool server from your laptop.
You can use this IDE to edit files on the OSPool access point server and a terminal to submit OSPool jobs.

### Clone Examples

You should also be able to use git clone while logged on the access point to pull code to the
access point. In particular you should be able to pull a copy of this repo with the examples
to the access point. Connect to the access point with ssh or with Visual Studio Code and a terminal window
and then execute this command to clone the repo with the examples.

    git clone git@github.com:hydroframe/ospool_parflow.git


# Apptainer

OSPool uses apptainer to support users to deploy software to their servers.
This is how we run parflow on OSPool servers.

All OSPool nodes are installed with apptainer so if you copy an apptainer image to
the OSPool access point it can be used to run parflow in OSPool.

See [Building Apptainer Image](#building-a-parflow-apptainer-image) to build your own apptainer image.
There is also a pre-built apptainer image for parflow on verde.princeton.edu.

    /home/SHARED/virtual-environments/parflow_mpi.sif


# Copy .sif file to OSPool access point

To run the demonstration using parflow on an OSPool server you must clone the example repo to your
access point. You must also copy a .sif file of the apptainer image to the demo folder of that cloned workspaces and
then run the parflow demo on the OSPool server.

Any files you copy to the access point server are persisted as long as you have your OSPool account.

Use ssh to connect to your access point server and clone this repo using these commands on the access point server.

    mkdir ~/workspaces
    cd ~/workspaces
    git clone git@github.com:hydroframe/ospool_parflow.git

Then back on your linux server where you have the sif file,  use scp to copy the .sif file to the demo directory of the clone workspace.

For example, from the verde.princeton.edu server use the pre-built .sif.

    cd /home/SHARED/virtual-environments
    scp parflow_mpi.sif <username>@<accesspointname>:/user/<username>/workspaces/ospool_parflow/demo

Then you can run parflow directly on the OSPool access point server with the commands below.
In these commands you must set your hf_hydrodata email and pin that is used by demo.py

    export HF_EMAIL=xxxx
    export HF_PIN=nnnn
    cd ~/workspaces/ospool_parflow/demo
    bash run_demo.sh

The run_demo.sh script runs a python script "demo.py" (from this repo) that uses subsettools to pull input data of a HUC to a project directory and then runs parflow using that directory. The run_demo.sh file executes the parflow run directly on the
OSPool access point server (only do this with small runs).

## Run Parflow on OSPool Execution Server
You can also run parflow on an OSPool execution server using Condor.
You can use an execution server for larger runs.
You need to first edit the demo.sh file with your hf_hydrodata email and pin so this is passed to the nodes.
Execute the following command from OSPool access point.

    condor_submit demo.submit

The condor_submit command is provided by OSPool on the access point server. It can be
used to submit a job just like the sbatch command on an HPC using slurm.

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
using subsettools or hf_hydrodata or some other code to construct a custom initial pressure head
for the parflow run. You could also add a "template" option to the parflow_options to specify
a custom version of parflow.yaml with custom values for all the parflow settings values if you wish.

Then use condor_submit to submit your job.

    condor_submit myjob.submit

This will execute your parflow run on an OSPool execution node and download the result files back
to your access node as specified in your version of demo.submit.


# Building a Parflow Apptainer Image

The apptainer tool is similar to docker, but the model and definitions files are quite different.
Each of docker, singularity and apptainer allow you to build an image of an operating system
and all installed tools and libraries so you can run code on any linux server. The various OSPool servers
are all contributed from various instituations around the world and can have very different environments.
Apptainer allows the ability to run an application (such as parflow) on any of these servers.

This repo contains a folder containing code to create an apptainer image that contains
parflow. There are two subfolders to create two different builds of parflow in different images.

    1. Parflow built with OpenMPI.
    2. Parflow built with the sequential (non-mpi) version of parflow.

Although OSPool does support some execution nodes with GPUs these servers may contain different
versions of GPU so it is difficult to create parflow GPU builds for all possible GPU types
so the GPU apptainer image was not create yet.

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
