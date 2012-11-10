from subprocess import *
from os.path import join
import re
import sys

cmd_names = [
    'info',
    'list',
    'depends',
    'search',
    'locations',
    'envs',
    'create',
    'install',
    'upgrade',
    'activate',
    'deactivate',
    'download',
    'remove',
    'upgrade2pro'
]

def scrape_help(cmd_name):

    cmd = "CIO_TARGET='ce' COLUMNS=1000 conda %s -h" % cmd_name

    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)

    output = p.stdout.read()

    # groups:                ----1---- -----2----
    usage_pat = re.compile(r'(^usage): (conda .*)\n')
    usage = usage_pat.search(output)

    # groups:                          --1-
    desc_pat = re.compile(r'usage.*\n\n(.*)\n\n')
    desc = desc_pat.search(output)

    # groups:                                               --1--   --2-
    positional_pat = re.compile(r'positional arguments:\n\s+(\w*)\s+(.*)\n')
    pos = positional_pat.search(output)

    # groups:                            ---1--
    optional_pat = re.compile(r'(optional(.*\n)*)$')
    opt = optional_pat.search(output)

    if opt:
        options = opt.group(1)

        yn_pat = re.compile(r'{.*}')
        options = yn_pat.sub('', options)

        rd_pat = re.compile(r'(default: )(.*/anaconda)')
        options = rd_pat.sub(r"\1ROOT_DIR", options)

        in_pat = re.compile(r'(in )(.*/anaconda)')
        options = in_pat.sub(r"\1ROOT_DIR", options)

    else:
        options = ''

    output = desc.group(1)

    output += "\n\n**%s**: ``%s``\n\n" % (usage.group(1), usage.group(2))

    if pos:
        output += "*%s*\n\t%s\n\n" % (pos.group(1), pos.group(2))

    output += options

    return output

    

if __name__ == '__main__':
    for name in cmd_names:
        output = scrape_help(name)

        path = "/tmp"
        if len(sys.argv) > 1:
            path = sys.argv[1]
        outpath = join(path, "%s.txt" % name)

        print "Scraping help for '%s' -> %s" % (name, outpath)

        outfile = open(outpath, "w")
        outfile.write(output)
        outfile.close()