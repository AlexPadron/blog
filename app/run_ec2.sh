# Helper script for deploying on ec2

# Start ssh agent and add id
eval "$(ssh-agent -s)"
ssh-add ../../id_aws

# stop existing server
killall python3
echo "Done stopping old server"

# Run new server
sudo python3 -m pip install -r requirements.txt
sudo sh scripts/deploy.sh & bg
