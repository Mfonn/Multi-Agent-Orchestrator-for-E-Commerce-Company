#!/bin/bash
STACK=udacity-agentcore
REGION=us-east-1

echo "Buckets in the old stack:"
BUCKETS=$(aws cloudformation list-stack-resources --stack-name $STACK --region $REGION \
  --query "StackResourceSummaries[?ResourceType=='AWS::S3::Bucket'].PhysicalResourceId" --output text)
echo "$BUCKETS"

for b in $BUCKETS; do
  echo "Emptying $b ..."
  aws s3 rm "s3://$b" --recursive
done

echo "Deleting the old stack (this takes a few minutes)..."
aws cloudformation delete-stack --stack-name $STACK --region $REGION
aws cloudformation wait stack-delete-complete --stack-name $STACK --region $REGION \
  && echo "Old stack deleted." \
  || aws cloudformation describe-stack-events --stack-name $STACK --region $REGION \
       --query "StackEvents[?ResourceStatus=='DELETE_FAILED'].[LogicalResourceId,ResourceStatusReason]" --output table