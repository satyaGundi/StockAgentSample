# 1. Use a slim Python image to keep the size small
FROM python:3.12-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Install 'uv' for lightning-fast dependency installation
RUN pip install --no-cache-dir uv

# 4. Copy ONLY the dependency file first (Optimizes Docker caching)
COPY pyproject.toml .

# 5. Install dependencies directly into the system python
RUN uv pip install --system .

# 6. Copy your project folders into the container
COPY ./backend ./backend
COPY ./frontend ./frontend

# 7. Expose the port FastAPI runs on
EXPOSE 8000

# 8. Command to start the server
# We use 0.0.0.0 so it's accessible outside the container (crucial for Azure)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
