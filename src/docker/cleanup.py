# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import shutil
import os

def cleanup(clone_dir, results_dir="./results"):
    """Remove the cloned repository and all results files."""
    # Clean working directory
    if os.path.exists(clone_dir):
        shutil.rmtree(clone_dir)
    
    # Clean results directory
    if os.path.exists(results_dir):
        for file in os.listdir(results_dir):
            file_path = os.path.join(results_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)


if __name__ == "__main__":
    clone_dir = "./working"
    cleanup(clone_dir)
