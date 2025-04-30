#!/bin/bash

# belirtilen her bir path için git check-ignore komutunu çalıştırır
# ve her bir path için sonucu çıkışa yazar

set -e

# check if any path is specified
if [ $# -eq 0 ]; then
    echo "no path(s) specified" >&2
    exit 1
fi

exit_statuses=()
for f in "$@"; do
    set +e
    git check-ignore "$f" >/dev/null
    exit_status=$?
    set -e

    exit_statuses+=("$exit_status")
    if [ $exit_status -ne 0 ] && [ $exit_status -ne 1 ]; then
        exit 1
    fi
done

#print statuses
for status in "${exit_statuses[@]}"; do
    echo "$status"
done
