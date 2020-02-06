#!/usr/bin/env bash
ps aux | grep classify_extract_online | awk '{print $2}' | xargs kill