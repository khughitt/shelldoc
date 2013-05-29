#!/usr/bin/env python
"""
Shell script report generator inspired by knitr.

Keith Hughitt <khughitt@umd.edu>

Examples
--------
shelldoc.py input.smd output.md
"""
import os
import re
import sys
import subprocess

def main():
    """Main function"""
    if(len(sys.argv) < 3):
        sys.exit("Error: please specify input and output files to use..")
    else:
        infile = sys.argv[1]
        outfile = sys.argv[2]

    # Modes
    # 0 = Markdown
    # 1 = Shellscript
    # 2 = Other code block
    _MODE_ = 0

    # check output file
    if os.path.exists(outfile):
        x = None

        while x not in ["y", "n", ""]:
            x = input("Specified output file exists. Overwrite? [Y/n] ").lower()
        if x == 'n':
            sys.exit()

    outfile = open(outfile, 'w')

    for line in open(infile, 'r'):
        cmds = []

        # start shell block
        if line.startswith('```{'):
            # detect language
            parts = re.match(r'```\{(\w*)([^\}]*)\}', line).groups()
            lang = parts[0]

            # shell
            if lang == 'bash':
                _MODE_ = 1
                continue
            # other
            else:
                _MODE_ = 2
                outfile.write('```%s\n' % lang)
                continue

        # end shell block
        elif line.startswith('```\n'):
            # @TODO: loosen immediate newline constraint
            if _MODE_ == 2:
                outfile.write('```\n')
            _MODE_ = 0
            continue

        # text
        if _MODE_ != 1:
            outfile.write(line)
        # shell command
        else:
            # print command
            outfile.write('```bash\n')
            outfile.write(line)
            outfile.write('```\n\n```\n')

            # Execute shell commands and inject output
            cmd = line.strip().split(' ')

            if '' in cmd:
                cmd.remove('')

            p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            out, err = p.communicate()

            # write result
            out = out.decode('utf-8')

            # prepend #'s
            out = out.replace('\n', '\n# ')[:-2]
            outfile.write("# %s" % out)
            outfile.write('```\n\n')

if __name__ == "__main__":
    main()