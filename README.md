# Create a live stream video using Amazon Rekognition, Kinesis Video Streams, Kinesis Data Streams and GStreamer 

## Introduction
The purpose of this project is to demonstrate how the use of deep learning/machine learning (applied in image and video) features offered by **AWS** works.

With this prototype, you'll be able to setup what is needed to run real-time video capture and analyze it using advanced tools.

Here's the prototype's conceptual architecture:
![enter image description here](https://d1.awsstatic.com/re19/KVS_WebRTC/product-page-diagram_Kinesis-video-streams_how-it-works_01.cb5682fffec40aed239111f7454a586b31d6e680.png)
If you are starting from scratch and are unfamiliar with Python, completing all the steps may take a few hours.

## Preparing your development environment
Items in this checklist are required for the development environment:

 1. Download and install Python version 3.7+ and the Pip package manager. Follow the instructions (according to your operating system) on the [official website](https://www.python.org/downloads/) of the distributor. 
 2. Create a Python [virtual environment](https://virtualenv.pypa.io/en/stable/) for the project using Virtualenv. This will cause project dependencies to be isolated from your Operating System. Once you create the python environment, enable it before proceeding to the next steps.
 3. Use Pip to install [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html), and [configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) it right after. To be able to run this project, you must have all permissions for the following services:
	 - Amazon Rekognition
	 - Amazon Kinesis Video Streams
	 - Amazon Kinesis Data Streams
4. <a name = "aws-config"></a>Make sure you have one of selected the regions that have access to the services mentioned:
	 - us-east-1
	 - us-west-2
	 - us-west-1
5. Clone this GitHub repository. Install all dependencies (using the environment pip we created in **step 2**) that are described in the "**requirements.txt**" file which is inside of the project.
 

## Preparing AWS environment
Right after preparing the environment for development, we should create Amazon services:

 1. Create an IAM service role to give Amazon Rekognition Video access to your Kinesis video streams and your Kinesis data streams. Note the ARN,  we will need this later.
	   1. [Create an IAM rule](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html). Use the following information.
		   1. Choose **Rekognition** for the service name
		   2. Choose **Rekognition** for the service role use case
		   3. Choose the **AmazonRekognitionServiceRole** permissions policy, which gives Amazon Rekognition Video write access to Kinesis data streams that are prefixed with AmazonRekognition and read access to all your Kinesis video streams.
	2. Note the Amazon Resource Name (ARN) of the service role. You need it to start video analysis operations.

 2. Create a [Kinesis Video Streams](https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/gs-createstream.html) and write down the generated ARN.
 3. Create a [Kinesis Data Streams](https://docs.aws.amazon.com/streams/latest/dev/introduction.html) and write down the generated ARN.

## Preparing Kinesis Video Streams Producer SDK
### Introduction
A Kinesis Video Streams Producer is any application that makes it easy to securely connects to a video stream, and reliably publishes video and other media data to Kinesis Video Streams.

Amazon offers SDK in two languages: [Java](https://github.com/awslabs/amazon-kinesis-video-streams-producer-sdk-java) and [C ++](https://github.com/awslabs/amazon-kinesis-video-streams-producer-sdk-cpp). In this example, we will be using the Producer C++ SDK with Docker.

### Pre-requisite:
- Docker must be installed and configured . Check official website of how to install docker using [Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/) and [Windows](https://docs.docker.com/docker-for-windows/)
- (Windows) Due to the complexity of using the webcam in Windows, you must configure an IP address for your camera to do [RTSP](https://pt.wikipedia.org/wiki/RTSP).

###  Install
- Check Linux or Windows tutorial.

## Setting up project code

### Pre-requisites
1. Clone project
2. AWS Environment Configured
3. Docker Producer SDK configured.
4. Vritualenv configured and with dependencies installed

### Setting it up and running
1. Populate the **.env.example** file according to the AWS data you set up in [the previous steps](#aws-config).
2. Rename the **.env.example** file to **.env**.
3. Run Dockerfile to start producer.
4. Open a terminal in **src/** and run **consumer.py** file.
```console
(env)$ python consumer.py
```
5. If you want to stop all process, just press **Ctrl + Shift + C**.

  
To view the video being streamed in real time, open your Kinesis Video Streams, and to monitor incoming data traffic, open your Kinesis Data Streams.

## Reference
- [Amazon Rekognition Developer Guide](https://docs.aws.amazon.com/rekognition/latest/dg/rekognition-dg.pdf);
- [Instructions for installing Kinesis Video Streams Producer SDK on Linux (Ubuntu, Raspberry PI)](https://github.com/awslabs/amazon-kinesis-video-streams-producer-sdk-cpp/blob/master/install-instructions-linux.md);