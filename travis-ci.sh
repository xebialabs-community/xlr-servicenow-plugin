#!/bin/bash

set -e

mkdir -p ~/xl-licenses
http --check-status --print=b --auth $username:$password --json POST https://download.xebialabs.com/api/temporary/xl-release firstName=xlc lastName=xlc email=xlc@xebialabs.com company=xebialabs | jq --raw-output '.license' > ~/xl-licenses/xl-release-license.lic
./gradlew clean assemble
export plugin_jar=$(ls build/libs | sort -n | head -1)
docker-compose -f src/test/resources/docker/docker-compose.yml up -d
docker wait credentials_updater
docker logs xlr
./gradlew itest -PCHROME_HEADLESS_MODE=true
docker logs xlr
docker-compose -f src/test/resources/docker/docker-compose.yml stop
docker-compose -f src/test/resources/docker/docker-compose.yml rm -f
