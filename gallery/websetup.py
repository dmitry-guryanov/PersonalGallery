"""Setup the PersonalGallery application"""
import logging
import os

from gallery import model
from gallery.config.environment import load_environment
from gallery.model.meta import Session, Base

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    load_environment(conf.global_conf, conf.local_conf)

    # Create the tables if they don't already exist
    log.info("Creating tables...")
    Base.metadata.create_all(bind = Session.bind)
    log.info("Successfully set up.")

    if not os.path.exists(conf.global_conf["permanent_store"]):
        os.mkdir(conf.global_conf["permanent_store"])

    log.info("Adding front page data...")
    album = model.Album(id = 0, name = "root")
    Session.add(album)
    Session.commit()
    log.info("Successfully set up.")

