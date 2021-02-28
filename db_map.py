from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
import os
import asyncio
import logging
from aiogram import Bot
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from config import TOKEN, MY_ID, DB_FILENAME

Base = declarative_base()

class MediaIds(Base):
    __tablename__ = 'MediaIds'
    id = Column(Integer, primary_key=True)
    file_id = Column(String(255))
    filename = Column(String(255))



async def start():
    engine = create_engine(f'sqlite:///{DB_FILENAME}')

    if not os.path.isfile(f'./{DB_FILENAME}'):
        Base.metadata.create_all(engine)

    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)

    bot = Bot(token=TOKEN)
    session = Session()

    msg = await bot.send_voice(MY_ID, open('demo-media/ogg/Rick_Astley_-_Never_Gonna_Give_You_Up.ogg' ,'rb') , disable_notification=True)
    newItem = MediaIds(file_id=msg.voice.file_id, filename='Voice')
    session.add(newItem)

    msg = bot.send_document(MY_ID, open('demo-media/files/very important text file.txt' ,'rb') , disable_notification=True)
    newItem = MediaIds(file_id=msg.document.file_id, filename='Document')
    session.add(newItem)

    msg = bot.send_video(MY_ID, open('demo-media/videos/hedgehod.mp4' ,'rb') , disable_notification=True)
    newItem = MediaIds(file_id=msg.video.file_id, filename='Video')
    session.add(newItem)

    msg = bot.send_video_note(MY_ID, open('demo-media/videoNotes/cute-puppy.mp4' ,'rb') , disable_notification=True)
    newItem = MediaIds(file_id=msg.video_note.file_id, filename='VideoNote')
    session.add(newItem)
    session.commit()
    session.close()
    Session.remove()

if __name__ == '__main__':
    start()