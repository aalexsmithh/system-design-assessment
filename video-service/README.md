This is a mockup of the FastAPI app that would run this fictional video streaming service.

Development requirements:
- poetry
- use of pyenv is strongly encouraged

Run this service 
```bash
cd video-service
pyenv install
poetry env use python
poetry install
poetry run fastapi dev src/video_service/main.py
```
