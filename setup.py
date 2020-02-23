import os

import distutils.cmd
import distutils.log
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.txt")) as f:
    README = f.read()
with open(os.path.join(here, "CHANGES.txt")) as f:
    CHANGES = f.read()

requires = [
    "pyramid",
    "pyramid_chameleon",
    "pyramid_debugtoolbar",
    "pyramid_tm",
    "SQLAlchemy",
    "transaction",
    "zope.sqlalchemy",
    "waitress",
    "mako",
    "pyramid_mako",
    "docutils",
    "pillow",
    "pyrss2gen",
    "alembic",
    "pyyaml",
    "click",
    "python-dateutil",
]


class CustomCommand(distutils.cmd.Command):
    """
    Customize commands for setup scripts.
    """

    description = "Custom commands"
    user_options = [
        # The format is (long option, short option, description).
        ("action=", "a", "Specify the action: [extract_i18n]"),
    ]

    def initialize_options(self):
        """Set default values for options."""
        # Each user option must be listed here with their default value.
        self.action = "doc"

    def finalize_options(self):
        """Post-process options."""

    def run(self):
        """Run command."""
        if self.action == "extract_i18n":
            dir_name = "weblog/locale/zh_CN/LC_MESSAGES"
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            dir_name = "weblog/locale/en/LC_MESSAGES"
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            os.system(
                "pot-create  ./ -c ./lingua.ini -o " "weblog/locale/weblog.pot"
            )

            prefix = "/usr/local/Cellar/gettext/0.19.7/bin/"
            cmd_cn = (
                "%smsgmerge --update "
                "weblog/locale/zh_CN/LC_MESSAGES/weblog.po "
                "weblog/locale/weblog.pot"
            ) % prefix
            cmd_en = (
                "%smsgmerge --update -q "
                "weblog/locale/en/LC_MESSAGES/weblog.po "
                "weblog/locale/weblog.pot"
            ) % prefix

            self.announce(cmd_cn, distutils.log.INFO)
            os.system(cmd_cn)
            self.announce(cmd_en, distutils.log.INFO)
            os.system(cmd_en)


setup(
    name="weblog",
    version="0.3.5",
    description="weblog",
    long_description=README + "\n\n" + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author="",
    author_email="",
    url="",
    keywords="web wsgi bfg pylons pyramid",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite="weblog",
    install_requires=requires,
    entry_points="""\
      [paste.app_factory]
      main = weblog:main
      [console_scripts]
      weblog_initdb = weblog.scripts.initializedb:main
      weblog_load_posts = weblog.scripts.load_posts:main
      """,
    cmdclass={"weblog": CustomCommand},
)
