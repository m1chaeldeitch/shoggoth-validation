"""
shoggoth-validation - preparation.py

Contains various helpers for manipulating autograder submissions in bulk.

Requires a local configuration to be specified, see after imports.

The most common task is to generate JSON for a folder of submissions. The typical workflow is:
1) Use rename_canvas_submission_files to do initial processing (module_0raw -> module_1renamed).
2) Make a manual copy of module_0raw to module_2patched.
3) Make any needed corrections to the files in module_2patched.
4) Run run_shoggoth_bulk to run the local shoggoth to generate JSON for all submissions.

where module is a placeholder for something more speific like (ser334_24sc_m2).

See main for an example.

"""
__author__ = "Ruben Acuna"
__copyright__ = "Copyright 2024-25, Ruben Acuna"

import glob
import os
import platform
import shutil
import sys
import subprocess
import json
import zipfile
from enum import Enum

import constants

# LOCAL CONFIGURATION
if platform.system() == "Windows":
    FOLDER_SER222_AUTOGRADERS = "C:\\Users\\Ruben\\Dropbox\\Git\\ser222\\homework_projects"
    FOLDER_SER334_AUTOGRADERS = None
elif platform.system() == "Linux":
    FOLDER_SER222_AUTOGRADERS = None
    FOLDER_SER334_AUTOGRADERS = "/home/mike-jones/Documents/ASU/FURI/Autograder-Related/LocalGS"
else:
    print(f"Unsupported OS found: {platform.system()}")
    exit()


class Language(Enum):
    JAVA = 1    # only tested on Windows
    C = 2       # only tested on Linux


def rename_canvas_submission_files(input_folder, output_folder):
    r"""
    This function converts the default Canvas files into the simpler form listed in the assignment. Trims the prefix and
    removes -# from the end of files. Assumes that the input is a folder of source files, one file per submission.

    The usual usage is to process a folder of submissions (input_folder) from Canvas:
        Example: data_original\submissions\ser334_24sc_m2_0raw
    and then put the renamed files into a new folder (output_folder):
        Example: data_original\submissions\ser334_24sc_m2_1renamed

    :param input_folder: Folder of submissions from Canvas.
    :param output_folder: Folder for renamed files.
    """
    #TODO: delete previous contents of output folder.

    for filename in os.listdir(input_folder):
        new_name = filename.replace("-1", "")
        new_name = new_name.replace("-2", "")

        new_name = new_name.split("_")[-1]

        if os.path.exists(output_folder + os.sep + new_name):
            print(f"target file name {new_name} already exists.")
            continue

        shutil.copy(input_folder + os.sep + filename, output_folder + os.sep + new_name)


def run_shoggoth_bulk(course, lang, config_file, semester):
    r"""
    Runs a local installation of a shoggoth java or c autograder on a folder of submissions and saves the results in
    JSON. Supports either single source file submission or .zip containers.

    For this to function, there must a local copy of the shoggoth autograder. Its location has to be configured at the
    top of this file.

    There must also be a folder of submissions at:
        constants.FOLDER_SUBMISSIONS + os.sep + "{course}_{semester}_{module}_2patched"
    For example:
        data_original\submissions\ser334_24sc_m2_2patched

    :param course: Short name for the course.
    :param lang: the programming used for the assignment.
    :param config_file: Config from autograder.
    :param semester: Semester ID for data (e.g., 24sc).
    """

    print("run_shoggoth_bulk:")

    with open(config_file) as file:
        config = json.load(file)

    module = config["module"]
    uid = config["uid"]
    config_proj_loc = config["project_location"][:-1].replace("/", os.sep)

    input_folder = constants.FOLDER_SUBMISSIONS + os.sep + f"{course}_{semester}_{module}_2patched"
    output_folder = constants.FOLDER_EVALUATIONS + os.sep + f"{course}_{semester}_{module}"

    if lang == Language.JAVA:
        autograder_root = FOLDER_SER222_AUTOGRADERS + os.sep + f"{course}_{uid}_hw02_autograder"
        autograder_src = autograder_root + os.sep + config_proj_loc[19:]

    else: # C
        autograder_root = FOLDER_SER334_AUTOGRADERS + os.sep + f"{course}_{uid}_hw02_autograder"
        autograder_src = FOLDER_SER334_AUTOGRADERS + os.sep + config_proj_loc[12:]

    # TODO: support optional files
    if "files_optional" in config and len(config["files_optional"]) > 0:
        raise Exception("run_shoggoth_bulk() does not support optional files.")

    # check if output folder exists
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    # check if target folder for submission source code exists
    if not os.path.exists(autograder_src):
        os.mkdir(autograder_src)

    for filename in os.listdir(input_folder):
        if not (".java" in filename or ".c" in filename or ".zip" in filename):
            continue

        print ("Processing " + filename)
        output_filename = filename.split(".")[0] + ".json"

        #clean the project folder of existing files.
        if lang == Language.C:
            existing_files = glob.glob(autograder_src + os.sep + "*")
            for file_path in existing_files:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)

        if ".java" in filename or ".c" in filename:
            target_file_path = autograder_src + os.sep + config["files_required"][0]

            if os.path.exists(target_file_path):
                os.remove(target_file_path)

            shutil.copy(input_folder + os.sep + filename, target_file_path)
        else: # must be .zip

            # remove existing files. to ensure that all files are refreshed (even if zip is incomplete).
            for required_file in config["files_required"]:
                expected_file = autograder_src + os.sep + required_file

                if os.path.exists(expected_file):
                    os.remove(expected_file)

            # extract files into target file. probably check if all are there
            with zipfile.ZipFile(input_folder + os.sep +filename, 'r') as zipf:
                compressed_files = zipf.namelist()
                selected_files = [x for x in compressed_files if x in config["files_required"]]
                skipped_files = [x for x in compressed_files if x not in config["files_required"]]

                if len(skipped_files):
                    print(f"  Skipping {len(skipped_files)} files in ZIP ({skipped_files}).")

                zipf.extractall(autograder_src, members=selected_files)

        output_path = output_folder + os.sep + output_filename
        print("  output_path:", output_path)

        # check if we actually need to generate JSON
        if not os.path.exists(output_path):

            if lang == Language.JAVA:
                # the console output of shoggoth-c is the JSON result.
                with open(output_path, "w") as output_stream:
                    arg = ["mvn", "-q", "compile", "exec:java"] # force recompile so that tests don't run with previous bins.
                    p = subprocess.run(arg, shell=True, cwd=autograder_root, stdout=output_stream)

            else: # C
                # the console output of shoggoth-c is the human-readable test summery.
                log_path = os.path.splitext(output_path)[0] + "_stdout.txt"

                # shoggoth-c saves the results to a separate JSON file.
                results_path = FOLDER_SER334_AUTOGRADERS + os.sep + "results" + os.sep + "results.json"

                if os.path.exists(results_path):
                    os.remove(results_path)

                with open(log_path, "w") as output_stream:
                    arg = [sys.executable, "main.py"]
                    p = subprocess.run(arg, shell=False, cwd=autograder_root, stdout=output_stream)

                shutil.copy(results_path, output_path)

        else:
            print ("  JSON output already exists, skipping autograder.")


# testing area
if __name__ == '__main__':

    #SER222
    #run_shoggoth_bulk("ser222", Language.JAVA, "config_m12.json", "24su")

    #SER334
    #rename_canvas_submission_files(constants.FOLDER_SUBMISSIONS + os.sep + "ser334_24sc_m2_0raw", constants.FOLDER_SUBMISSIONS + os.sep + "ser334_24sc_m2_1renamed")
    #run_shoggoth_bulk("ser334", Language.C, constants.FOLDER_DATA_ORIGINAL + os.sep + "ser334_config_m2.json", "24sc")

    #SER334 M3 (developmental test set)
    run_shoggoth_bulk("ser334", Language.C, constants.FOLDER_DATA_ORIGINAL + os.sep + "ser334_config_m3.json", "00dv")
