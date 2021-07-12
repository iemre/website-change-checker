#!/bin/bash

set -u

wait_seconds_after_nav=10

# get new screenshots
while read -r url_conf; do
  url=`echo $url_conf | cut -d' ' -f1`
  l_offset=`echo $url_conf | cut -d' ' -f2`
  t_offset=`echo $url_conf | cut -d' ' -f3`
  r_offset=`echo $url_conf | cut -d' ' -f4`
  b_offset=`echo $url_conf | cut -d' ' -f5`

  h=`echo $url | md5sum | awk '{ print $1 }'`
  dir="ss_$h"
  old_dir="${dir}_old"
  mkdir -p $dir
  mkdir -p $old_dir
  cp $dir/* $old_dir/  

  # this Docker container creates a `screenshot/` folder in the current directory and downloads a screenshot of the given website
  docker run -v $(pwd):/data leonjza/gowitness gowitness single --screenshot-path $dir --delay $wait_seconds_after_nav --user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36" "$url"

  # find if there is any change in one of the websites in urls.txt
  result="$(python3 check_image_diff.py $dir $l_offset $t_offset $r_offset $b_offset)"

  if [ -z "$result" ]
  then
    echo "no change"
  else
    curl -H "Content-Type: application/json" -d "{\"username\": \"test\", \"content\": \"$url\"}" "${DISCORD_WEBHOOK}"
  fi
done < urls.txt


