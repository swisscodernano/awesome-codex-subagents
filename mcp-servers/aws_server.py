#!/usr/bin/env python3
"""
AWS MCP Server for Codex CLI
AWS operations via boto3.
"""
import os
import json
import asyncio
from mcp.server import Server
from mcp.types import Tool, TextContent

# Lazy import boto3 to avoid errors if not installed
boto3 = None

server = Server("aws-mcp")

def get_boto3():
    """Lazy load boto3."""
    global boto3
    if boto3 is None:
        import boto3 as b3
        boto3 = b3
    return boto3

@server.list_tools()
async def list_tools():
    """List available tools."""
    return [
        # EC2
        Tool(
            name="aws_ec2_list",
            description="List EC2 instances",
            inputSchema={
                "type": "object",
                "properties": {
                    "filters": {"type": "array", "description": "Instance filters", "items": {"type": "object"}},
                    "region": {"type": "string", "default": "eu-central-1"}
                }
            }
        ),
        Tool(
            name="aws_ec2_describe",
            description="Describe a specific EC2 instance",
            inputSchema={
                "type": "object",
                "properties": {
                    "instance_id": {"type": "string"},
                    "region": {"type": "string", "default": "eu-central-1"}
                },
                "required": ["instance_id"]
            }
        ),
        # S3
        Tool(
            name="aws_s3_list_buckets",
            description="List S3 buckets",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="aws_s3_list_objects",
            description="List objects in S3 bucket",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket": {"type": "string"},
                    "prefix": {"type": "string", "default": ""},
                    "max_keys": {"type": "integer", "default": 100}
                },
                "required": ["bucket"]
            }
        ),
        # Lambda
        Tool(
            name="aws_lambda_list",
            description="List Lambda functions",
            inputSchema={
                "type": "object",
                "properties": {
                    "region": {"type": "string", "default": "eu-central-1"}
                }
            }
        ),
        Tool(
            name="aws_lambda_get",
            description="Get Lambda function details",
            inputSchema={
                "type": "object",
                "properties": {
                    "function_name": {"type": "string"},
                    "region": {"type": "string", "default": "eu-central-1"}
                },
                "required": ["function_name"]
            }
        ),
        # CloudWatch
        Tool(
            name="aws_cloudwatch_alarms",
            description="List CloudWatch alarms",
            inputSchema={
                "type": "object",
                "properties": {
                    "state": {"type": "string", "enum": ["ALARM", "OK", "INSUFFICIENT_DATA"]},
                    "region": {"type": "string", "default": "eu-central-1"}
                }
            }
        ),
        Tool(
            name="aws_cloudwatch_logs",
            description="Query CloudWatch Logs",
            inputSchema={
                "type": "object",
                "properties": {
                    "log_group": {"type": "string"},
                    "filter_pattern": {"type": "string", "default": ""},
                    "start_time": {"type": "integer", "description": "Unix timestamp in ms"},
                    "limit": {"type": "integer", "default": 50},
                    "region": {"type": "string", "default": "eu-central-1"}
                },
                "required": ["log_group"]
            }
        ),
        # RDS
        Tool(
            name="aws_rds_list",
            description="List RDS instances",
            inputSchema={
                "type": "object",
                "properties": {
                    "region": {"type": "string", "default": "eu-central-1"}
                }
            }
        ),
        # ECS
        Tool(
            name="aws_ecs_clusters",
            description="List ECS clusters",
            inputSchema={
                "type": "object",
                "properties": {
                    "region": {"type": "string", "default": "eu-central-1"}
                }
            }
        ),
        Tool(
            name="aws_ecs_services",
            description="List ECS services in a cluster",
            inputSchema={
                "type": "object",
                "properties": {
                    "cluster": {"type": "string"},
                    "region": {"type": "string", "default": "eu-central-1"}
                },
                "required": ["cluster"]
            }
        ),
        # Cost
        Tool(
            name="aws_cost_today",
            description="Get today's AWS costs",
            inputSchema={"type": "object", "properties": {}}
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list:
    """Execute tool calls."""
    try:
        b3 = get_boto3()
        region = arguments.get("region", "eu-central-1")

        # EC2
        if name == "aws_ec2_list":
            ec2 = b3.client("ec2", region_name=region)
            filters = arguments.get("filters", [])

            response = ec2.describe_instances(Filters=filters) if filters else ec2.describe_instances()

            instances = []
            for reservation in response.get("Reservations", []):
                for instance in reservation.get("Instances", []):
                    name_tag = next((t["Value"] for t in instance.get("Tags", []) if t["Key"] == "Name"), "")
                    instances.append({
                        "id": instance["InstanceId"],
                        "name": name_tag,
                        "type": instance["InstanceType"],
                        "state": instance["State"]["Name"],
                        "private_ip": instance.get("PrivateIpAddress"),
                        "public_ip": instance.get("PublicIpAddress")
                    })

            return [TextContent(type="text", text=json.dumps(instances, indent=2))]

        elif name == "aws_ec2_describe":
            ec2 = b3.client("ec2", region_name=region)
            instance_id = arguments.get("instance_id")

            response = ec2.describe_instances(InstanceIds=[instance_id])
            instance = response["Reservations"][0]["Instances"][0]

            return [TextContent(type="text", text=json.dumps(instance, indent=2, default=str))]

        # S3
        elif name == "aws_s3_list_buckets":
            s3 = b3.client("s3")
            response = s3.list_buckets()

            buckets = [{"name": b["Name"], "created": str(b["CreationDate"])} for b in response.get("Buckets", [])]
            return [TextContent(type="text", text=json.dumps(buckets, indent=2))]

        elif name == "aws_s3_list_objects":
            s3 = b3.client("s3")
            bucket = arguments.get("bucket")
            prefix = arguments.get("prefix", "")
            max_keys = arguments.get("max_keys", 100)

            response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix, MaxKeys=max_keys)

            objects = []
            for obj in response.get("Contents", []):
                objects.append({
                    "key": obj["Key"],
                    "size": obj["Size"],
                    "modified": str(obj["LastModified"])
                })

            return [TextContent(type="text", text=json.dumps({
                "bucket": bucket,
                "prefix": prefix,
                "count": len(objects),
                "objects": objects
            }, indent=2))]

        # Lambda
        elif name == "aws_lambda_list":
            lam = b3.client("lambda", region_name=region)
            response = lam.list_functions()

            functions = []
            for f in response.get("Functions", []):
                functions.append({
                    "name": f["FunctionName"],
                    "runtime": f.get("Runtime"),
                    "memory": f["MemorySize"],
                    "timeout": f["Timeout"],
                    "modified": f["LastModified"]
                })

            return [TextContent(type="text", text=json.dumps(functions, indent=2))]

        elif name == "aws_lambda_get":
            lam = b3.client("lambda", region_name=region)
            function_name = arguments.get("function_name")

            response = lam.get_function(FunctionName=function_name)
            return [TextContent(type="text", text=json.dumps(response, indent=2, default=str))]

        # CloudWatch
        elif name == "aws_cloudwatch_alarms":
            cw = b3.client("cloudwatch", region_name=region)
            state = arguments.get("state")

            if state:
                response = cw.describe_alarms(StateValue=state)
            else:
                response = cw.describe_alarms()

            alarms = []
            for alarm in response.get("MetricAlarms", []):
                alarms.append({
                    "name": alarm["AlarmName"],
                    "state": alarm["StateValue"],
                    "metric": alarm["MetricName"],
                    "namespace": alarm["Namespace"],
                    "reason": alarm.get("StateReason", "")[:100]
                })

            return [TextContent(type="text", text=json.dumps(alarms, indent=2))]

        elif name == "aws_cloudwatch_logs":
            logs = b3.client("logs", region_name=region)
            log_group = arguments.get("log_group")
            filter_pattern = arguments.get("filter_pattern", "")
            limit = arguments.get("limit", 50)

            import time
            start_time = arguments.get("start_time", int((time.time() - 3600) * 1000))  # Last hour

            response = logs.filter_log_events(
                logGroupName=log_group,
                filterPattern=filter_pattern,
                startTime=start_time,
                limit=limit
            )

            events = []
            for event in response.get("events", []):
                events.append({
                    "timestamp": event["timestamp"],
                    "message": event["message"][:500]
                })

            return [TextContent(type="text", text=json.dumps(events, indent=2))]

        # RDS
        elif name == "aws_rds_list":
            rds = b3.client("rds", region_name=region)
            response = rds.describe_db_instances()

            instances = []
            for db in response.get("DBInstances", []):
                instances.append({
                    "id": db["DBInstanceIdentifier"],
                    "engine": db["Engine"],
                    "class": db["DBInstanceClass"],
                    "status": db["DBInstanceStatus"],
                    "endpoint": db.get("Endpoint", {}).get("Address")
                })

            return [TextContent(type="text", text=json.dumps(instances, indent=2))]

        # ECS
        elif name == "aws_ecs_clusters":
            ecs = b3.client("ecs", region_name=region)
            response = ecs.list_clusters()

            clusters = response.get("clusterArns", [])
            return [TextContent(type="text", text=json.dumps(clusters, indent=2))]

        elif name == "aws_ecs_services":
            ecs = b3.client("ecs", region_name=region)
            cluster = arguments.get("cluster")

            response = ecs.list_services(cluster=cluster)
            services = response.get("serviceArns", [])

            # Get service details
            if services:
                details = ecs.describe_services(cluster=cluster, services=services[:10])
                service_info = []
                for svc in details.get("services", []):
                    service_info.append({
                        "name": svc["serviceName"],
                        "status": svc["status"],
                        "desired": svc["desiredCount"],
                        "running": svc["runningCount"]
                    })
                return [TextContent(type="text", text=json.dumps(service_info, indent=2))]

            return [TextContent(type="text", text="No services found")]

        # Cost
        elif name == "aws_cost_today":
            ce = b3.client("ce", region_name="us-east-1")  # Cost Explorer is global
            from datetime import date, timedelta

            today = date.today()
            start = today.strftime("%Y-%m-%d")
            end = (today + timedelta(days=1)).strftime("%Y-%m-%d")

            response = ce.get_cost_and_usage(
                TimePeriod={"Start": start, "End": end},
                Granularity="DAILY",
                Metrics=["UnblendedCost"]
            )

            results = response.get("ResultsByTime", [])
            if results:
                cost = results[0].get("Total", {}).get("UnblendedCost", {})
                return [TextContent(type="text", text=json.dumps({
                    "date": start,
                    "cost": cost.get("Amount"),
                    "unit": cost.get("Unit")
                }, indent=2))]

            return [TextContent(type="text", text="No cost data available")]

        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

    except ImportError:
        return [TextContent(type="text", text="Error: boto3 not installed. Run: pip install boto3")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]

if __name__ == "__main__":
    from mcp.server.stdio import stdio_server

    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())

    asyncio.run(main())
