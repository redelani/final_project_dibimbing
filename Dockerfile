FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

COPY app /app/ 
COPY app/streamlit_app.py /app/app/
COPY app/model.py /app/app/


# Expose ports for FastAPI and Streamlit
EXPOSE 8000
EXPOSE 8501

# Start Uvicorn and Streamlit
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 & streamlit run app/streamlit_app.py"]