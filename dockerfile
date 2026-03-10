# 1. Use a slim Python image
FROM python:3.12-slim

# 2. Set the working directory
WORKDIR /app

# 3. Install 'uv'
RUN pip install --no-cache-dir uv

# 4. Copy the configuration and source files first
# We copy everything so 'uv' can see the 'backend' folder and 'README.md'
COPY pyproject.toml README.md* ./
COPY ./backend ./backend
COPY ./frontend ./frontend

# 5. Install the project and dependencies
# Now that the folders exist, this command will succeed
RUN uv pip install --system .

# 6. Expose the port
EXPOSE 8000

# 7. Command to start the server
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
