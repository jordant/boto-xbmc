#!/usr/bin/env python
from boto.s3.connection import S3Connection
from boto.exception import S3ResponseError
import os
import optparse
import sys

parser = optparse.OptionParser()
parser.add_option('--access', '-a', action='store')
parser.add_option('--secret', '-s', action='store')
parser.add_option('--path', '-p', default='.', action='store')
parser.add_option('--bucket', '-b', action='store')
parser.add_option('--allbuckets', '-A', action='store_true')
parser.add_option('--host', default='objects.dreamhost.com', action='store')

options, remainder = parser.parse_args()


d = os.path.dirname(options.path + "/")
if not os.path.exists(d):
   print 'Creating path ' + options.path
   os.makedirs(d)

conn = S3Connection(options.access, options.secret, host=options.host)

buckets = ()

if options.bucket:
    try:
        bucket = conn.get_bucket(options.bucket)
    except:
        print 'Error: Cannot find bucket ' + options.bucket
        sys.exit()
    buckets = bucket
elif options.allbuckets:
    buckets = conn.get_all_buckets()

for bucket in buckets:
    print 'Bucket ' + bucket.name
    bucket_path = options.path + "/" + bucket.name + "/"
    b = os.path.dirname(bucket_path)
    if not os.path.exists(b):
        print 'Creating Bucket Path ' + bucket_path
        os.makedirs(b)
    try:
        for key in bucket.list():
            if not key.name.startswith('.'):
                    if key.name.endswith('/'):
                        kf = os.path.dirname(bucket_path + key.name)
                        if not os.path.exists(kf):
                                print "Create folder " + key.name
                                os.makedirs(kf)
                    dest = bucket_path + '/' + key.name + '.strm'
                    src_url = key.generate_url(0, query_auth=True, force_http=True)
                    try:
                        with open(dest, "a") as df:
                            df.write(src_url)
                    except S3ResponseError:
                        print 'Failed to write ' + dest
                        continue
    except S3ResponseError:
        print 'Failed to list bucket ' + bucket.name

print 'Done.'
