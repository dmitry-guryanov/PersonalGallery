"""Setup the PersonalGallery application"""
import logging

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

    log.info("Adding front page data...")
    album = model.Album(id = 0, name = "root")
    Session.add(album)
    Session.commit()
    log.info("Successfully set up.")

    #FIXME: create needed directories
