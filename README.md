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

# Overview of Signup Steps

The instructions in the next sections give details about how to sign up, configure and run a simple parflow demo on OSPool. This is a short summmary of the those steps.

    1. Signup for OSPool. Open an URL, fill out a form and request an account.

    2. Register. Register your ssh certificate with your OSPool account to be able ssh connect.

    3. Download ssh certificates. Download certificates to allow use of GIT on OSPool servers.

    4. Clone Repo. Connect to OSPool with ssh and clone the demo repo to Server.

    5. Configure hf_hydrodata email and pin with the demo.

    6. Run the Parflow demo on OSPool server.

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

## Register for SSH Connection

The instruction from the OSPool email will tell you to click [here](https://portal.osg-htc.org/documentation/overview/account_setup/comanage-access/) for instructions to connect to OSPool.
These instructions give you options to connect with a browser based connection or an ssh key.
The best way to connect is with an ssh key. You probably have an ssh public/private key in your .ssh folder on your laptop and/or verde.princeton.edu. 

To register your ssh keys with OSPool their
instructions will have you go to a [registration page](https://registry.cilogon.org/registry).
You may need to authenticate with CILogin.  This will take you to the OSG/Path Services page. On that page use the pull down menu at the top right "head" icon and pick "MY PROFILE (OSG)". 
From the next page select "Authenticators" from the options on the right. Then click "Manage" on the line with "SSH Public Keys".
There are pictures of this in the OSPool instructions [here](https://portal.osg-htc.org/documentation/overview/account_setup/comanage-access/).

From the Manage page press "Add SSH Key" and upload your public SSH key.
Your key should be on your machine in the directory:

    .ssh/id_ed25519.pub

After this you should now be be able 
to ssh from your laptop or linux server to the access point using the command below.
Use the username and accesspoint server name emailed to you by OSPool.

    ssh <username>@<accesspoint>

You also should be able to copy files to the access point server using scp.

## Generate a public/private key to Allow Git Clone
We want to be able to clone a Git repo to OSPool so you need to generate keys to use with Git Hub.

Connect to OSPool using ssh

    ssh <username>@<accesspoint>

Set current directory to .ssh and generate keys and change the permissions of files to only visible to you.

    cd ~/.ssh
    ssh-keygen -t ed25519 -C “your-email@domain”
    chmod 700 *

This will generate files id_ed25519.pub, id_ed25519.

Browse and sign in to your github account:
    https://github.com/youraccount

* Use the button in top right corner of the GitHub page get menu items and select "Settings". 

* Select "SSH and GPG keys". Press button "New SSH key".
* Paste a copy the file "id_ed25529.pub" (your public key) into the Key text field. This is probably a line that starts with "ssh-ed25519".
* Enter a name in the "Title" of the GitHub Setting "Add SSH Key" dialog. This is just a reminder for you the reason for this key.
* Press "Add SSH Key".

After this you should be able to git clone a repo to your account on OSPool.

## Visual Studio Code

Once you have setup the certificate based connection ability you should be
able to use Visual Studio Code to connect to the OSPool server from your laptop.
You can use this IDE to edit files on the OSPool access point server and a terminal to submit OSPool jobs.

## Apptainer

OSPool uses apptainer to support users to deploy software to their servers.
This is how we run parflow on OSPool servers.

Previously we built and copied an apptainer image containing parflow to the OSPool server
and stored this in a shared parflow project folder. You can see the file when you as ssh
connected to the access point.

    ls /ospool/uw-shared/projects/parflow/parflow_mpi_2025_10_01.sif

This apptainer image was built using code in this repo.
See [Building Apptainer Image](#building-a-parflow-apptainer-image) to build your own apptainer image.

You do not have to build your own apptainer image. There is already a parflow image on
the OSPool server and this is referenced in the .submit file in the demo example.


## Clone the demo to the OSPool Server

To run the demonstration using parflow on an OSPool server you must clone the example repo to your
access point. 

Any files you copy to the access point server are persisted as long as you have your OSPool account.

Use ssh to connect to your access point server. Then use GIT to clone this repo using these commands:

    git clone git@github.com:hydroframe/ospool_parflow.git


The demo uses hf_hydrodata to download parflow input files. This needs your email and PIN.
So before running the demo set your email and pin for hf_hydrodata. Edit the file "demo.sh" in the demo folder
and edit the lines

    export HF_EMAIL=xxxx
    export HF_PIN=nnnn

If you do not already have an HF_EMAIL pin (or it has expired) then create one
using this [link](https://hydrogen.princeton.edu/pin).

You can do a test run of parflow directly on the access point (like running on Verde head node).

    cd ospool_parflow/demo
    bash run_demo.sh

The run_demo.sh script runs a python script "demo.py" (from this repo) that uses subsettools to pull input data of a HUC to a project directory and then runs parflow using that directory. The run_demo.sh file executes the parflow run directly on the
OSPool access point server (only do this with small runs).

## Run Parflow on OSPool Execution Server
You can also run parflow on an OSPool execution server using Condor.
You can use an execution server for larger runs.
You need to first edit the demo.sh file with your hf_hydrodata email and pin so this is passed to the nodes.
Execute the following command from OSPool access point.

    condor_submit demo.submit

If the job is submitted this will respond with a message like:

    1 job(s) submitted to cluster 12713327.

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
These files are also specified in the demo.submit file. 

The pressure files from the parflow run are returned back from the job into the file:

    output.tar.gz

Any errors are returned into the file "demo.error". If the job finished successfully this file
will exist and by empty.

The stdout results of the job are is written to the "demo.output" file which contains the messages
produced by the job when it ran on the execution server.

These file names are all specified in the demo.submit file you used to submit the job.

You can extract all the files generated by the parflow run from the output.tar.gz by executing:

    tar xvf output.tar.gz

See [documentation](https://portal.osg-htc.org/documentation/htc_workloads/managing_data/file-transfer-via-htcondor/) for the OSPool documentation for submitted a job.


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

The demo.py file in the demo uses a utility file called "project.py" in this repo that
defines a function called "create_project" that simplifies the construction of a parflow
definition file and the calls to subset tools and pftools. Your own project probably uses subsettools
and pftools directly and this should also work fine as long as your code is in a GIT repo
that you can clone to the OSPool server in a similar way to this demo.

You will also have to create your own .submit job to invoke your project.
Use condor_submit to submit your job.

    condor_submit myjob.submit

This will execute your parflow run on an OSPool execution node and download the result files back
to your access node as specified in your version of demo.submit.


# Building a Parflow Apptainer Image

You should not need to build your own apptainer image since an image has already been created and
stored in a shared parflow project folder on the OS Server.

However, this section contains the instructions for how the apptainer image was created.
The apptainer tool is similar to docker, but the model and definitions files are quite different.
The apptainer tool is the same as a tool named singularity. All of these are tools create
containers that contain a copy of an operating system and all the installed tools for an
application. This allows you to run the code of an application on any linux server without
worrying about differences in the operating system or the installed tools on that server.
The various OSPool servers are all contributed from various instituations around the world and can have very different environments. 
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

This .sif file is also copied to the OSPool server and stored in a shared project folder called parflow
that is referenced by the demo project contained in this repo.
