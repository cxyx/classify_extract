#!/usr/bin/env bash
cd ..
model_links_dir=$1
config_links_dir=$2
python -m classify_extract.app.start_online ${model_links_dir} ${config_links_dir} classify_extract_online
