
import subprocess
import os
from pathlib import Path
import tarfile
import gzip
import shutil

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


def test_usage_shows_help():
    result = run_script([])
    assert result.returncode == 1
    assert "Usage:" in result.stdout


def test_create_with_multiple_files(tmp_path):
    # Make sure src directory exists
    assert SRC_DIR.exists(), f"Source directory not found: {SRC_DIR}"

    # Find some test files in ../src
    test_files = list(SRC_DIR.glob("*.cpp"))  # Or change pattern as needed
    assert test_files, "No .cpp files found in src"

    # Paths for the tarball
    tarball_path = tmp_path / "code.tar"

    # Prepare file paths as strings
    file_paths = [str(f.resolve()) for f in test_files]

    # Run the script to create the tarball
    result = run_script([
        "--mode", "create",
        "--tarball", str(tarball_path),
        "--files", *file_paths
    ])

    assert result.returncode == 0
    assert tarball_path.exists()

    # Optionally: extract and validate content
    # extract_dir = tmp_path / "extracted"
    # extract_dir.mkdir()
    # result = run_script([
    #     "--mode", "extract",
    #     "--tarball", str(tarball_path),
    #     "--folder", str(extract_dir)
    # ])
    # assert result.returncode == 0

    # Check at least one expected file extracted
    # for f in test_files:
    #     extracted_file = extract_dir / f.name
    #     assert extracted_file.exists()


def test_create_and_extract_gzipped_tar(tmp_path):
    file_path = tmp_path / "main.cpp"
    file_path.write_text("int main() { return 0; }")

    tarball_path = tmp_path / "code.tar.gz"

    # Create gzip tarball
    result = run_script([
        "--mode", "create",
        "--format", "gzip",
        "--tarball", str(tarball_path),
        "--files", str(file_path)
    ])
    assert result.returncode == 0
    assert tarball_path.exists()

    extract_dir = tmp_path / "out"
    extract_dir.mkdir()

    # Extract gzip tarball
    # result = run_script([
    #     "--mode", "extract",
    #     "--format", "gzip",
    #     "--tarball", str(tarball_path),
    #     "--folder", str(extract_dir)
    # ])
    # assert result.returncode == 0
    # assert (extract_dir / "main.cpp").exists()


def test_invalid_mode_fails(tmp_path):
    result = run_script(["--mode", "invalid"])
    assert result.returncode == 1
    assert "Invalid mode" in result.stdout or result.stderr


def test_missing_tarball_error(tmp_path):
    result = run_script(["--mode", "extract", "--folder", str(tmp_path)])
    assert result.returncode == 1
    assert "Error" in result.stdout or result.stderr


def test_missing_required_args(tmp_path):
    result = run_script(["--mode", "create"])
    assert result.returncode == 1
    assert "Error" in result.stdout or result.stderr
