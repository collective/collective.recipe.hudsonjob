This recipe will render your config file for hudson and push it to the website.

Supported options
=================

The recipe supports the following options:

host (required)
    Hostname of your hudson instance.

jobname (required)
    Name of the job/project to create on Hudson.

template (this packages ships with default)
    Template ``config.xml`` that will be used to configure Hudson job.

port (80)
    Port of the job/project to create on Hudson.

username (None)
    For basic authentication specify username.

password (None)
    For basic authentication specify password.

config_name (hudson_config.xml)
    Name of generated configuration file that will get POSTed to Hudson.
    

Example usage
=============

We'll start by creating a buildout that uses the recipe::

    [add_to_hudson]
    recipe = collective.recipe.hudsonjob
    host = hudson.ploneboutique.com
    jobname = foobar
    port = 80
    username = test
    password = test
    template = %(path)s

    [hudson-conf]
    svn = http:// .
    git = ..

This will generate ``add_to_hudson`` command that will send your config to the
hudson (located as specified at add_to_hudson buildout section).

So run the buildout::
    
    $ bin/buildout
    Develop: '/home/ielectric/code/collective.recipe.hudsonjob/.'
    install_dir /home/ielectric/code/collective.recipe.hudsonjob/develop-eggs/tmpfg_pqRbuild
    Uninstalling add_to_hudson.
    Updating test.
    Installing add_to_hudson.
    Generated script '/home/ielectric/code/collective.recipe.hudsonjob/bin/add_to_hudson'.

Now we can see our configuration file at
``parts/collective.recipe.hudsonjob/hudson_config.xml``

And let's make new job at our hudson::

    $ bin/add_to_hudson

That's it! Your hudson has a new project, you may need to enter SCM
credentials the first time.

.. note:: Default template will render from *hudson-conf* section in buildout on every
buildout run. Template is done with Genshi.
