## Automate firewall rules for Google GKE autopilot nodes

Google maintains the GKE nodes themselves for autopilot nodes and provides no way for users to create firewall rules to allow their GKE nodes access to any resources on GCP or other resources that typically are protected by google firewall.  

This script will go out every x minutes and check the kube cluster, pull all the IP's look at your firewall rule "autopilot-rules" and look to see if there are any IP's that are missing or outside of the current node IP list and then update the firewall rule with the new IP's if there is a discrepancy. You may need to create the firewall rule for t to update, the rule already existed when I created this script.

There are env settings to customize this, they are rem’d out in the dockerfile as it is better to define the env settings in .env or in a config map.  The Dockerfile expects that your service account json file is in ./serviceaccount.json and will fail if you don’t remove the copy command or update it with the name you used for your creds.  Your service account should have gke admin, gcp instance admin and gcp firewall admin privileges. 

If you are going to run this as a pod in your kube cluster, you must first create the RBAC for this to work or otherwise your container will not be authorized to run kubectl commands, just change the namespace and create the rbac using the provided rbac.yaml file

To use, create the docker container

*Need to pre-statge autopilot-fw rule, doesnt matter the contents they will be overwritten. You can find and replace if you want to change the name of the rule to something else

(sudo) docker build -t google-scripts -f Dockerfile .

Dont forget to set the env settings 

PROJECT=(This is your google project id)
FIREWALL_NAME=(This is the name of the firewall rule)
TARGET_TAG=(this is the destination network tag the rule should target”
CREDENTIALS_FILE=/app/serviceaccount.json (This actually can probably be removed in place of the Google_Application_Credentials)
RUN_INTERVAL=5m (This will check every 5 minutes and update only if needed)
GOOGLE_APPLICATION_CREDENTIALS=/app/serviceaccount.json

I hope this helps save you some time.

