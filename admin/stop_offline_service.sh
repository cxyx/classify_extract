#!/usr/bin/env bash
ps aux | grep classify_extract_offline | awk '{print $2}' | xargs kill