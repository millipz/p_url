# p-URL Short'ner

## Overview

This project is a URL shortening application built for a coding challenge. It consists of a backend service deployed on AWS Lambda with API Gateway, and a frontend interface. The application uses AWS Systems Manager (SSM) Parameter Store for data storage.

## Project Structure

The project is divided into two main components:

- `backend/`: Contains the Lambda function code and backend logic
- `frontend/`: Houses the draft frontend application (Streamlit app)

## Prerequisites

- [uv](https://github.com/astral-sh/uv) for Python environment management

### Frontend only

- `frontend/.env.dev` file with API Gateway URL to link to backend e.g.

    ```
    API_ENDPOINT = https://xxxxxxxxxx.execute-api.eu-west-2.amazonaws.com/dev
    ```

### Backend only
- [Terraform](https://www.terraform.io/) for infrastructure deployment
- AWS CLI configured with appropriate credentials

## Setup and Installation

### Backend

1. Set up the environment, install and run tests:
    ```
    make backend-all
    ```

2. Deploy (requires Terraform and AWS credentials)
    ```
    make deploy-backend
    ```

### Frontend

1. Set up the environment, install and run tests:
    ```
    make frontend-all
    ```

2. Run Streamlit App
    ```
    make frontend-run
    ```

## Deployment


### Deploy the infrastructure:
    ```
    make deploy-infrastructure
    ```

### Destroy the infrastructure:
    ```
    make destroy-infrastructure
    ```
