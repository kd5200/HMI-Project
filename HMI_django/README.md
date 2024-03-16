# HMI-Project

This repository contains the source code for the HMI project.

## Installing Dependencies

To install project dependencies, follow these steps:

1. Navigate to the root directory of the project (/HMI_project/work_project/HMI_django).

2. Run the following command to install dependencies using pip:
   ```sq
   pip install -r requirements.txt
   ```

##

## Installing PostgreSQL

To install PostgreSQL, follow these steps:

1. Install PostgreSQL using your package manager:
   ```
   sudo apt update
   sudo apt install postgresql postgresql-contrib
   ```
2. Start the PostgreSQL service:
   ```
   sudo systemctl start postgresql
   ```

##

## Setting Environment Variables

To set environment variables, follow these steps:

1. Create a .env file in the root directory of the project.

2. Add environment variables to the .env file in the following format:
   ```
   API_KEY="value"
   ```

##

## Creating an API Key from OpenWeatherAPI

To create an API key from OpenWeatherAPI, follow these steps:

1. Visit the OpenWeatherAPI website (https://home.openweathermap.org/users/sign_in) and sign up for an account.

2. Once logged in, navigate to the API keys section.

3. Generate a new API key and copy it for later use.

##

## Creating a Google API Key

To create a Google API key, follow these steps:

1. Visit the Google Cloud Console and sign in or create a new account. (https://console.cloud.google.com/apis/library?project=hmi-cities-data)
2. Create a new project or select an existing one.

3. Navigate to the APIs & Services > Credentials section.

4. Create a new API key and copy it for later use.

##

## Running the Django Server Locally

##
