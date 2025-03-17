from cloudflare import Cloudflare
from fastapi import  FastAPI, HTTPException, status
from sqlmodel import select
from .database import Database
from .models import PublicUserProfileResponse, UploadVideoResponse, Video, VideoLike, VideoResponse

app = FastAPI()

client = Cloudflare()

@app.get("/")
def hello_world():
    return {"Hello": "World"}


@app.get("/video/{id}", response_model=VideoResponse)
def get_video_(
        db: Database # get database connection with dependecy injection
    ):
    video = db.get(Video, id)

    # fetch our db to get id > cf identifier mapping
    video_info = client.stream.get(identifier=video.cloudflare_id, account_id="account_id")
    stream = client.stream.embed.get(identifier=video.cloudflare_id, account_id="account_id")

    # fetch video likes from our db using a sql count to avoid transmitting all rows back to app
    s = select(VideoLike.id).where(VideoLike.video_id == id).count()
    likes = db.exec(s)

    if not video_info:
        return 500
    
    if not stream:
        return 500

    return VideoResponse(stream=stream, thumbnail=video_info.thumbnail, duration=video_info.duration, likes=likes)

@app.post("/video/{id}/like")
def save_video_like():
    pass

@app.get("/video/{id}/like")
def get_video_likes():
    pass

@app.post("/video/{id}/fav")
def save_video_fav():
    pass

@app.get("/upload", response_model=UploadVideoResponse)
def get_upload_url(db: Database, duration: int = 300):
    if duration > 500:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Duration exceeds allowed") 

    # https://developers.cloudflare.com/api/resources/stream/subresources/direct_upload/methods/create/
    du = client.stream.direct_upload.create(account_id="account_id", max_duration_seconds=duration)
    if du:
        video = Video(cloudflare_id=du.uid, duration=duration)
        db.add(video)

        return UploadVideoResponse(video_meta=video, upload_url=du.upload_url)


@app.get("/profile/{id}", response_model=PublicUserProfileResponse)
def get_user_profile(db: Database):
    # return a user's public profile from info in db
    # likes = db.get(...)
    # favourites = db.get(...)
    # uploads = db.get(...)

    return PublicUserProfileResponse(likes=[], favourites=[], uploads=[])