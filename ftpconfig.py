'''
Created on Sep 9, 2013

@author: WThiel
'''

class FtpConfig():

    def __init__(self, configfile):
        
        params = {}
        fr = open(configfile,'r')
        linesplit = []
        linevalues = []
        line = ""
        
        for line in fr:
            if len(line.strip()) > 0:
                if line.strip()[0] is not "#":
                    linesplit = line.split(":")
                    if len(linesplit) > 1:
                        print line.strip()
                        linevalues = [s.strip() for s in (":".join(linesplit[1:])).split(",")]
                        params[linesplit[0].strip()] = linevalues
        print ""
                        
        self.file_prefix = params['file_prefix'][0]
        self.file_index_list = params['file_index_list']
        self.file_suffix = params['file_suffix'][0]
        
        self.ftp_server = params['ftp_server'][0]
        self.ftp_directory = params['ftp_directory'][0]
        
        self.local_tempdata = params['local_tempdata'][0]
        self.local_psqldir = params['local_psqldir'][0]
        
        self.db_user = params['db_user'][0]
        self.db_port = params['db_port'][0]
        self.db_dbname = params['db_dbname'][0]
        self.db_tablename = params['db_tablename'][0]
        
        fr.close()
        