# hashserv
Trustless and cryptographically audited public file server. Built on top of some of the work done on [MetaDisk](http://metadisk.org) and [DriveShare](http://driveshare.org) as part of the [Storj Project](http://storj.io).


#### 1. Uploading

A hashserv can accept, preferably encrypted, files and pieces of files. This data is uploaded via POST. Currently the size of the data that can be uploaded is limited to 32 MB. Files larger than that should be split, encrypted, and uploaded client side. 

#### 2. Auditing

The hashserv should list all files it is currently storing. All files are to be addressed by their hash. File name, and any other metadata should be discarded on upload. A cryptographical audit of each file should also be displayed. Where audits should be completed will be up to the settings of the hashserv node. 

In public mode, hashserv should use the latest Bitcoin blockchain hash, and Bitcoin blocks as its timescale. In private mode, the user who uploaded the file will be responsible issuing challenges.

#### 3. Downloading
Users may download files via GET by requesting the hash of the files. The data will most likely be encrypted and the user will have decrypt the file client side. 

#### 4. Exporting
Hashserv nodes should have a finite capacity for data storage. They should utilize other hashserv nodes, and DriveShare users to offload capacity. Data stored off node should be clearly marked as such.

#### 5. Payment
Early versions of this software will accept data freely within capacity limits. Upload and download actions should be metered, as this will be used to later charge uploaders and downloaders. 

