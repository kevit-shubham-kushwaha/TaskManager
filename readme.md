# TaskManager

## Project Overview

TaskManager is an application designed to manage and assign tasks to students. It allows you to track all the tasks each student is involved in, monitor the status of each task, view who created the task, its due date, and the overall deadline — helping ensure accountability and timely completion.


## Project Features

1. Task Creation
2. Task Tracking
3. User Authentication
4. User Authorizatation


## Setting Up Environment

### 1. Cloning project
- git clone url
- cd TaskManager

### 2.Install virtual environment
- sudo apt install python3-virtualenv
- pip install virtualenv

### 3.Setting up the virtual environment
- python -m venv venv

### 4. Activating the virtual environment
- venv\Scripts\activate
- source venv/bin/activate

### 5. Installing Dependies for virtual environment
- pip install -r requirements.txt

### 6. Setting up env variable
- touch .env 
- add all data for .env from reference of example .env


## Running the Applicatation

- python main.py
- python3 main.py