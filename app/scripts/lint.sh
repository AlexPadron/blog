find "$(git rev-parse --show-toplevel)" -name "*.py" -print0 | xargs -0 pylint --rcfile .pylintrc 2>&1
