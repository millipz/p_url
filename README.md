# p-URL Short'ner

## Overview

This project is a URL shortening application built for a coding challenge. It consists of a backend service deployed on AWS Lambda with API Gateway, and a frontend interface. The application uses AWS Systems Manager (SSM) Parameter Store for data storage.

## To run the frontend locally

These instructions are for MacOS or Linux systems

1. Begin by cloning this repo locally.

1. Make sure you have Python 3 or above, and make installed

1. This app is built using [uv](https://docs.astral.sh/uv/). if you don't have it, `pip install uv`

1. Ensure you have a `.env.dev` file to connect to the backend. This should have been provided to you by the developer. If you want to run the backend yourself, see instructions below. Place this file in the `frontend` directory. Ensure it is named `.env.dev`, the leading '.' may be removed in some environments. The contents should look something like the below:

    ```
    API_ENDPOINT = https://xxxxxxxxxx.execute-api.eu-west-2.amazonaws.com/dev
    ```

1. `make frontend-all`

1. `make frontend-run`

## Project Structure

The project is divided into two main components:

- `backend/`: Contains the Lambda function code and backend logic
- `frontend/`: Houses the draft frontend application (Streamlit app)

## Requirements

- [uv](https://github.com/astral-sh/uv) for Python environment management

### Backend only
- [Terraform](https://www.terraform.io/) for infrastructure deployment
- AWS CLI configured with appropriate credentials


### To run the backend on your own AWS account

1. Set up the environment, install and run tests: `make backend-all`

1. Deploy (requires Terraform and AWS credentials): `make deploy-backend`

1. To destroy the infrastructure: `make destroy-infrastructure`
