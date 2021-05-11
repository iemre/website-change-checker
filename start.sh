#!/bin/bash

set -u

# update old screenshots
cp screenshots/* oldscreenshots/

wait_seconds_after_nav=5

# get new screenshots
while read -r url; do
  # this Docker container creates a `screenshot/` folder in the current directory and downloads a screenshot of the given website
  docker run --rm -v $(pwd):/data leonjza/gowitness gowitness single --delay $wait_seconds_after_nav --user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36" "$url"
done < urls.txt

# find if there is any change in one of the websites in urls.txt
result="$(python3 check_image_diff.py)"

if [ -z "$result" ]
then
  echo "no change"
else
  curl -H "Content-Type: application/json" -d "{\"username\": \"test\", \"content\": \"$result\"}" "${DISCORD_WEBHOOK}"
fi

