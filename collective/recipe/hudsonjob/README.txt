This recipe will render your config file for hudson and push it to the website.

Supported options for Hudson
============================

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


Supported variables for configuration template (``config.xml``)
===============================================================

description
    This description is placed on the project top page so that visitors can know what this job is about. You can use any HTML tags here. 
svn
    Pairs of URL and name of the checkout directory
git
    URL for the checkout
poll_scm
    This field follows the syntax of cron (with minor differences). Specifically, each line consists of 5 fields separated by TAB or whitespace:
    MINUTE HOUR DOM MONTH DOW
    MINUTE	Minutes within the hour (0-59)
    HOUR	The hour of the day (0-23)
    DOM	The day of the month (1-31)
    MONTH	The month (1-12)
    DOW	The day of the week (0-7) where 0 and 7 are Sunday.
    To specify multiple values for one field, the following operators are available. In the order of precedence,

    '*' can be used to specify all valid values.
    'M-N' can be used to specify a range, such as "1-5"
    'M-N/X' or '*/X' can be used to specify skips of X's value through the range, such as "*/15" in the MINUTE field for "0,15,30,45" and "1-6/2" for "1,3,5"
    'A,B,...,Z' can be used to specify multiple values, such as "0,30" or "1,3,5"
    Empty lines and lines that start with '#' will be ignored as comments.

    In addition, '@yearly', '@annually', '@monthly', '@weekly', '@daily', '@midnight', and '@hourly' are supported.

    Examples	
    # every minute
    * * * * *
    # every 5 mins past the hour 
    5 * * * *

shell
    Runs a shell script (defaults to sh, but this is configurable) for building the project. The script will be run with the workspace as the current directory. Type in the contents of your shell script. If your shell script has no header line like #!/bin/sh —, then the shell configured system-wide will be used, but you can also use the header line to write script in another language (like #!/bin/perl) or control the options that shell uses.
    By default, the shell will be invoked with the "-ex" option. So all of the commands are printed before being executed, and the build is considered a failure if any of the commands exits with a non-zero exit code. Again, add the #!/bin/... line to change this behavior.

    As a best practice, try not to put a long shell script in here. Instead, consider adding the shell script in SCM and simply call that shell script from Hudson (via bash -ex myscript.sh or something like that), so that you can track changes in your shell script.
        

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

    # template vars
    svn = http:// .
    description = foobar

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

Template will be rendered by buildout on every run. Templating is done with Genshi.

Adding template support for xml is really straight-forward, feel free to
contribute (but don't forget tests).
