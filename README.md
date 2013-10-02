boto-xbmc
=========

Uses boto to create a directory structure/strm files from S3 buckets and objects , that can be scrapped by XBMC. This allows you to stream your media library directly from any S3 endpoint.

## Usage
./boto-xbmc.py -a ACCESS_KEY_ID -s SECRET -A -p /home/user/media 

## Features
* Single bucket or All buckets

## Requirements
*  python-boto (https://github.com/boto/boto)
