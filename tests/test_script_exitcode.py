import psutil
import pytest
import requests
import subprocess
import os
from pathlib import Path
import time
import json
import io
import tarfile
import gzip

SCRIPT = "../src/package.sh"
SRC_DIR = Path(__file__).parent.parent / "src"

def run_script(args, input=None):
    """Run the script with the given args and return the completed process."""
    result = subprocess.run(
        [SCRIPT] + args,
        input=input,
        capture_output=True,
        text=True,
    )
    return result

def test_invalid_mode_fails(tmp_path):
    result = run_script(["--mode", "invalid_mode"])
    assert result.returncode == 1
    assert "Invalid mode" in result.stdout or result.stderr

def test_missing_required_args(tmp_path):
    result = run_script(["--mode", "create"])
    assert result.returncode == 1
    assert "Error" in result.stdout or result.stderr

def test_missing_tarball_arga(tmp_path):
    result = run_script(["--mode", "extract", "--folder", str(tmp_path)])
    assert result.returncode == 1
    assert "Error" in result.stdout or result.stderr

def test_invalid_file_path(tmp_path):
    result = run_script(["--mode", "create", "--tarball", "tarball.tar", "--files", "invalid_file"])
    assert result.returncode == 2

def test_invalid_folder_path(tmp_path):
    result = run_script(["--mode", "extract", "--tarball", "tarball.tar", "--folder", "invalid_folder"])
    assert result.returncode == 2

def test_invalid_tarball_fail(tmp_path):
    result = run_script(["--mode", "extract", "--tarball", "../src/main.cpp", "--folder", str(tmp_path)])
    assert result.returncode == 3
