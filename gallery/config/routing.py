"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper

def make_map():
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=1)#config['debug'])

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
#    map.connect('error/:action/:id', controller='error')

    # CUSTOM ROUTES HERE

#    map.connect(':controller/:action/:id')
    map.connect('', controller='album', action='index')
    map.connect('album/:aid', controller='album', action='show_first_page')
    map.connect('album/:aid/:page', controller='album', action='show_page')
    map.connect('login', controller='login', action='index')
    map.connect('login/:action', controller='login')
    map.connect('photo/:aid/:pid', controller='photo', action='index')
    map.connect('admin/album_add/:aid', controller='admin', action='album_add', aid = 0)
    map.connect('admin/album_del/:aid', controller='admin', action='album_del', aid = 0)
    map.connect('admin/album_edit/:aid', controller='admin', action='album_edit', aid = 0)
    map.connect('admin/album_edit_submit/:aid', controller='admin', action='album_edit_submit', aid = 0)
    map.connect('admin/photo_add/:aid', controller='admin', action='photo_add')
    map.connect('admin/photo_add_submit/:aid', controller='admin', action='photo_add_submit')
    map.connect('admin/photo_del_submit/:aid/:pid', controller='admin', action='photo_del_submit')
    map.connect('admin/photo_edit/:aid/:pid', controller='admin', action='photo_edit')
    map.connect('admin/photo_edit_submit/:aid/:pid', controller='admin', action='photo_edit_submit')

#    map.connect(':controller/:action/:id')
#    map.connect('*url', controller='template', action='view')

    return map
