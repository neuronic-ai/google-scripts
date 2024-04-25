import subprocess
import os
import googleapiclient.discovery
from googleapiclient.errors import HttpError
import time

def get_node_ips():
    """Run kubectl to get node external IPs."""
    try:
        cmd = "kubectl get nodes -o=jsonpath='{.items[*].status.addresses[?(@.type==\"ExternalIP\")].address}'"
        result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip().split()
    except subprocess.CalledProcessError as e:
        print(f"Error running kubectl: {e.stderr}")
        return None

def update_firewall_rules():
    project = os.getenv('PROJECT')
    firewall_name = os.getenv('FIREWALL_NAME')
    target_tag = os.getenv('TARGET_TAG')
    credentials_file = os.getenv('CREDENTIALS_FILE')

    compute = googleapiclient.discovery.build('compute', 'v1')

    try:
        # Fetch current firewall rule
        current_firewall_rule = compute.firewalls().get(project=project, firewall=firewall_name).execute()
        current_source_ranges = set(current_firewall_rule.get('sourceRanges', []))

        # Get node IPs using kubectl
        node_ips = set(get_node_ips())
        if node_ips is None:
            return "Failed to retrieve node IPs."

        # Only update if there are changes in the IPs
        if node_ips != current_source_ranges:
            firewall_body = {
                "sourceRanges": list(node_ips),
                "targetTags": [target_tag],
                "allowed": [
                    {"IPProtocol": "tcp", "ports": ["2049", "111"]},
                    {"IPProtocol": "udp", "ports": ["2049", "111"]}
                ]
            }
            compute.firewalls().update(
                project=project, firewall=firewall_name, body=firewall_body).execute()
            return "Firewall rules updated"
        else:
            return "No update required; node IPs are unchanged."

    except HttpError as error:
        print(f'An error occurred: {error}')
        return f'Failed to update firewall rules: {error}'


if __name__ == "__main__":
    # Run the script continuously
    while True:
        result = update_firewall_rules()
        print(result)
        time.sleep(300)  # Sleep for 5 minutes (300 seconds)

