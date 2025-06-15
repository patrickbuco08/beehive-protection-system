#!/bin/bash

if [ "$1" = "jupyter" ]; then
  jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token="" --NotebookApp.password=""
else
  echo "Container is running. Connect with 'docker exec -it beehive-protection bash' to execute commands."
  # Keep container running
  tail -f /dev/null
fi
