FROM jjanzic/docker-python3-opencv
COPY app.py .
COPY templates templates
COPY static static
COPY requirements.txt .
COPY camera.py .
COPY image_utils.py .
COPY image_processor.py .
COPY pose_estimator.py .
COPY setup.sh .
RUN sh setup.sh
EXPOSE 8008
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r hrnet/requirements_for_docker.txt
CMD ["python", "app.py"]
