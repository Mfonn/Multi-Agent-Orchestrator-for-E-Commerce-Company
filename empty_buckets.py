import boto3

REGION = "us-east-1"
STACK = "udacity-agentcore"

cf = boto3.client("cloudformation", region_name=REGION)
s3 = boto3.resource("s3", region_name=REGION)

resources = cf.list_stack_resources(StackName=STACK)["StackResourceSummaries"]

for r in resources:
    if r["ResourceType"] == "AWS::S3::Bucket" and r["ResourceStatus"] != "DELETE_COMPLETE":
        name = r["PhysicalResourceId"]
        print("Emptying every version in:", name)
        try:
            # Deletes current files, old versions and delete markers
            s3.Bucket(name).object_versions.delete()
            print("  done")
        except Exception as e:
            print("  skipped:", e)