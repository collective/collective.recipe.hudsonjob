# -*- coding: utf-8 -*-
"""Recipe hudson"""

import os
import sys
import urllib2
import logging

import zc.recipe.egg
from zc.buildout import UserError
from collective.recipe.template.genshitemplate import Recipe as GenshiRecipe


class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        self.egg = zc.recipe.egg.Scripts(buildout, self.options['recipe'], options)

        if 'host' not in self.options:
            raise UserError('You forgot to set "host" of the hudson in section "%s"' % self.options['recipe'])
        if 'jobname' not in self.options:
            raise UserError('You forgot to set "jobname" to create at hudson in section "%s"' % self.options['recipe'])

        self.options.setdefault('port', '80')
        self.options.setdefault('template', os.path.join(os.path.dirname(__file__), 'default_config.xml.in'))
        self.options.setdefault('config_name', 'hudson_config.xml')
        self.options.setdefault('username', '')
        self.options.setdefault('password', '')

        # figure out default output file
        plone_hudson = os.path.join(self.buildout['buildout']['parts-directory'], __name__)
        if not os.path.exists(plone_hudson):
            os.makedirs(plone_hudson)

        # setup input/output file
        self.options['input'] = self.options['template']
        self.options['output'] = os.path.join(plone_hudson, self.options['config_name'])

        # what files are tracked by this recipe
        self.files = [plone_hudson,
            os.path.join(self.buildout['buildout']['bin-directory'], self.name)]

    def install_scripts(self):
        # generate script add_to_hudson
        zc.buildout.easy_install.scripts(
            [(self.name, 'collective.recipe.hudsonjob', 'add_to_hudson')],
            self.egg.working_set()[1],
            self.buildout[self.buildout['buildout']['python']]['executable'],
            self.buildout['buildout']['bin-directory'],
            arguments=self.options.__repr__(),
        )

    def render_hudson_config(self):
        """render our hudson template"""
        g = GenshiRecipe(self.buildout, self.name, self.options)
        g.install()

    def install(self):
        """Installer"""
        self.render_hudson_config()
        self.install_scripts()

        # Return files that were created by the recipe. The buildout
        # will remove all returned files upon reinstall.
        return self.files

    def update(self):
        """Update template"""
        self.install()


def add_to_hudson(options):
    """Makes HTTP POST request to hudson to add new job.

    :param options: Configuration to hudson instance
    :type options: dict

    """
    host = "http://%(host)s:%(port)s/createItem?name=%(jobname)s" % options
    headers = {
        "Content-Type": "application/xml; charset=utf-8",
    }
    opener = urllib2.build_opener()
    if options.get('username', None):
        auth_handler = urllib2.HTTPBasicAuthHandler()
        auth_handler.add_password(
            realm='Hudson',
            uri=host,
            user=options['username'],
            passwd=options['password'])
        opener.add_handler(auth_handler)

    # upload hudson config
    params = open(options['output']).read()
    try:
        print "Creating new job at %s" % host
        opener.open(urllib2.Request(host, params, headers))
    except urllib2.HTTPError as e:
        print e
        print "\t(does the job maybe already exists?)"
        sys.exit(2)
    else:
        print "Done."
