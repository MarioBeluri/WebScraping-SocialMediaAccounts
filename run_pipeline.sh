#!/usr/bin/env bash

screen -dmS s0 bash -c 'venv/bin/python3 -m scripts.toofame --conf=$(pwd)/local.config.yaml; exec sh'
screen -dmS s1 bash -c 'venv/bin/python3 -m scripts.accs_market --conf=$(pwd)/local.config.yaml; exec sh'
screen -dmS s2 bash -c 'venv/bin/python3 -m scripts.accsmarket --conf=$(pwd)/local.config.yaml; exec sh'
screen -dmS s3 bash -c 'venv/bin/python3 -m scripts.midman --conf=$(pwd)/local.config.yaml; exec sh'
screen -dmS s4 bash -c 'venv/bin/python3 -m scripts.socialtradia --conf=$(pwd)/local.config.yaml; exec sh'
screen -dmS s5 bash -c 'venv/bin/python3 -m scripts.surgegram --conf=$(pwd)/local.config.yaml; exec sh'
screen -dmS s6 bash -c 'venv/bin/python3 -m scripts.swapsocials --conf=$(pwd)/local.config.yaml; exec sh'
screen -dmS s7 bash -c 'venv/bin/python3 -m scripts.buysocia --conf=$(pwd)/local.config.yaml; exec sh'
