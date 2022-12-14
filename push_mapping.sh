mkdir --parents "$HOME/.ssh"
DEPLOY_KEY_FILE="$HOME/.ssh/deploy_key"
echo "$1" > "$DEPLOY_KEY_FILE"
chmod 600 "$DEPLOY_KEY_FILE"
SSH_KNOWN_HOSTS_FILE="$HOME/.ssh/known_hosts"
ssh-keyscan -H "github.com" > "$SSH_KNOWN_HOSTS_FILE"
export GIT_SSH_COMMAND="ssh -i "$DEPLOY_KEY_FILE" -o UserKnownHostsFile=$SSH_KNOWN_HOSTS_FILE"
echo "Hello!"
git clone -b master git@github.com:unifyai/Mapping.git --depth 1