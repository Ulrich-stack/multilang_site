
# Multilang Site

This project is a multilingual Django blog website with a chatbot feature. It is configured to use Render for deployment and includes support for multiple languages.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Deployment](#deployment)
- [Environment Variables](#environment-variables)

## Features

- Multilingual support
- Integrated chatbot using OpenAI and LangChain for RAG (Retrieval-Augmented Generation)
- Dynamic language selector
- Deployed using Docker on Render

## Requirements

- Python 3.12
- Dependencies in requirements.txt

## Installation

### Clone the Repository

```bash
git clone https://github.com/Ulrich-stack/multilang_site.git
cd multilang_site
```

### Create and Activate Virtual Environment

```bash
python -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
```

### Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Set Up Environment Variables

Create a `.env` file in the project root and add the following environment variables:

```
# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key
```

### Apply Migrations

```bash
python manage.py migrate
```

## Running the Project

### Development Server

To run the development server, execute:

```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your web browser to see the application.


## Environment Variables

Ensure the following environment variables are set in your `.env` file or in your deployment environment:

- `OPENAI_API_KEY`: Your OpenAI API key used for the chatbot.
