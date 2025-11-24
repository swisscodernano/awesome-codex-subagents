#!/usr/bin/env python3
"""
Kubernetes MCP Server for Codex CLI
K8s operations via kubectl.
"""
import os
import json
import asyncio
import subprocess
from mcp.server import Server
from mcp.types import Tool, TextContent

# Configuration
KUBECONFIG = os.getenv("KUBECONFIG", "~/.kube/config")
DEFAULT_NAMESPACE = os.getenv("K8S_NAMESPACE", "default")
READONLY = os.getenv("MCP_K8S_READONLY", "true").lower() == "true"

server = Server("kubernetes-mcp")

def run_kubectl(args: list, timeout: int = 30) -> tuple[str, int]:
    """Run kubectl command."""
    try:
        env = os.environ.copy()
        env["KUBECONFIG"] = os.path.expanduser(KUBECONFIG)

        result = subprocess.run(
            ["kubectl"] + args,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env
        )
        return result.stdout or result.stderr, result.returncode
    except FileNotFoundError:
        return "kubectl not found in PATH", 1
    except Exception as e:
        return str(e), 1

@server.list_tools()
async def list_tools():
    """List available tools."""
    tools = [
        # Core resources
        Tool(
            name="k8s_get_pods",
            description="List pods in a namespace",
            inputSchema={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string", "default": DEFAULT_NAMESPACE},
                    "selector": {"type": "string", "description": "Label selector (e.g., 'app=nginx')"},
                    "all_namespaces": {"type": "boolean", "default": False}
                }
            }
        ),
        Tool(
            name="k8s_get_deployments",
            description="List deployments",
            inputSchema={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string", "default": DEFAULT_NAMESPACE},
                    "all_namespaces": {"type": "boolean", "default": False}
                }
            }
        ),
        Tool(
            name="k8s_get_services",
            description="List services",
            inputSchema={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string", "default": DEFAULT_NAMESPACE},
                    "all_namespaces": {"type": "boolean", "default": False}
                }
            }
        ),
        Tool(
            name="k8s_get_nodes",
            description="List cluster nodes",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="k8s_get_namespaces",
            description="List namespaces",
            inputSchema={"type": "object", "properties": {}}
        ),
        # Detailed info
        Tool(
            name="k8s_describe",
            description="Describe a resource",
            inputSchema={
                "type": "object",
                "properties": {
                    "resource_type": {"type": "string", "description": "Resource type (pod, deployment, service, etc.)"},
                    "name": {"type": "string"},
                    "namespace": {"type": "string", "default": DEFAULT_NAMESPACE}
                },
                "required": ["resource_type", "name"]
            }
        ),
        Tool(
            name="k8s_logs",
            description="Get pod logs",
            inputSchema={
                "type": "object",
                "properties": {
                    "pod": {"type": "string"},
                    "namespace": {"type": "string", "default": DEFAULT_NAMESPACE},
                    "container": {"type": "string", "description": "Container name (if multiple)"},
                    "tail": {"type": "integer", "default": 100},
                    "previous": {"type": "boolean", "default": False}
                },
                "required": ["pod"]
            }
        ),
        Tool(
            name="k8s_events",
            description="Get cluster events",
            inputSchema={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string", "default": DEFAULT_NAMESPACE},
                    "all_namespaces": {"type": "boolean", "default": False}
                }
            }
        ),
        # Cluster info
        Tool(
            name="k8s_cluster_info",
            description="Get cluster info",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="k8s_top_pods",
            description="Show pod resource usage",
            inputSchema={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string", "default": DEFAULT_NAMESPACE},
                    "all_namespaces": {"type": "boolean", "default": False}
                }
            }
        ),
        Tool(
            name="k8s_top_nodes",
            description="Show node resource usage",
            inputSchema={"type": "object", "properties": {}}
        ),
        # ConfigMaps and Secrets
        Tool(
            name="k8s_get_configmaps",
            description="List configmaps",
            inputSchema={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string", "default": DEFAULT_NAMESPACE}
                }
            }
        ),
        Tool(
            name="k8s_get_secrets",
            description="List secrets (names only, no data)",
            inputSchema={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string", "default": DEFAULT_NAMESPACE}
                }
            }
        ),
        # Ingress
        Tool(
            name="k8s_get_ingresses",
            description="List ingresses",
            inputSchema={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string", "default": DEFAULT_NAMESPACE},
                    "all_namespaces": {"type": "boolean", "default": False}
                }
            }
        ),
        # Raw get
        Tool(
            name="k8s_get",
            description="Get any resource type",
            inputSchema={
                "type": "object",
                "properties": {
                    "resource": {"type": "string", "description": "Resource type (e.g., pods, deployments, statefulsets)"},
                    "name": {"type": "string", "description": "Resource name (optional)"},
                    "namespace": {"type": "string", "default": DEFAULT_NAMESPACE},
                    "output": {"type": "string", "enum": ["json", "yaml", "wide"], "default": "json"}
                },
                "required": ["resource"]
            }
        )
    ]

    if not READONLY:
        tools.extend([
            Tool(
                name="k8s_scale",
                description="Scale a deployment",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "deployment": {"type": "string"},
                        "replicas": {"type": "integer"},
                        "namespace": {"type": "string", "default": DEFAULT_NAMESPACE}
                    },
                    "required": ["deployment", "replicas"]
                }
            ),
            Tool(
                name="k8s_restart",
                description="Restart a deployment (rollout restart)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "deployment": {"type": "string"},
                        "namespace": {"type": "string", "default": DEFAULT_NAMESPACE}
                    },
                    "required": ["deployment"]
                }
            ),
            Tool(
                name="k8s_delete_pod",
                description="Delete a pod (will be recreated by controller)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "pod": {"type": "string"},
                        "namespace": {"type": "string", "default": DEFAULT_NAMESPACE}
                    },
                    "required": ["pod"]
                }
            )
        ])

    return tools

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list:
    """Execute tool calls."""
    try:
        namespace = arguments.get("namespace", DEFAULT_NAMESPACE)
        all_ns = arguments.get("all_namespaces", False)
        ns_args = ["-A"] if all_ns else ["-n", namespace]

        if name == "k8s_get_pods":
            selector = arguments.get("selector")
            args = ["get", "pods"] + ns_args + ["-o", "json"]
            if selector:
                args.extend(["-l", selector])

            output, code = run_kubectl(args)
            if code != 0:
                return [TextContent(type="text", text=f"Error: {output}")]

            data = json.loads(output)
            pods = []
            for pod in data.get("items", []):
                pods.append({
                    "name": pod["metadata"]["name"],
                    "namespace": pod["metadata"]["namespace"],
                    "status": pod["status"]["phase"],
                    "ready": f"{sum(1 for c in pod['status'].get('containerStatuses', []) if c.get('ready'))}/{len(pod['spec']['containers'])}",
                    "restarts": sum(c.get("restartCount", 0) for c in pod["status"].get("containerStatuses", [])),
                    "node": pod["spec"].get("nodeName", "")
                })

            return [TextContent(type="text", text=json.dumps(pods, indent=2))]

        elif name == "k8s_get_deployments":
            args = ["get", "deployments"] + ns_args + ["-o", "json"]
            output, code = run_kubectl(args)

            if code != 0:
                return [TextContent(type="text", text=f"Error: {output}")]

            data = json.loads(output)
            deps = []
            for dep in data.get("items", []):
                deps.append({
                    "name": dep["metadata"]["name"],
                    "namespace": dep["metadata"]["namespace"],
                    "ready": f"{dep['status'].get('readyReplicas', 0)}/{dep['spec']['replicas']}",
                    "up_to_date": dep["status"].get("updatedReplicas", 0),
                    "available": dep["status"].get("availableReplicas", 0)
                })

            return [TextContent(type="text", text=json.dumps(deps, indent=2))]

        elif name == "k8s_get_services":
            args = ["get", "services"] + ns_args + ["-o", "json"]
            output, code = run_kubectl(args)

            if code != 0:
                return [TextContent(type="text", text=f"Error: {output}")]

            data = json.loads(output)
            svcs = []
            for svc in data.get("items", []):
                svcs.append({
                    "name": svc["metadata"]["name"],
                    "namespace": svc["metadata"]["namespace"],
                    "type": svc["spec"]["type"],
                    "cluster_ip": svc["spec"].get("clusterIP"),
                    "ports": [f"{p.get('port')}/{p.get('protocol')}" for p in svc["spec"].get("ports", [])]
                })

            return [TextContent(type="text", text=json.dumps(svcs, indent=2))]

        elif name == "k8s_get_nodes":
            output, code = run_kubectl(["get", "nodes", "-o", "json"])

            if code != 0:
                return [TextContent(type="text", text=f"Error: {output}")]

            data = json.loads(output)
            nodes = []
            for node in data.get("items", []):
                conditions = {c["type"]: c["status"] for c in node["status"].get("conditions", [])}
                nodes.append({
                    "name": node["metadata"]["name"],
                    "status": "Ready" if conditions.get("Ready") == "True" else "NotReady",
                    "roles": ",".join(k.replace("node-role.kubernetes.io/", "") for k in node["metadata"].get("labels", {}) if k.startswith("node-role")),
                    "version": node["status"]["nodeInfo"]["kubeletVersion"],
                    "os": node["status"]["nodeInfo"]["osImage"]
                })

            return [TextContent(type="text", text=json.dumps(nodes, indent=2))]

        elif name == "k8s_get_namespaces":
            output, code = run_kubectl(["get", "namespaces", "-o", "json"])

            if code != 0:
                return [TextContent(type="text", text=f"Error: {output}")]

            data = json.loads(output)
            namespaces = [ns["metadata"]["name"] for ns in data.get("items", [])]

            return [TextContent(type="text", text=json.dumps(namespaces, indent=2))]

        elif name == "k8s_describe":
            resource_type = arguments.get("resource_type")
            name_arg = arguments.get("name")

            output, code = run_kubectl(["describe", resource_type, name_arg, "-n", namespace])
            return [TextContent(type="text", text=output[:10000])]

        elif name == "k8s_logs":
            pod = arguments.get("pod")
            container = arguments.get("container")
            tail = arguments.get("tail", 100)
            previous = arguments.get("previous", False)

            args = ["logs", pod, "-n", namespace, "--tail", str(tail)]
            if container:
                args.extend(["-c", container])
            if previous:
                args.append("--previous")

            output, code = run_kubectl(args, timeout=60)
            return [TextContent(type="text", text=output[:20000])]

        elif name == "k8s_events":
            args = ["get", "events"] + ns_args + ["--sort-by=.lastTimestamp", "-o", "json"]
            output, code = run_kubectl(args)

            if code != 0:
                return [TextContent(type="text", text=f"Error: {output}")]

            data = json.loads(output)
            events = []
            for event in data.get("items", [])[-50:]:  # Last 50
                events.append({
                    "type": event.get("type"),
                    "reason": event.get("reason"),
                    "object": f"{event['involvedObject'].get('kind')}/{event['involvedObject'].get('name')}",
                    "message": event.get("message", "")[:200],
                    "count": event.get("count"),
                    "last_seen": event.get("lastTimestamp")
                })

            return [TextContent(type="text", text=json.dumps(events, indent=2))]

        elif name == "k8s_cluster_info":
            output, code = run_kubectl(["cluster-info"])
            return [TextContent(type="text", text=output)]

        elif name == "k8s_top_pods":
            args = ["top", "pods"] + ns_args
            output, code = run_kubectl(args)
            return [TextContent(type="text", text=output)]

        elif name == "k8s_top_nodes":
            output, code = run_kubectl(["top", "nodes"])
            return [TextContent(type="text", text=output)]

        elif name == "k8s_get_configmaps":
            output, code = run_kubectl(["get", "configmaps", "-n", namespace, "-o", "json"])

            if code != 0:
                return [TextContent(type="text", text=f"Error: {output}")]

            data = json.loads(output)
            cms = [{"name": cm["metadata"]["name"], "keys": list(cm.get("data", {}).keys())} for cm in data.get("items", [])]

            return [TextContent(type="text", text=json.dumps(cms, indent=2))]

        elif name == "k8s_get_secrets":
            output, code = run_kubectl(["get", "secrets", "-n", namespace, "-o", "json"])

            if code != 0:
                return [TextContent(type="text", text=f"Error: {output}")]

            data = json.loads(output)
            # Only show names, not data!
            secrets = [{"name": s["metadata"]["name"], "type": s["type"]} for s in data.get("items", [])]

            return [TextContent(type="text", text=json.dumps(secrets, indent=2))]

        elif name == "k8s_get_ingresses":
            args = ["get", "ingresses"] + ns_args + ["-o", "json"]
            output, code = run_kubectl(args)

            if code != 0:
                return [TextContent(type="text", text=f"Error: {output}")]

            data = json.loads(output)
            ingresses = []
            for ing in data.get("items", []):
                ingresses.append({
                    "name": ing["metadata"]["name"],
                    "namespace": ing["metadata"]["namespace"],
                    "hosts": [r.get("host") for r in ing["spec"].get("rules", [])],
                    "address": [lb.get("ip") or lb.get("hostname") for lb in ing["status"].get("loadBalancer", {}).get("ingress", [])]
                })

            return [TextContent(type="text", text=json.dumps(ingresses, indent=2))]

        elif name == "k8s_get":
            resource = arguments.get("resource")
            name_arg = arguments.get("name", "")
            output_format = arguments.get("output", "json")

            args = ["get", resource]
            if name_arg:
                args.append(name_arg)
            args.extend(["-n", namespace, "-o", output_format])

            output, code = run_kubectl(args)
            return [TextContent(type="text", text=output[:15000])]

        # Write operations
        elif name == "k8s_scale" and not READONLY:
            deployment = arguments.get("deployment")
            replicas = arguments.get("replicas")

            output, code = run_kubectl(["scale", "deployment", deployment, f"--replicas={replicas}", "-n", namespace])
            return [TextContent(type="text", text=output if code == 0 else f"Error: {output}")]

        elif name == "k8s_restart" and not READONLY:
            deployment = arguments.get("deployment")

            output, code = run_kubectl(["rollout", "restart", "deployment", deployment, "-n", namespace])
            return [TextContent(type="text", text=output if code == 0 else f"Error: {output}")]

        elif name == "k8s_delete_pod" and not READONLY:
            pod = arguments.get("pod")

            output, code = run_kubectl(["delete", "pod", pod, "-n", namespace])
            return [TextContent(type="text", text=output if code == 0 else f"Error: {output}")]

        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

    except json.JSONDecodeError as e:
        return [TextContent(type="text", text=f"JSON parse error: {str(e)}\nRaw output: {output[:500]}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]

if __name__ == "__main__":
    from mcp.server.stdio import stdio_server

    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())

    asyncio.run(main())
