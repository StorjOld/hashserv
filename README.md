# hashserv
Trustless and cryptographically audited public file server. Built on top of some of the work done on [MetaDisk](http://metadisk.org) and [DriveShare](http://driveshare.org) as part of the [Storj Project](http://storj.io).

#### 1. Uploading
A hashserv can accept preferably encrypted files and pieces of files. This data is uploaded via POST. Currently the size of the data that can be uploaded is limited to 32 MB. Files larger than that should be split, encrypted, and uploaded client side. 
