import subprocess
import os
import socket
import tempfile
import time
import yaml
import re
import logging

from typing import Dict, List, Optional, Union
from .controller_manager import ControllerManager
from .utils.port_forwarding import PortForwardProcessManager

class JupyterPod(ControllerManager):
    
    def __init__(
        self, 
        container_spec: Dict,
        local_port: int = 8888,
        remote_port: int = 8888,
        context: Optional[str] = None,
        kubectl_path: Optional[str] = None,
        debug_mode: bool = False,
        token: Optional[str] = None,
        password: Optional[str] = None,
        cpu: Optional[str] = None,
        memory: Optional[str] = None,
        gpu: Optional[str] = None
    ):
        """
        Initialize a JupyterPod instance for managing Jupyter notebooks in Kubernetes.

        Args:
            container_spec (Dict): Specification for the Jupyter container, including image and volumes
            local_port (int, optional): Local port to forward Jupyter to. Defaults to 8888.
            remote_port (int, optional): Port Jupyter runs on in the container. Defaults to 8888.
            context (str, optional): Kubernetes context to use. Defaults to current context.
            kubectl_path (str, optional): Path to kubectl binary. Defaults to system kubectl.
            debug_mode (bool, optional): Enable debug logging. Defaults to False.
            token (str, optional): Jupyter authentication token. If None, no token is set.
            password (str, optional): Jupyter authentication password. If None, no password is set.
            cpu (str, optional): CPU resource specification (e.g., "1", "500m"). Defaults to None.
            memory (str, optional): Memory resource specification (e.g., "1Gi", "512Mi"). Defaults to None.
            gpu (str, optional): GPU resource specification (e.g., "1"). Defaults to None.
        """
        self.local_port = local_port
        self.remote_port = remote_port
        self.token = token
        self.password = password
        
        # Build the manifest from the container spec
        manifest = self._build_controller_manifest(container_spec, cpu, memory, gpu)
        
        super().__init__(
            manifest=manifest,
            context=context,
            kubectl_path=kubectl_path,
            debug_mode=debug_mode
        )

        self.port_forward_manager = PortForwardProcessManager(
            local_port=self.local_port,
            pod_port=self.remote_port,
            pod_name=self.name,
            namespace=self.namespace,
            context=self.context,
            logger=self.logger
        )

#--------------------------------------------------------------------------------
# Controller Lifecycle Methods
#--------------------------------------------------------------------------------
    def start_notebook(self):
        """
        Start the Jupyter notebook pod and set up port forwarding.
        """
        self.logger.info("Starting Jupyter notebook pod")
        self.start_controller()
        self._setup_port_forwarding()
        self.print_url()

    def stop_notebook(self):
        """
        Stop the Jupyter notebook pod and clean up port forwarding.
        """
        self.logger.info("Stopping Jupyter notebook pod")
        self._stop_port_forwarding()
        self.stop_controller()

#--------------------------------------------------------------------------------
# Port Forwarding Methods
#--------------------------------------------------------------------------------

    def _build_controller_manifest(self, container_spec: Dict, cpu: Optional[str], memory: Optional[str], gpu: Optional[str]) -> Dict:
        """
        Build a Deployment manifest from the container specification.
        
        Args:
            container_spec (Dict): The container specification
            cpu (str, optional): CPU resource specification
            memory (str, optional): Memory resource specification
            gpu (str, optional): GPU resource specification
            
        Returns:
            Dict: The Kubernetes Deployment manifest
        """
        # Create a copy of the container spec to avoid modifying the original
        container_spec = container_spec.copy()
        
        # Remove any invalid security context fields
        if "securityContext" in container_spec:
            security_context = container_spec["securityContext"]
            if "fsGroup" in security_context:
                del security_context["fsGroup"]
            if not security_context:  # If securityContext is now empty, remove it
                del container_spec["securityContext"]
        
        # Ensure container has a name
        if "name" not in container_spec:
            container_spec["name"] = "jupyter"
        
        # Add port if not specified
        if "ports" not in container_spec:
            container_spec["ports"] = [{"containerPort": self.remote_port}]
        
        # Add Jupyter command if not specified
        if "command" not in container_spec:
            command = ["start-notebook.sh", f"--port={self.remote_port}"]
            if self.token is not None:
                command.append(f"--NotebookApp.token='{self.token}'")
            else:
                command.append("--NotebookApp.token=''")
            
            if self.password is not None:
                command.append(f"--NotebookApp.password='{self.password}'")
            else:
                command.append("--NotebookApp.password=''")
            
            container_spec["command"] = command
        
        # Set up resources
        resources = {}
        if cpu or memory:
            resources["requests"] = {}
            resources["limits"] = {}
            if cpu:
                resources["requests"]["cpu"] = cpu
                resources["limits"]["cpu"] = cpu
            if memory:
                resources["requests"]["memory"] = memory
                resources["limits"]["memory"] = memory
            if gpu:
                resources["requests"]["nvidia.com/gpu"] = gpu
                resources["limits"]["nvidia.com/gpu"] = gpu
        
        if resources:
            container_spec["resources"] = resources

        # Extract volumes and volumeMounts from container spec
        volumes = container_spec.pop("volumes", [])
        volume_mounts = container_spec.pop("volumeMounts", [])
        init_containers = container_spec.pop("initContainers", [])

        # Ensure all volumeMounts have corresponding volumes
        for mount in volume_mounts:
            mount_name = mount["name"]
            if not any(v["name"] == mount_name for v in volumes):
                # If no matching volume is found, create a default one
                volumes.append({
                    "name": mount_name,
                    "persistentVolumeClaim": {
                        "claimName": "mdsmlvol"  # Use your default PVC name
                    }
                })

        # Create the Deployment manifest
        manifest = {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "name": f"jupyter-notebook-{int(time.time())}",
                "labels": {
                    "app": "jupyter-notebook"
                }
            },
            "spec": {
                "replicas": 1,
                "selector": {
                    "matchLabels": {
                        "app": "jupyter-notebook"
                    }
                },
                "template": {
                    "metadata": {
                        "labels": {
                            "app": "jupyter-notebook"
                        }
                    },
                    "spec": {
                        "initContainers": init_containers,  # Add initContainers
                        "containers": [{
                            **container_spec,
                            "volumeMounts": volume_mounts
                        }],
                        "volumes": volumes,
                        "restartPolicy": "Always"
                    }
                }
            }
        }

        return manifest

    def _setup_port_forwarding(self):
        """
        Set up port forwarding from the pod to the local machine using PortForwardProcessManager.
        """
        self.logger.info(f"Setting up port forwarding from local port {self.local_port} to pod port {self.remote_port}")
        
        # Attempt port forwarding
        if not self.port_forward_manager._attempt_port_forwarding():
            raise RuntimeError("Failed to establish port forwarding")

    def _stop_port_forwarding(self):
        """
        Stop the port forwarding process.
        """
        if self.port_forward_manager:
            self.logger.info("Stopping port forwarding")
            self.port_forward_manager._stop_port_forward()
            self.port_forward_manager = None

#--------------------------------------------------------------------------------
# Management and Logging Methods
#--------------------------------------------------------------------------------

    def print_url(self):
        """
        Print the URL to access the Jupyter notebook.
        """
        url = f"http://localhost:{self.local_port}"
        self.logger.info(f"Jupyter notebook is available at: {url}")
        print(f"\nJupyter notebook is available at: {url}")
        print("Press Ctrl+C to stop the notebook when you're done.")
