"""
Poll for new screenshots on the desktop and rename them into a new directory.
"""
import re
import os
import sys
import time
import glob

DIR_NAME                = "Desktop"
SCREENSHOT_DIR          = os.path.join(os.getenv("HOME"), DIR_NAME)
SCREENSHOT_EXTENSION    = "png"
SCREENSHOT_PATTERN      = r'^Screen Shot \d\d(.*)\.%s$' % SCREENSHOT_EXTENSION
POLLING_DELAY           = 4

def _get_new_directory_name(arg1):
    if arg1 in ['', None]:
        raise ValueError("Please specify a dest.")
    new_dir_name = os.path.join(SCREENSHOT_DIR, arg1)
    if not os.path.exists(new_dir_name):
        print "Creating directory: %s" % new_dir_name
        os.mkdir(new_dir_name)
    return new_dir_name

def _files_matching_regex(dirname, pat):
    wildcard_path = os.path.join(dirname, '*')
    all_files = [os.path.basename(n) for n in glob.glob(wildcard_path)]
    return set([m for m in all_files if bool(re.search(pat, m))])

def main(*args):
    print "Polling for new files every %d seconds matching this pattern /%s/ in '%s'." % \
         (POLLING_DELAY, SCREENSHOT_PATTERN, SCREENSHOT_DIR)

    if not os.path.exists(SCREENSHOT_DIR):
        raise ValueError("Not found: '%s'" % SCREENSHOT_DIR)
    if not os.path.isdir(SCREENSHOT_DIR):
        raise ValueError("Not directory: '%s'" % SCREENSHOT_DIR)

    if len(args) != 2:
        raise ValueError("script takes 1-- the name of the destination directory.")
    new_dir = _get_new_directory_name(args[1])
    session_name = os.path.basename(new_dir)
    existed_already = _files_matching_regex(SCREENSHOT_DIR, SCREENSHOT_PATTERN)

    def _get_new_screenshots():
        matching_files = _files_matching_regex(SCREENSHOT_DIR, SCREENSHOT_PATTERN)
        return sorted(list(matching_files - existed_already))

    def _place_file(filename):
        # Make sure the original file exists.
        opath = os.path.join(SCREENSHOT_DIR, filename)
        assert os.path.exists(opath)

        # Figure out the next (available) name.
        numcatch_re = r'^%s(\d+)\.%s$' % (session_name, SCREENSHOT_EXTENSION)
        already_placed = _files_matching_regex(new_dir, numcatch_re)
        if len(already_placed) is 0:
            index = 0
        else:
            index = max([int(re.match(numcatch_re, fn).groups()[0]) for fn in already_placed])
        next_i = index + 1
        nextname = "%s%d" % (session_name, next_i)
        nextpath = "%s.%s" % (os.path.join(new_dir, nextname), SCREENSHOT_EXTENSION)

        # ensure that the file won't conflict with another
        assert not os.path.exists(nextpath)
        # assert that the directory hasn't moved.
        assert os.path.exists(new_dir) and os.path.isdir(new_dir)

        print "Moving '%s' to '%s'" % (opath, nextpath)
        os.rename(opath, nextpath)

    try:
        while True:
            new_ones = _get_new_screenshots()
            for new_file in _get_new_screenshots():
                _place_file(new_file)
            time.sleep(POLLING_DELAY)
    except KeyboardInterrupt, e:
        for new_file in _get_new_screenshots():
            _place_file(new_file)
        sys.exit(0)

if __name__=="__main__":
    main(*list(sys.argv))