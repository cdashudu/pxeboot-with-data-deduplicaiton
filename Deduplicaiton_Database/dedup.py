import time
import hashlib
import os
import sys
import MySQLdb
class DuplicateKeyError(Exception): pass

class SingleSet(set):
    def add(self, value):
        if vlaue in self:
            raise DuplicateKeyError('Value {!r} already present'.format(value))
        super().add(value)

    def update(self, values):
        error_values = []
        for value in values:
            if value in self:
                error_values.append(value)
        if error_values:
            raise DuplicateKeyError('Value(s) {!r} already present'.format(
                                    error_values))
        super().update(values)

my_set = SingleSet()

def connect_db():
    #Add error handling
    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                         user="root",         # your username
                         passwd="Root!23",  # your password
                         db="ESA")        # name of the data base
    return db

def fixedLengthDeduplication(filename, filepath, username):
    sequence_no=0
    inc=4096 #block size
    f = open(os.path.join(filepath, filename), "rb")  

    data=f.read()
    f.close()
    bytes=len(data)
    fileNames=[]
    db=connect_db()
    
    for i in range(0, bytes+1, inc):
        #VARIABLES
        #FINGERPRINT_ID
        #FILEPATH_ID
        sequence_no=sequence_no+1
        print(sequence_no)

        hash_md5=hashlib.md5()
        hash_md5.update(data[i:i+inc])
        fn = "file%s" % hash_md5.hexdigest() #FileName of the file chunk

        #put the chunk with file name as the hashed value in the folder
        f = open( os.path.join('/home/cs/ESA_project/programs/hashedfile/', fn), 'wb') 
        f.write(data[i:i+inc]) #Write the file chunk
        f.close()

        hashVal=str(hash_md5.hexdigest())
        

#########insert the filepath mapping
        print("Inserting filepath mapping")
        print(time.asctime( time.localtime(time.time())))
        cursor1 = db.cursor()

        hash_md5_filePath = hashlib.md5()
        hash_md5_filePath.update(filepath)
        filePathHash = hash_md5_filePath.hexdigest()

        querytoInsertFilePath= """INSERT INTO PATH_MAPPING (PATHNAME, PATHHASH)
        SELECT * FROM (SELECT '%(path)s','%(pathHash)s') AS tmp
        WHERE NOT EXISTS (
        SELECT PATHNAME, PATHHASH FROM PATH_MAPPING WHERE PATHHASH='%(pathHash)s'
        );""" %{'path':filepath, 'pathHash' : filePathHash} 
        
        cursor1.execute(querytoInsertFilePath) #Execute Insert query
        
        queryToGetFilePathID="""SELECT PATH_MAPPING_ID 
        from PATH_MAPPING 
        where PATHHASH='%(pathHash)s'"""%{'pathHash':filePathHash}

        cursor1.execute(queryToGetFilePathID) #Execute the Select query
        
        FILEPATH_ID = cursor1.fetchone()[0] #collect the PATH_ID        
        print("END of Inserting filepath mapping")
        print(time.asctime( time.localtime(time.time())))

########insert entry in Hash table
        print("Inserting hash table")
        print(time.asctime( time.localtime(time.time())))

        cursor2 = db.cursor()
        
        queryToInsertFingerPrint="""INSERT INTO HASH_TABLE (FINGERPRINT) 
        SELECT * FROM (SELECT '%(hash)s') AS tmp
        WHERE NOT EXISTS (
        SELECT FINGERPRINT FROM HASH_TABLE WHERE FINGERPRINT='%(hash)s'
        );""" %{'hash':hashVal}
        
        cursor2.execute(queryToInsertFingerPrint) #Insert the Hash in HASH TABLE

        queryToGetHashID="""select HASH_ID 
        from HASH_TABLE 
        where FINGERPRINT='%(hash)s'"""%{'hash':hashVal}
        
        cursor2.execute(queryToGetHashID) #Get the HASH ID for the INSERTED HASH
        FINGERPRINT_ID=cursor2.fetchone()[0]
        
        print("END of Inserting hashtable")
        print(time.asctime( time.localtime(time.time())))

#########insert entry in user table
        
        print("Inserting user table")
        print(time.asctime( time.localtime(time.time())))
        
        cursor3 = db.cursor()

        queryToInsertUserFileData="""INSERT INTO `ESA`.`USERS`
        (
        `USERNAME`,
        `FILENAME`,
        `FILE_LOCATION_ID`)
         VALUES
        ('%(username)s', '%(filename)s', '%(filepathID)s');
        """ %{'filename':filename, 'filepathID' : FILEPATH_ID ,'username': username}
        
        cursor3.execute(queryToInsertUserFileData)

        print("END of Inserting user table")
        print(time.asctime( time.localtime(time.time())))

#########insert entry in mapping table
        
        print("Inserting file mapping table")
        print(time.asctime( time.localtime(time.time())))
        
        cursor4 = db.cursor()
        
        queryToInsertFileMapping="""INSERT INTO `ESA`.`FILE_MAPPING`
        (`FILENAME`,
        `FILEPATH_ID`,
        `HASH_ID`,
        `FILE_SEQUENCE`)
         VALUES
        ('%(filename)s', '%(filepathID)s', '%(hashID)s', '%(fileSeq)s');
        """ %{'filename':filename, 'filepathID' : FILEPATH_ID ,'hashID': FINGERPRINT_ID, 'fileSeq':sequence_no  } 
        
        cursor4.execute(queryToInsertFileMapping)
        
        print("Inserting file mapping table")
        print(time.asctime( time.localtime(time.time())))

        # commit your changes
        db.commit()


fixedLengthDeduplication("test.mp4","/home/cs/ESA_project", "chandu")

