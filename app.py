import os.path
import config

from aws_cdk.aws_s3_assets import Asset

from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    App, Stack
)

from constructs import Construct

dirname = os.path.dirname(__file__)


class GameStudioStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # VPC
        vpc = ec2.Vpc(self, (config.project_name + "-VPC"),
                      nat_gateways=0,
                      subnet_configuration=[ec2.SubnetConfiguration(name="public", subnet_type=ec2.SubnetType.PUBLIC)]
                      )

        # AMI
        amzn_linux = ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            virtualization=ec2.AmazonLinuxVirt.HVM,
            storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
        )

        # Instance Role and SSM Managed Policy
        role = iam.Role(self, config.project_name + "SSM", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))

        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))

        # Security Group
        helix_sg = ec2.SecurityGroup(self, "helix-core-SG",
                                     vpc=vpc
                                     )
        for a in config.allowed_list:
            helix_sg.add_ingress_rule(ec2.Peer.ipv4(a + '/32'), ec2.Port.tcp(1666),
                                      "allow access to helix core server")

        # Instance
        instance = ec2.Instance(self, (config.project_name + "-helix-core"),
                                instance_type=ec2.InstanceType(config.instance_type),
                                machine_image=amzn_linux,
                                security_group=helix_sg,
                                vpc=vpc,
                                role=role,
                                block_devices=[ec2.BlockDevice(
                                    device_name="/dev/sdb",
                                    volume=ec2.BlockDeviceVolume.ebs(config.project_size)
                                )
                                ]
                                )

        # Script in S3 as Asset
        asset = Asset(self, "Asset", path=os.path.join(dirname, "configure.sh"))
        local_path = instance.user_data.add_s3_download_command(
            bucket=asset.bucket,
            bucket_key=asset.s3_object_key
        )

        # Userdata executes script from S3
        instance.user_data.add_execute_file_command(
            file_path=local_path
        )
        asset.grant_read(instance.role)


app = App()
GameStudioStack(app, "GameStudio")

app.synth()
