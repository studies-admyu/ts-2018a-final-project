#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import gzip

from data_processing.pb2.reader.gs_pb2 import document_length
from data_processing.pb2.reader.big_pb2 import ImageStruct

class Pb2DocumentReader:
    _DOCUMENT_LENGTH_SIZE = 5
    def __init__(self, path):
        self._stream = None
        self._filename = path
        
        if not os.path.isfile(path):
            raise Exception('File %s is not found' % (path))
        if path.endswith('.gz'):
            self._stream = gzip.open(path, 'rb')
        else:
            self._stream = open(path, 'rb')
    
    def __iter__(self):
        while True:
            document_len_struct = document_length()
            
            document_length_bytes = self._stream.read(
                self._DOCUMENT_LENGTH_SIZE
            )
            if len(document_length_bytes) < self._DOCUMENT_LENGTH_SIZE:
                return
            
            try:
                document_len_struct = document_length()
                document_len_struct.ParseFromString(
                    document_length_bytes
                )
                image_struct_size = document_len_struct.length
            
                img_struct_bytes = self._stream.read(image_struct_size)
                img_struct = ImageStruct()
                img_struct.ParseFromString(
                    img_struct_bytes
                )
                
                yield img_struct
            
            except Exception as e:
                raise Exception(
                    'Reading exception (%s): %s' % (self._filename, e)
                )
