# Quant-Trading
Python libaries for Quant Trading

Local Run
1. Change your filepath in main.py
2. Execute main.py

AWS
1. create folder in s3 upload the files
2. Spin up Ec2 vm cluster
3. To run the code everyday run autoscript by adding below in crontab -e
35 7 * * 1-5 screen -dms trading /home/ec2-user/trading/trading/auto_script 


