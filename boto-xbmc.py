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
buckets = conn.get_all_buckets()

for bucket in buckets:
    if options.bucket:
        if not bucket.name == options.bucket:
                continue
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
                        continue

                    dest = bucket_path + '/' + os.path.splitext(key.name)[0] + '.strm'
                    src_url = key.generate_url(3600, query_auth=True, force_http=True)

                    try:
                        with open(dest, "w") as df:
                            df.write(src_url)
                    except S3ResponseError:
                        print 'Failed to write ' + dest
                        continue
    except S3ResponseError:
        print 'Failed to list bucket ' + bucket.name

print 'Done.'
