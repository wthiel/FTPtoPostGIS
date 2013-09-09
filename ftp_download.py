'''
Created on Sep 4, 2013

@author: WThiel
'''
from ftplib import FTP
import zipfile
import os
import subprocess as sub
import sys
from ftpconfig import FtpConfig

def loadfiles(ftpconfig_file):
    print "Loading configuration from %s ..." % ftpconfig_file
    config = FtpConfig(ftpconfig_file)
    ftp = FTP(config.ftp_server)
    print(ftp)
    print(ftp.login())
    print(ftp.cwd(config.ftp_directory))
    datadir = config.local_tempdata.replace("/", "\\\\")
    
    for (i, fileindex) in enumerate(config.file_index_list):
        filename = '%s%s%s' % (config.file_prefix, fileindex, config.file_suffix)
        print '#############################################'
        print '%i of %i' % (i + 1, len(config.file_index_list))
        print 'Writing to local file %s/%s.zip' % (config.local_tempdata, filename)
        writefile = open('%s/%s.zip' % (config.local_tempdata, filename), 'wb')
        
        print 'Getting %s.zip' % filename
        print ('%.2f MB ...') % (ftp.size('%s.zip' % filename)/(1024.0*1024.0))
        ftp.retrbinary('RETR %s.zip' % filename, writefile.write)
    
        writefile.close()
    
        print 'Unzipping %s.zip' % filename
        with zipfile.ZipFile('%s/%s.zip' % (config.local_tempdata, filename), "r") as z:
            z.extractall('%s/' % config.local_tempdata)
        
        print 'Deleting %s.zip' % filename
        os.remove('%s/%s.zip' % (config.local_tempdata, filename))
        
        print 'Importing %s to PostGIS database:%s tablename:%s' % (filename, config.db_dbname, config.db_tablename)
        sub.check_output("\"%s\\shp2pgsql\" -a -s 4269 \"%s\\%s.shp\" %s | \"%s\\psql\" -p %s -U %s -d %s" 
                           % (config.local_psqldir, datadir, filename, config.db_tablename, config.local_psqldir, config.db_port, config.db_user, config.db_dbname), shell=True)
    
    print '#############################################'
    print 'Finished'

if __name__ == '__main__':
    loadfiles(sys.argv[1])
