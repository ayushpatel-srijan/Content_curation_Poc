#!/bin/bash
ssh -fNT -L 8080:localhost:8080 -i /root/.ssh/chat_gpt_demo.pem ec2-user@52.76.138.243 &
streamlit run app.py --server.port=8501

