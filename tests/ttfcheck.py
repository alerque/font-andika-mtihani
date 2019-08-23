# template config file for local testing of ttfs with fontbakery.

from fontbakery.callable import condition, check, disable
from fontbakery.constants import PriorityLevel
from fontbakery.message import Message
from fontbakery.checkrunner import (DEBUG, PASS, INFO, SKIP, WARN, FAIL, ERROR, Section)
from fontbakery.fonts_profile import profile_factory # NOQA pylint: disable=unused-import

profile = profile_factory(default_section=Section("SIL font project"))

# imports are used to mix in other external profiles
profile_imports = [
    ['fontbakery.profiles', ['cff', 'cmap', 'dsig', 'glyf', 'gpos', 'head', 'hhea', 'hmtx', 'kern', 'loca', 'name', 'opentype', 'os2', 'post', 'shared_conditions', 'googlefonts', 'adobefonts']]
]
# example of import params for SIL common profile and ABS profile directly in pysilfont
# profile_imports = ['silfont.fbtests.common', 'silfont.fbtests.abs']



# Our own checks below
# See https://font-bakery.readthedocs.io/en/latest/developer/writing-profiles.html

# putting this at the top of the file
# can give a quick overview:
expected_check_ids = (
    'org.sil.software/checks/helloworld',
    'org.sil.software/check/has-R'
)

# We use `check` as a decorator to wrap an ordinary python
# function into an instance of FontBakeryCheck to prepare
# and mark it as a check.
# A check id is mandatory and must be globally and timely
# unique. See "Naming Things: check-ids" below.
@check(id='org.sil.software/checks/helloworld')
# This check will run only once as it has no iterable
# arguments. Since it has no arguments at all and because
# checks should be idempotent (and this one is), there's
# not much sense in having it all. It will run once
# and always yield the same result.
def hello_world():
    """Simple "Hello (alphabets of the) World" example."""
    # The function name of a check is not very important
    # to create it, only to import it from another module
    # or to call it directly, However, a short line of
    # human readable description is mandatory, preferable
    # via the docstring of the check.

    # A status of a check can be `return`ed or `yield`ed
    # depending on the nature of the check, `return`
    # can only return just one status while `yield`
    # makes a generator out of it and it can produce
    # many statuses.
    # A status also always must be a tuple of (Status, Message)
    # For `Message` a string is OK, but for unit testing
    # it turned out that an instance of `fontbakery.message.Message`
    # can be very useful. It can additionally provide
    # a status code, better suited to figure out the exact
    # check result.
    yield PASS, 'Hello (alphabets of the) World'


@check(id='org.sil.software/check/has-R')
# This check will run once for each item in `fonts`.
# This is achieved via the iterag definition of font: fonts
def has_cap_r_in_name(font):
    """Filename contains an "R"."""
    # This test is not very useful again, but for each
    # input it can result in a PASS or a FAIL.
    if 'R' not in font:
        # This is our first check that can potentially fail.
        # To document this: return is also ok in a check.
        return FAIL, '"R" is not in font filename.'
    else:
        # since you can't return at one point in a function
        # and yield at another point, we always have to
        # use return within this check.
        return PASS, '"R" is in font filename.'



# skip checks (they still appear)
def check_skip_filter(checkid, font=None, **iterargs):
  if checkid in (
       'com.google.fonts/check/metadata/reserved_font_name'
      , 'com.google.fonts/check/description/broken_links'
      , 'com.google.fonts/check/name/rfn'
  ):
    return False, ('We do not want or care about these checks')
  return True, None

profile.check_skip_filter = check_skip_filter

# disable checks
def check_disable_filter(checkid, font=None, **iterargs):
  if checkid in (
       'com.google.fonts/check/metadata/reserved_font_name'
      , 'com.google.fonts/check/description/broken_links'
      , 'com.google.fonts/check/name/rfn'
  ):
    return False, ('We do not want or care about these checks')
  return True, None

profile.check_skip_filter = check_skip_filter
profile.check_disable_filter = check_disable_filter
profile.auto_register(globals())


