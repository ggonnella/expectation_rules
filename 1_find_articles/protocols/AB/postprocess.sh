#!/usr/bin/env bash
#
# Post-process the results of query.sh
#
# Usage:
#   ./postprocess.sh <query_out>
#
# Arguments:
#   <query_out>   Output of query.sh
#

QUERY_OUT=$1

sort -n -u -r ${QUERY_OUT}
