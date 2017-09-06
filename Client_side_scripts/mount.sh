#!/bin/bash
read -p "Enter Your Name: "  username
#sudo ssh -o "StrictHostKeyChecking no" -i /home/chandu/scripts/id_rsa yash@192.168.0.26 /home/yash/runTest.sh $username
ssh -t -o "StrictHostKeyChecking no" -i /home/ubuntu-mate/scripts/id_rsa  yash@192.168.0.26 /home/yash/scripts/dedup.sh $username
