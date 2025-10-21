#!/bin/bash
set -e

echo "Installing dependencies one by one..."
pip install --upgrade pip
pip install fastapi
pip install "uvicorn[standard]"
pip install sqlalchemy
pip install pandas
pip install python-multipart
pip install pydantic
pip install python-dotenv

echo "All dependencies installed successfully!"