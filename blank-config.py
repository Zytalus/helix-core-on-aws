# Required Changes
# replace insert-project-name with your project name *DO NOT CHANGE NAME AFTER CDK DEPLOY*
project_name = "insert-project-name-here"

# replace ipv4 addresses with those that need access to helix core server
allowed_list = ["0.0.0.0",
                "255.255.255.255"
                ]

# Optional Changes
# set project storage size in gb (approx. $1 per month per 10gb)
project_size = 200
# set helix core instance type
instance_type = "c5.large"