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

SCRIPT = "package.sh"
SRC_DIR = Path(__file__).parent.parent / "src"
TMP_DIR = Path("/tmp")

def run_script(args, input=None):
    """Run the script with the given args and return the completed process."""
    result = subprocess.run(
        [f"./{SCRIPT}"] + args,
        input=input,
        capture_output=True,
        text=True,
        cwd=SRC_DIR # change work dir
    )
    return result


def test_usage_shows_help():
    result = run_script([])
    assert result.returncode == 1
    assert "Usage:" in result.stdout

@pytest.mark.order(1)
def test_create_tar(tmp_path):
    # Make sure src directory exists
    assert SRC_DIR.exists(), f"Source directory not found: {SRC_DIR}"
    # Paths for the tarball
    tarball_path = tmp_path / "code.tar"
    # Prepare file paths as strings !!! relative to SRC_DIR !!!
    file_names = [f.name for f in SRC_DIR.glob("*.cpp")]
    assert file_names, "No .cpp files found in src"

    # Run the script to create the tarball
    result = run_script([
        "--mode", "create",
        "--tarball", str(tarball_path),
        "--files", *file_names
    ])
    assert result.returncode == 0
    assert tarball_path.exists()

    # copy .tar to /tmp
    result = subprocess.run(
        ["cp"] + [str(tarball_path), str(TMP_DIR)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0

@pytest.mark.order(2)
def test_extract_tar(tmp_path):
    # tarballl
    tarball_path = tmp_path / "code.tar"
    # extract path
    extract_dir = tmp_path / "extracted"
    extract_dir.mkdir()

    # mv .tar to tmp
    result = subprocess.run(
        ["mv"] + [str(TMP_DIR / "code.tar"), str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0

    # Run the script to extract the tarball
    result = run_script([
        "--mode", "extract",
        "--tarball", str(tarball_path),
        "--folder", str(extract_dir)
    ])
    assert result.returncode == 0

    # Find some test files in ../src
    files = list(SRC_DIR.glob("*.cpp"))
    assert files, "No .cpp files found in src"

    # Check at least one expected file extracted
    for f in files:
        extracted_file = extract_dir / f.name
        assert extracted_file.exists()

@pytest.mark.order(3)
def test_create_gzipped_tar(tmp_path):
    # Make sure src directory exists
    assert SRC_DIR.exists(), f"Source directory not found: {SRC_DIR}"
    # Paths for the tarball
    tarball_path = tmp_path / "code.tar.gz"
    # Prepare file paths as strings !!! relative to SRC_DIR !!!
    file_names = [f.name for f in SRC_DIR.glob("*.cpp")]
    assert file_names, "No .cpp files found in src"

    # Create gzip tarball
    result = run_script([
        "--mode", "create",
        "--format", "gzip",
        "--tarball", str(tarball_path),
        "--files", *file_names
    ])
    assert result.returncode == 0
    assert tarball_path.exists()

    # cpoy .tar to /tmp
    tmp_path = "/tmp"
    result = subprocess.run(
        ["cp"] + [str(tarball_path), str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0

@pytest.mark.order(4)
def test_extract_gzipped_tar(tmp_path):
    # tarballl
    tarball_path = tmp_path / "code.tar.gz"
    # extract path
    extract_dir = tmp_path / "extracted"
    extract_dir.mkdir()

    # mv .tar to tmp
    result = subprocess.run(
        ["mv"] + [str(TMP_DIR / "code.tar.gz"), str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0

    # Extract gzip tarball
    result = run_script([
        "--mode", "extract",
        "--format", "gzip",
        "--tarball", str(tarball_path),
        "--folder", str(extract_dir)
    ])
    assert result.returncode == 0
    assert (extract_dir / "main.cpp").exists()

    # Find some test files in ../src
    files = list(SRC_DIR.glob("*.cpp"))
    assert files, "No .cpp files found in src"

    # Check at least one expected file extracted
    for f in files:
        extracted_file = extract_dir / f.name
        assert extracted_file.exists()
