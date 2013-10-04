boto-xbmc
=========

Uses boto library to create STRM files from object stores such as DreamHost Objects
(DHO) and Amazon S3. The leftover STRM files/directories can be scrapped by
XBMC and streamed directly from the object store.

## Usage
./boto-xbmc.py -a ACCESS_KEY_ID -s SECRET -A -p /home/user/media 

## Features
* Single bucket or All buckets

## Requirements
*  python-boto (https://github.com/boto/boto)
