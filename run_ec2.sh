# Helper script for deploying on ec2

# Start ssh agent and add id
eval “$(ssh-agent -s)”
ssh-add ../id_aws

# stop existing server
killall python

# run new server
sudo su

python3 -m pip install -r app/requirements.txt
sh app/scripts/deploy.sh & bg
