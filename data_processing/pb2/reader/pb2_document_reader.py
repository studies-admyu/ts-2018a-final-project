#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import gzip

from data_processing.pb2.reader.gs_pb2 import document_length
from data_processing.pb2.reader.big_pb2 import ImageStruct

class Pb2DocumentReader:
    _DOCUMENT_LENGTH_SIZE = 5
    def __init__(self, path, yield_exceptions = False):
        self._stream = None
        self._yield_exceptions = yield_exceptions
        
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
            
            occured_exception = None
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
            
            except Exception as e:
                occured_exception = e
                if not self._yield_exceptions:
                    raise occured_exception
                else:
                    img_struct = None
            
            if self._yield_exceptions:
                yield img_struct, occured_exception
            else:
                yield img_struct
