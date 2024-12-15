# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import requests
import subprocess
import os
import shutil

from docker.config import COMBINED_DIR

def main():
    # Clean up combined results before starting
    url = "https://raw.githubusercontent.com/michaellatman/mcp-get/refs/heads/main/packages/package-list.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to download the file: {e}")
        return

    try:
        package_list = json.loads(response.text)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        return

    for package in package_list:
        source_url = package.get("sourceUrl")
        if source_url:
            trimmed_url = "/".join(source_url.split("/")[:5])
            try:
                result = subprocess.run(["./docker_run_one.sh", trimmed_url], capture_output=True, text=True)
                result.check_returncode()
                print(f"Successfully processed {trimmed_url}")
                print(result.stdout)
            except subprocess.CalledProcessError as e:
                print(f"Failed to process {trimmed_url}: {e}")
                print(e.stderr)

if __name__ == "__main__":
    main()
