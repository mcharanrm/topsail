#! /bin/bash

if [ -n "$BASH_VERSION" ]; then
    # assume Bash
    TESTING_ANSIBLE_LLM_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
elif [ -n "$ZSH_VERSION" ]; then
    # assume ZSH
    TESTING_ANSIBLE_LLM_DIR=${0:a:h}
elif [[ -z "${TESTING_ANSIBLE_LLM_DIR:-}" ]]; then
     echo "Shell isn't bash nor zsh, please expose the directory of this file with TESTING_ANSIBLE_LLM_DIR."
     false
fi

TESTING_UTILS_DIR="$TESTING_ANSIBLE_LLM_DIR/../utils"

export CI_ARTIFACTS_FROM_COMMAND_ARGS_FILE=${TESTING_NOTEBOOKS_DIR}/command_args.yaml

if [[ -z "${CI_ARTIFACTS_FROM_CONFIG_FILE:-}" ]]; then
    export CI_ARTIFACTS_FROM_CONFIG_FILE=${TESTING_NOTEBOOKS_DIR}/config.yaml
fi
echo "Using '$CI_ARTIFACTS_FROM_CONFIG_FILE' as configuration file."

source "$TESTING_UTILS_DIR/configure.sh"
