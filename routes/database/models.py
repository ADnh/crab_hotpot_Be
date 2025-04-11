# db/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)


class Video(Base):
    __tablename__ = "video"

    id = Column(Integer, primary_key=True)
    url_video = Column(String(255), nullable=False)
    logs = relationship("Log", back_populates="video")


class Target(Base):
    __tablename__ = "target"

    id = Column(Integer, primary_key=True)
    hoten = Column(String(100))
    sdt = Column(String(20))
    diachi = Column(String(255))
    chuthich = Column(Text)
    
    images = relationship("Image", back_populates="target")
    logs = relationship("Log", back_populates="target")


class Image(Base):
    __tablename__ = "image"

    id = Column(Integer, primary_key=True)
    url_image = Column(String(255), nullable=False)
    id_target = Column(Integer, ForeignKey("target.id"))
    
    target = relationship("Target", back_populates="images")


class Log(Base):
    __tablename__ = "log"

    id = Column(Integer, primary_key=True)
    id_video = Column(Integer, ForeignKey("video.id"))
    id_target = Column(Integer, ForeignKey("target.id"))
    speech = Column(Text)
    comments = Column(Text)

    video = relationship("Video", back_populates="logs")
    target = relationship("Target", back_populates="logs")
