root="$(git rev-parse --show-toplevel)"
echo "$root"
export SETTINGS_PATH="$root/app/prod_config.json"
python3 "$root/app/server.py" run
