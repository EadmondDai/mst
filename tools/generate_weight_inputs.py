#!/usr/bin/env python

from generate_input import main as generate_input
from mstutil import get_path_to_tools_root
from optparse import OptionParser
import os, sys

def main(argv=sys.argv[1:]):
    usage = """usage: %prog [options]
Generates input for part 2 of the project en masse.

Examples:
    Generate inputs for 2D vertex placement in powers of 2 up to and including
    10000 vertices (10 inputs for each step):
        %prog -d2 -u10000 -n10

    Generate inputs for random edge weights in steps of 10 vertices up to and
    including 100 vertices (1 input for each step):
        %prog -a -s10 -u100"""
    parser = OptionParser(usage)
    parser.add_option("-a", "--additive-step-type",
                      action="store_true", default=False,
                      help="use additive stepping between numbers of vertices [default: multiplicative]")
    parser.add_option("-d", "--dims",
                      type="int", default=0,
                      help="number of dimensions to use; 0 => use random edge weights [default: %default]")
    parser.add_option("-g", "--go",
                      action="store_true", default=False,
                      help="run right away rather than generating inputs")
    parser.add_option("-l", "--min",
                      type="int", default=1,
                      help="minimum number of vertices to generate a graph for [default: %default]")
    parser.add_option("-n", "--num-per-step",
                      type="int", default=1, metavar="n",
                      help="number of inputs to generate for each step [default: %default]")
    parser.add_option("-s", "--step",
                      type="float", default=2.0,
                      help="step amount between vertex sizes (see -a) [default: %default]")
    parser.add_option("-u", "--max",
                      type="int", default=1024,
                      help="maximum number of vertices to generate a graph for [default: %default]")
    (options, args) = parser.parse_args(argv)
    if len(args) > 1:
        parser.error("too many arguments")

    if options.dims == 0:
        what = '-e 0.0,1.0'
    else:
        what = '-v %u,0.0,1.0' % options.dims

    if options.min < 1 or options.min > options.max:
        parser.error('-l must be in the range [1, max]')

    if options.max < 1:
        parser.error('-u must be at least 1')

    if options.additive_step_type:
        if options.step < 1.0:
            parser.error('-s must be greater than or equal to 1 when -a is used')
    elif options.step <= 1.0:
        parser.error('-s must be greater than 1 when -a is not used')

    v = options.min
    while True:
        for _ in range(options.num_per_step):
            if not options.go:
                args = '-p15 %s %u' % (what, int(v))
                try:
                    print 'generating new input: ' + args
                    ret = generate_input(args.split())
                except Exception, errstr:
                    print >> sys.stderr, 'generate_weight_inputs failed for: ' + args + ': ' + str(errstr)
                    return -1
                if ret != 0:
                    print >> sys.stderr, 'generate_weight_inputs failed for: ' + args
                    return -1
            else:
                cmd = get_path_to_tools_root() + 'run_test.py'
                cmd += " -G '-p15 %s %u' -n1" % (what, int(v))
                if os.system(cmd) != 0:
                    print >> sys.stderr, 'generate_weight_inputs GO mode failed for: ' + cmd
                    return -1

        if v >= options.max:
            break
        if options.additive_step_type:
            v += options.step
        else:
            v *= options.step
        if v > options.max:
            v = options.max

    return 0

if __name__ == "__main__":
    sys.exit(main())
