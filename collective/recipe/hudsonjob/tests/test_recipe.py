#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import sys
import os

import mocker
from zc.buildout.buildout import _buildout_default_options, _unannotate, Options

from collective.recipe.hudsonjob import *


_unannotate({'buildout': _buildout_default_options})

class TestHudson(unittest.TestCase):
    """"""

    def setUp(self):
        self.m = mocker.Mocker()
        self.name = 'add_to_hudson'
        self.buildout = {
            'buildout': _buildout_default_options,
        }
        self.buildout['buildout'].update({
            'directory': '/tmp/',
            'offline': 'true',
            # TODO: we need to dynamically figure out eggs and develop-eggs directory ... somehow.
            #'eggs-directory': '/home/ielectric/.buildout/eggs/',
            #'develop-eggs-directory': '/home/ielectric/code/collective.recipe.hudsonjob/',
        })
        self.options = Options(self.buildout, self.name, {
            'recipe': 'collective.recipe.hudsonjob',
            'host': 'localhost',
            'jobname': 'foobar',
        })
        if not os.path.exists('bin'):
            os.mkdir('bin')

    def tearDown(self):
        self.m.restore()

    def build_recipe(self):
        self.r = Recipe(self.buildout, self.name, self.options)

    # TESTS

    def test_add_to_hudson_success(self):
        self.build_recipe()
        obj = self.m.replace("urllib2.build_opener")
        obj()
        opener = self.m.mock()
        self.m.result(opener)
        opener.open(mocker.ANY)
        self.m.replay()

        add_to_hudson(self.r.options)

    def test_add_to_hudson_basic_auth_success(self):
        self.options['username'] = 'foobar'
        self.options['password'] = 'passwd'

        self.build_recipe()
        obj = self.m.replace("urllib2.build_opener")
        obj()
        opener = self.m.mock()
        self.m.result(opener)
        opener.add_handler(mocker.ANY)
        opener.open(mocker.ANY)
        self.m.replay()

        add_to_hudson(self.r.options)
        # TODO: assert for basicauthhandler
        # TODO: fire up http server?

    def test_recipe(self):
        self.build_recipe()
        self.assertTrue(self.r.options['output'].endswith('hudson_config.xml'))
        self.assertTrue(self.r.options['template'].endswith('collective.recipe.hudsonjob/collective/recipe/hudsonjob/default_config.xml.in'))
        self.assertTrue(self.r.options['jobname'].endswith('foobar'))
        self.assertTrue(self.r.options['host'].endswith('localhost'))
        self.assertTrue(self.r.options['config_name'].endswith('hudson_config.xml'))
        self.assertEqual(self.r.files, ['parts/collective.recipe.hudsonjob', 'bin/add_to_hudson'])

    def test_recipe_usererror_host(self):
        del self.options['host']
        self.assertRaises(UserError, self.build_recipe)

    def test_recipe_usererror_jobname(self):
        del self.options['jobname']
        self.assertRaises(UserError, self.build_recipe)

    def test_recipe_install_scripts(self):
        self.build_recipe()
        self.options._created = []
        self.r.install_scripts()

        # TODO: see if script exists

    def test_recipe_render_template(self):
        self.build_recipe()
        self.options._created = []
        self.r.render_hudson_config()

        # TODO: test if config is there

    def test_recipe_update_success(self):
        self.build_recipe()
        self.options._created = []
        self.r.update()


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestHudson))
    return suite
