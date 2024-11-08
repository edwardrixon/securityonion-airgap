#!/usr/bin/python
# Created by https://github.com/SkiTheSlicer
# Updated by https://github.com/edwardrixon

#from securityonion_airgap_download import compare_md5s

def parse_arguments():
  import argparse
  import os
  import sys
  parser = argparse.ArgumentParser(
    prog='securityonion_airgap_update.py',
    description='Update tools within Security Onion.',
    epilog='Created by SkiTheSlicer (https://github.com/SkiTheSlicer)')
  parser.add_argument('-f', '--input-file',
                      nargs='?',
                      help='Specifies compressed archive containing updates')
  parser.add_argument('-g', '--geoip',
                      action='store_true',
                      help='Perform Bro GeoIP updates only.')
  parser.add_argument('-r', '--rules',
                      action='store_true',
                      help='Perform Snort rule updates only.')
  parser.add_argument('-i', '--ip2c',
                      action='store_true',
                      help='Perform SQueRT ip2c updates only.')
  return parser.parse_args()

def decompress_tarfile(file_to_decompress):
  import os
  import tarfile
  import sys
  if not os.path.isdir(file_to_decompress) and file_to_decompress.endswith('.tar.gz'):
    print "Decompressing " + file_to_decompress + "..."
    with tarfile.open(file_to_decompress) as tar:
      tar.extractall()
  else:
    print "ERROR: Invalid tar file."
    sys.exit(1)

def main():
  import os
  import sys
  from securityonion_airgap_download import compare_md5s
  import subprocess
  args = parse_arguments()
  if not os.path.exists(args.input_file):
    print 'ERROR: ' + args.input_file + ' doesn\'t exist. Exitting.'
    sys.exit(1)
  elif os.path.isdir(args.input_file):
    #for f in os.listdir(args.input_file):
    #  file = os.join(args.input_file, f)
    print 'ERROR: Script currently doesn\'t support crawling a directory. Exitting.'
      #Maybe list dir, select newest tarball, and overwrite value of args.input_file. Then change next elseif to just if.
    sys.exit(1)
  elif not os.path.isdir(args.input_file):
    print '\n[MAIN: Setup]'
    if os.path.exists('.'.join([args.input_file, 'md5'])):
      compare_md5s(os.path.dirname(os.path.abspath(args.input_file)))
    decompress_tarfile(args.input_file)
    base_dir = args.input_file[:-7]
    print 'Base Dir: ' + base_dir
    script_dir = os.path.dirname(os.path.realpath(__file__))
    #ip2c_script = script_dir + '/squert_ip2c_update.py'
    #ip2c_cmd = script_dir + '/squert_ip2c_update.py -d ' + os.path.join(base_dir, 'RIR')
    ids_script = script_dir + '/ids_offline_update.py'
    #print os.path.abspath(base_dir)
    if args.rules:
      print '\n[MAIN -> IDS: Snort Rules]'
      # what about Doing blacklist?
      subprocess.call(['python', ids_script, '--rules', '-R' + os.path.join(os.path.abspath(base_dir), 'Snort')])
    else:
      print '\n[MAIN -> IDS: Blacklists, Rules]'
      subprocess.call(['python', ids_script, '-B' + os.path.join(os.path.abspath(base_dir), 'Snort', 'Blacklist'), '-R' + os.path.join(os.path.abspath(base_dir), 'Snort')])
     # print '\n[MAIN -> IP2C]'
      #subprocess.call(['python', ip2c_script, '-d' + os.path.join(os.path.abspath(base_dir), 'RIR')])
      print '\nFinished!'

if __name__ == "__main__":
  main()
