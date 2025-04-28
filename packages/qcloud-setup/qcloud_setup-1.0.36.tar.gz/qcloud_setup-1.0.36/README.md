-----------------------------------------------------------------------

<h1 align="center"> Q-Cloud Administrator Documentation </h1>

-----------------------------------------------------------------------


## Introduction

Q-Cloud is a framework that allows users to easily launch elastic compute
clusters on AWS and submit Q-Chem calculations to them.  The clusters will
automatically expand with demand, up to the maximum size determined by
the type of Q-Cloud license purchased, and idle nodes will shut down to 
minimize running costs.

Q-Cloud clusters are built around three separate AWS service stacks with the
following names and purposes:
1. _qcloud-users_: This stack controls user access to the cluster.  It
   launches a Cognito service which manages users, passwords and access tokens.
2. _qcloud-api-gateway_: This stack provides the REST endpoints for submitting jobs to
   the cluster and for accessing the results from calculations.  
3. _qcloud-cluster_: This is the actual compute cluster and consists of a head node
   (which can be just a t2.micro instance) running a SLURM workload manager.
   The head node is responsible for launching the compute instances which run
   the Q-Chem calculations.  The head node runs for the lifetime of the
   cluster, but the compute nodes run on-demand and automatically terminate
   when there are no jobs in the queue.

**Note:** Charges apply to many AWS services.  See the Costs section for
further details and information on how to minimise the running costs of the
cluster.


## Prerequisites

The cluster administrator will need to have a valid AWS account and be able to
log into their account via the [console](https://signin.aws.amazon.com/) in
order to obtain access and secret access keys.

Users of the cluster do not require AWS accounts as their access to the
cluster is configured separately, (see the Adding users section below for
further details on setting up user accounts).

The Q-Cloud packages require you to have python (v3.9 or later)
installed on the local machine used to administer the cluster.  

The following steps are required to set up a Q-Cloud cluster.

## 1) Obtain access keys

This step can be skipped if you have already configured the AWS CLI.  

Open up the AWS [console](https://signin.aws.amazon.com/) in a browser.  Search 
for IAM and select the first hit.  This brings up the IAM dashboard.

1. From the left hand panel select 'Users' and then click on the name of a user
   with administrator privileges (i.e. the AdministratorAccess permissions
   policy has been attached).   Note this administrator user is only required
   to create the qcloud_admin user with restricted permissions and is not used
   to launch any of the Q-Cloud resources.
2. Select the 'Security credentials' tab and scroll down to the 'Access keys'
   section and click the 'Create access key' button.
3. Select the 'Command Line Interface CLI' option as the use case, check
   the confirmation checkbox and click the Next button.
4. Enter a description for the key and click 'Create access key'.
5. Make a note of both the access key and the secret access key.  You will not
   have another opportunity to see the secret key, so if you misplace it you
   will need to deactivate the key and generate a new one.  The access keys 
   look something like the following:
```
aws_access_key_id = AKIBS7OH2PUVOGH8A9ZT
aws_secret_access_key = 5rV7LzKMLKNUO+IupIgsdj876FSx8nPLdfy7F9A4
```


## 2) Install the qcloud_setup script

Download the install_qcloud.sh script, add executable permissions  and run it:
```
wget https://downloads.q-chem.com/install_qcloud.sh
chmod +x install_qcloud.sh
./install_qcloud.sh
```
This will create a virtual environment with the required Python packages installed.
Make a note of the directory created for the virtual environment (this is output
at the end of the install script).  To activate the virtual environment and run
the qcloud_setup script, simply type.
```
bash
cd /path/to/qcloud_venv
source env/bin/activate
qcloud_setup [options]
```
Note the bash line is only required if bash is not your regular shell.
To exit the virtual environment after setting up your cluster simply, type 
```
deactivate
```
You will need to activate the virtual environment before using the qcloud_setup
command.


## 3) Configure cluster
Within the virtual environment, cluster configuration files can be generated with the command: 
```
qcloud_setup --configure
```
This takes the user through an interactive setup process which produces a
configuration file with the name *qcloud-cluster.config* which can be viewed
before launching the cluster.  Do not modify the contents of the configuration
file as it may cause subsequent steps in the setup to fail.

By default the name of the cluster is 'qcloud', but this can be changed using
the `--name <cluster_name>` option.  This allows for multiple clusters to run
at the same time, if required.  Note that if a non-default name is specified
then this name must be passed using the `--name` option to subsequent commands
(e.g. `--launch`) in order that they operate on the correct cluster.

The options specified in the configuration process are discussed in detail below.


#### 3.1) AWS Credentials

These should have been configured previously for the qcloud_admin user and, if
so, are automatically detected. 

A new SSH key pair will be created to connect to the head node instance and the
private key will be saved in the qcloud\_\<region\>\_keypair.pem file.   This
file needs to be available when performing many of the qcloud_setup commands,
either in the current directory or by copying it to the location of your other
key files (e.g. the ~/.ssh directory).  Do not lose this private key as you
will be unable to connect to the head node without it.


#### 3.2) VPC setup

The Q-Cloud cluster runs inside a Virtual Private Cloud (VPC) and it is
recommended that a new VPC be created for running the Q-Cloud cluster.
However, because there is a limit on the number of VPCs per AWS account, this may
not be possible for some users. Please select whichever of the following 
options is best for your case:

- Default: This option will use your default VPC and both the head node and
  compute clusters will be in a public subnet (not recommended).
- Use existing: If available.  The setup script will look for a previously
  configured Q-Cloud VPC.  This will have both public (for the head node) 
  and private (compute nodes) subnets configured.
- Create new: This will create a new VPC with public and private subnets.  
  The availability zone of the subnets does not matter.


#### 3.3) Compute instance types

The costs shown are indicative only and are for running each instance. They
do not include storage or network costs.  Note the difference between c5 and
c5d instance types is the latter uses local NVMe-based SSD block storage which
is physically connected to the instance and therefore faster.


#### 3.4) Maximum compute nodes
This determines the maximum number of compute instances that can run concurrently. 
If more jobs are submitted than this value, they will be queued until the resources
become available.

This value should be set to the same number as the number of seats purchased as
part of your license.


#### 3.5) Job files
This is the space allocated for the jobs volume which is attached to the head
node and shared between compute instances.  This volume is used for output
files only and can be quite small.  Output files are automatically deleted
after they have been copied to the S3 bucket.


#### 3.6) Scratch files

This determines the scratch volume size per instance. As an indicative cost,
100Gb costs around $10/month.


## 4) Launching the cluster

Once a configuration file has been generated, the service stacks can be
launched with the following:
```
qcloud_setup  --launch 
```
The configuration file is automatically updated with values for the place holders
as the various resources are created.  

**Notes:** 
1. Some steps in the launch process can take several minutes to complete, in
   particular building the cluster stack.  Migrating the Q-Cloud software to
   your region can take a variable amount of time depending on network load.
2. If you terminate the the qcloud\_setup script during the creation process
   the stack will continue to be created.  Use the `--delete` option to
   actually delete or stop the stack creation.  
3. Interrupting the launch process may leave a temporary snapshot lying around.
   To delete this, log into the [AWS console](https://signin.aws.amazon.com/) and
   navigate to EC2 &#8594; Snapshots.  Any Q-Cloud snapshots can be safely deleted
   as long as you are not currently launching a cluster.

Once launched, you will need to send the following information to
license@q-chem.com to obtain your license activation key:

- Order number
- Name 
- University / Institution
- Elastic IP address (provided as output from the launch command)

Once you have your activation key, you can install it as follows:
```
qcloud_setup  --activation-key XXXX-XXXX-XXXX-XXXX-XXXX
```
This command requires access to the SSH key generated during the configuration
step, which should be either in the current directory or in your home directory
under ~/.ssh.



## Adding users
Before submitting jobs, a user will need to be added to the Cognito user pool:
```
qcloud_setup --add-user <user_name> --email <email_address>
```
Alternatively, you can add multiple users from a file:
```
qcloud_setup --add-users <file_name>
```
where the file\_name consists of a list of user names and email addresses with the 
format:
```
elmo     elmo@gmail.com
bigbird  bigbird@gmail.com
...
```

A message will be sent to the user's email address with their user name and a
temporary password, which will need to be changed when first attempting to
submit a job.

Note that the number of users able to be added each day is limited to 50 due to
email limits in the Cognito service.  If you need to add more than this you
will need to configure Cognito with the Simple Email Service' (SES) and add a
validated administrator email.

The cluster administrator will need to provide the server details to each 
user which can be obtained by running the command:
```
qcloud_setup --user-info
AwsRegion                        us-east-1
CognitoUserPoolId                us-east-1_KbkdtpKpW
CognitoAppClientId               2mgcn0o8fkakboq7jnqs6bd6ee
ApiGatewayId                     fkkxolpuo4
```
If these values are saved to a file:
```
qcloud_setup --user-info > user_info.txt
```
then the cluster users can use this file to configure the client:
```
qcloud --configure user_info.txt
```
Cluster users will need to install and configure the command line interface (CLI):
```
python3 -m pip install qcloud_user
```
this will install the qcloud command into their python environment and this can be configured
by running the following command and entering the values from the 
`qcloud_setup --user-info` command
```
qcloud --configure
```
The first time a user interacts with the cluster they will need to enter the temporary
password emailed to them before resetting their password.

See the README.md file distributed with the qcloud\_user module for further
details on interacting with the server.




## Suspending a Cluster

It is possible to shut down the cluster head node and restart it at a later
time in order to minimise the running costs.  If you plan to restart the
cluster, make sure to keep copies of the configuration file, ssh key (.pem
file) and activation key.

Use the `--suspend` option to delete only the cluster stack.  You will be prompted
if you want to delete the stack, type 'y' to confirm.

```
qcloud_setup --suspend
Delete stack qcloud-cluster? [y/N] y
```
This terminates the head node, but leaves the API gateway and Cognito stacks
running, using minimal resources.  Once the cluster has been deleted, the
results of previous jobs can still be accessed via the API gateway as these are
archived in an S3 bucket.  You will, of course, be unable to submit further
jobs until the cluster has been restarted.

To re-launch the cluster, issue the following command in the same directory as
the configuration and license files:

```
qcloud_setup  --launch 
qcloud_setup  --activation-key XXXX-XXXX-XXXX-XXXX-XXXX
```

**Note:** In order to restart a cluster, you must have configured the cluster to
use an elastic IP (EIP) address allocated to your AWS account. This EIP must be
available for reuse when re-launching the cluster, otherwise the Q-Chem license
will no longer be valid.

If you need to update the EIP of your host, please contact our support team at 
support@q-chem.com for assistance.


## Teminating a cluster
Before terminating a cluster, ensure there are no jobs running in the queue and
that you have downloaded the results of any calculations you wish to keep.  The
following command will  delete the cluster:
```
qcloud_setup --delete
```
You will be asked whether you want to delete each of the 3 stacks, 
and you should type 'y' for each.

To clean up all the resources allocated to the cluster, be sure to release the
elastic IP address and clean out any files created in the S3 bucket.


## Other options

Additional options for the setup script can be printed via:

```
qcloud_setup  --help
qcloud_setup  --info
qcloud_setup  --list
```

You can also open an ssh connection to the head node using the following:
```
qcloud_setup  --shell
```

## Costs

The costs associated with running the cluster hardware will be dominated by the
compute nodes used to run calculations.  These costs depend on the type of node
and the region configured during setup and can be estimated using the 
[AWS Cost Estimator](https://calculator.aws/#/addService/ec2-enhancement).

In addition to the compute-node costs, there are overhead costs associated with
running the head-node used for job submissions which will be incurred even if
there are no running jobs.  A low-cost T2 instance is used for this purpose and
will attract a monthly cost of around $10, depending on the amount of job
storage selected at setup time.

The costs associated with the head-node can be minimized by suspending the
cluster when not in use.  If this is done, there will still be a residual
charge for maintaining the elastic IP which is required for licensing.  This
cost is approximately $3.65 per month. 

*Note*: These costs are managed by AWS and will be charged to the account used
to launch the Q-Cloud cluster, they are separate from the Q-Cloud subscription
fee which is charged by Q-Chem Inc.

To monitor the costs associated with the cluster, the following will
give a summary of the costs recorded for the last 28 days:
```
qcloud_setup  --costs
```
You can also set notifications for when expenditure reaches 75% and 99% of
a specified budget, or when the expenditure is predicted to exceed the 
budgeted figure:
```
qcloud_setup  --set-budget n
```
where n is a integer number of USD.  

*Note*: Currently these cost settings apply to the entire AWS account.





## Troubleshooting

- When launching the cluster, if you receive permission problems associated
  with lambda functions, check to ensure that the IAM policy (QCloudIamPolicy) has been
  created in the same region as the cluster.

- When submitting jobs, a job ID should be returned. This is a random
  sequence of 12 alphanumeric characters associated with your job.  If you do
  not see a job ID, it is possible the submit function has not been updated
  with the instance ID of the head node.  Re-run the launch command to trigger
  this update:
```
qcloud_setup --launch
```

- If you encounter any problems not covered here, please contact our support team at 
  support@q-chem.com for assistance. 

