# helix-core-on-aws
This project will deploy a perforce helix core server to AWS.

# How to deploy stack
This guide assumes you have AWS CLI, Node, and Python installed and AWS CLI has been configured for your aws account.

1. Ensure CDK is installed
```
$ npm install -g aws-cdk
```

2. Create a Python virtual environment
```
$ python3 -m venv .venv
```

3. Activate virtual environment

_On MacOS or Linux_
```
$ source .venv/bin/activate
```

_On Windows_
```
% .venv\Scripts\activate.bat
```

4. Install the required dependencies.

```
$ pip install -r requirements.txt
```

5. Create configuration file
```
1. Create a copy of blank-config.py called config.py
2. Edit 'Required Changes' section
```


7. Synthesize (`cdk synth`) or deploy (`cdk deploy`) the stack

```
$ cdk deploy
```

8. Connect to server using p4admin change password and create user accounts

(Connection details can be found on AWS EC2 Console under running instances)
```
Server: ssl:'Public IPv4 DNS Hostname':1666
Username: super
Password: 'EC2 Instance ID' 
```
_Example Login Details_
```
Server: ssl:ec2-10-0-0-1.compute-1.amazonaws.com
Username: super
Password: i-0123456789abcdefg
```
[AWS EC2 Console](https://us-east-1.console.aws.amazon.com/ec2/v2/)

### To dispose of the stack afterwards:

```
$ cdk destroy
```

# Default Cost Estimate
[AWS Cost Calculator](https://calculator.aws/#/estimate?id=7ceb3ca8e571957d53f0821077429235a785bac5)

Cost can be reduced by stopping the ec2 instance in the AWS Console when no one is working and/or by reducing the size of ec2 instance and EBS Storage Volume.