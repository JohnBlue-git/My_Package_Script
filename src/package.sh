#!/bin/bash

#
# How to Use
#

how_to_use()
{
  echo "Usage: $0"
  echo " --mode [create|extract]"
  echo " --format [gzip]"
  echo " --folder <folder the files be extracted to>"
  echo " --tarball <input tarball / output tarball>"
  echo " --files array<files to be compressed>"
  echo ""
  echo "Example:"
  echo "$0 --mode create --tarball ./code.tar --files ./main.cpp"
  echo "$0 --mode create --format gzip --tarball ./code.tar.gz --files ./main.cpp"
  echo "$0 --mode extract --tarball ./code.tar --folder ./tmp"
  echo "$0 --mode extract --format gzip --tarball ./code.tar.gz --folder ./tmp"
  echo ""
  echo "exit code:"
  echo " 0: success"
  echo " 1: hit how to use / invalid usage / other fail"
  echo " 2: tarball or file or follder does not exist"
  echo " 3: fail to tar command (or is not tarball)"
  exit 1
}

if [[ $# -eq 0 ]]; then
  how_to_use
fi

#
# Parse command-line arguments
#

# Check for multiple option declarations
check_option() {
    local option_name="$1"
    local option_value="$2"
    local variable_name="$3"

    if [[ -n "${!variable_name}" ]]; then
        echo "Error: $option_name specified multiple times."
        exit 1
    fi

    if [[ -z "$option_value" || "$option_value" == --* ]]; then
        echo "Error: $option_name option requires a value."
        exit 1
    fi
    eval "$variable_name=\"$option_value\""
}

# Validate if a mode is in the allowed list
validate_mode() {
    local mode="$1"
    shift
    local allowed_modes=("$@")
    
    local is_valid=false
    for valid_mode in "${allowed_modes[@]}"; do
        if [[ "$mode" == "$valid_mode" ]]; then
            is_valid=true
            break
        fi
    done
    if [[ "$is_valid" == false ]]; then
        echo "Error: Invalid mode '$mode'. Allowed values are: ${allowed_modes[*]}"
        exit 1
    fi
}

echo "Parsing options and arguments"

ALLOWED_MODES=('create' 'extract' 'delete')
ALLOWED_FORMATS=('gzip')
FILES=()
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --mode)
            check_option "--mode" "$2" MODE
            validate_mode "$MODE" "${ALLOWED_MODES[@]}"
            # Skip --input and its value
            shift 2
            ;;
        --format)
            check_option "--format" "$2" FORMAT
            validate_mode "$FORMAT" "${ALLOWED_FORMATS[@]}"
            shift 2
            ;;
        --folder)
            check_option "--folder" "$2" FOLDER
            shift 2
            ;;
        --tarball)
            check_option "--tarball" "$2" TARBALL
            shift 2
            ;;
        --files)
            check_option "--files" "$2" FILES
            shift
            while [[ "$#" -gt 0 && ! "$1" =~ ^-- ]]; do
                FILES+=("$1")
                shift
            done
            ;;
        *)
            how_to_use
            ;;
    esac
done

# Ensure required options are provided based on mode
if [[ ! -n "$MODE" ]]; then
    echo "Error: please assign mode."
    exit 1
fi
case $MODE in
    'create')
        if [[ -z "$TARBALL" ]]; then
            echo "Error: --tarball is required for create mode."
            exit 1
        elif [ ${#FILES[@]} -eq 0 ]; then
            echo "Error: --files is required for create mode."
            exit 1
        fi
        ;;
    'extract')
        if [[ -z "$TARBALL" ]]; then
            echo "Error: --tarball is required for extract mode."
            exit 1
        elif [[ -z "$FOLDER" ]]; then
            echo "Error: --folder is required for extract mode."
            exit 1
        fi
        ;;
    *)
        how_to_use
        ;;
esac

#
# Processing
#

# Check for valid files
valid_files() {
    local files=("$@")
    local existing_files=()
    for file in "${files[@]}"; do
        if [ -f "$file" ]; then
            existing_files+=("$file")
        fi
    done
    echo "${existing_files[@]}"
}

echo "Packaging start"

# Main processing logic
case $MODE in
    'create')
        EXIST_FILES=($(valid_files "${FILES[@]}"))
        if [ ${#EXIST_FILES[@]} -eq 0 ]; then
            echo "No valid files found: ${FILES[@]}"
            exit 2
        fi
        if [[ -n "$FORMAT" && "$FORMAT" == "gzip" ]]; then
            tar -cpzvf "$TARBALL" "${EXIST_FILES[@]}" || { echo "Failed to create tarball $TARBALL"; exit 3; }
        else
            tar -cpvf "$TARBALL" "${EXIST_FILES[@]}" || { echo "Failed to create tarball $TARBALL"; exit 3; }
        fi
        echo "Created tarball: $TARBALL"
        ;;
    'extract')
        if [ ! -f "$TARBALL" ]; then
            echo "$TARBALL does not exist."
            exit 2
        fi
        if [ ! -d "$FOLDER" ]; then
            echo "$FOLDER does not exist."
            exit 2
        fi
        if [[ -n "$FORMAT" && "$FORMAT" == "gzip" ]]; then
            if ! file "$TARBALL" | grep -iq "gzip"; then
                echo "The file is not a .tar.gz compressed file."
                exit 3
            fi
            tar -xpzvf "$TARBALL" -C "$FOLDER" || { echo "Failed to extract tarball $TARBALL"; exit 3; }
        else
            if ! file "$TARBALL" | grep -iq "POSIX tar archive"; then
                echo "The file is not a .tar compressed file."
                exit 3
            fi
            tar -xpvf "$TARBALL" -C "$FOLDER" || { echo "Failed to extract tarball $TARBALL"; exit 3; }
        fi
        echo "Extracted to folder: $FOLDER"
        ;;
esac

exit 0

