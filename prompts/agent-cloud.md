# /agent-cloud

Expert cloud architect for AWS/GCP/Azure.

## AWS CLI
```bash
# EC2
aws ec2 describe-instances --filters "Name=tag:Name,Values=prod-*"
aws ec2 start-instances --instance-ids i-1234567890abcdef0

# S3
aws s3 ls s3://bucket/
aws s3 sync ./local s3://bucket/path

# Lambda
aws lambda invoke --function-name myFunc output.json

# CloudWatch
aws logs tail /aws/lambda/myFunc --follow
```

## GCP
```bash
gcloud compute instances list
gcloud run deploy --image gcr.io/project/app
gcloud functions deploy myFunc --runtime python39
```

## Azure
```bash
az vm list
az webapp deploy --name myapp --src-path app.zip
az functionapp deployment source config-zip -g rg -n func --src func.zip
```

## Cost Optimization
```
- Right-size instances
- Use reserved/spot instances
- Enable auto-scaling
- Delete unused resources
- Use S3 lifecycle policies
- Monitor with Cost Explorer
```
