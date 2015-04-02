# hashserv
Trustless and cryptographically audited public file server. Built on top of some of the work done on [MetaDisk](http://metadisk.org) and [DriveShare](http://driveshare.org) as part of the [Storj Project](http://storj.io).

## Functional Summary

#### 1. Uploading

A hashserv can accept, preferably encrypted, files and pieces of files. This data is uploaded via POST. Currently the size of the data that can be uploaded is limited to 32 MB. Files larger than that should be split, encrypted, and uploaded client side. 

#### 2. Auditing

The hashserv should list all files it is currently storing. All files are to be addressed by their hash. File name, and any other metadata should be discarded on upload. A cryptographical audit of each file should also be displayed. When audits should be completed will be up to the settings of the hashserv node. 

For public audits, hashserv should use the latest Bitcoin blockchain hash, and Bitcoin blocks as its timescale. For private audits, the user who uploaded the file will be responsible for issuing and verifying challenges.

#### 3. Downloading
Users may download files via GET by requesting the hash of the files. The data will most likely be encrypted and the user will have to decrypt the file client side. The hashserv node may also choose to serve decrypted content over HTTP. 

#### 4. Exporting
Hashserv nodes  have a finite capacity for data storage. They may utilize other hashserv nodes, and [DriveShare](http://driveshare.org) users to offload capacity. Data stored off node should be clearly marked as such.

#### 5. Payment
Early versions of this software will accept data freely within capacity limits. Upload and download actions should be metered, as this will be used to later charge uploaders and downloaders. 

## 1. Upload API

Upload a file to a hashserv node:

    POST /api/upload
    Parameters:
    - file

## 3. Download API

Download a file from a hashserv node:
	
	GET /api/download/<filehash>
    Parameters:
	- filehash

Serve a file from a hashserv node:

	GET /api/serve/<filehash>/<file_extension>
    Parameters:
	- filehash, file_extension