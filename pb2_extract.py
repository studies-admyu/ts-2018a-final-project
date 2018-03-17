#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

from data_processing.pb2.reader.pb2_document_reader import Pb2DocumentReader

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.stderr.write(
            'Need at least two arguments: <extract_dir> <gs_file1> ' +
            '[<gs_file2> ...]\n'
        )
        sys.exit(1)
    
    dir_to_extract = sys.argv[1]
    for filename in sys.argv[2:]:
        try:
            for image in Pb2DocumentReader(filename):
                with open(
                    os.path.join(
                        dir_to_extract, 
                        str(image.imageId.imageHash) + '.jpeg'),
                    'wb'
                ) as f:
                    f.write(image.content)
            
        except Exception as e:
            sys.stderr.write('ERROR: %s', str(e))
            continue
