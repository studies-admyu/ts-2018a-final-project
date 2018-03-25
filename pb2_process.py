#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import io
import json
import os
import sys
import tarfile

from multiprocessing import Pool
from shutil import copy2

import numpy as np
from PIL import Image

from data_processing.pb2.reader.pb2_document_reader import Pb2DocumentReader
from data_processing.pb2.analyzer.photobank_analyzer import PhotobankAnalyzer

IMAGE_FILE_TYPE = 'image'
GS_FILE_TYPE = 'gs'
TAR_FILE_TYPE = 'tar'

ANALYZE_OUTPUT_FILENAME_PATTERN = 'analyze_out_%s.jsonl'
RFITLER_OUTPUT_FILENAME_PATTERN = 'rfilter_out_%s.jsonl'

PI4 = np.arctan(1) * 16.0
MIN_HEIGHT = 200
MIN_WIDTH = 200
MIN_FACE_RATIO = 0.00075

def _run_mp(proc_num, fun, split_args):
    if not isinstance(proc_num, int) or (proc_num < 1):
        raise Exception(
            'Bad processes number \'%s\'' % (proc_num)
        )
    if len(split_args) != proc_num:
        raise Exception(
            'Split args count doesn\'t correspond to processes number'
        )
    
    processes_pool = Pool(processes = proc_num)
    processes_pool.map(fun, split_args)
    processes_pool.close()
    processes_pool.join()

def _split_args(proc_num, args_list):
    split_args_list = []
    split_size = (
        len(args_list) // proc_num + 
        (1 if len(args_list) % proc_num > 0 else 0)
    )
    
    for i in range(proc_num):
        split_args_list.append(args_list[split_size * i: split_size * (i + 1)])
    
    return split_args_list

def _unglob_files(files):
    files_found = []
    for file in files:
        globs_list = glob.glob(file)
        if not os.path.exists(file) and (len(globs_list) > 0):
            files_found.extend(globs_list)
        else:
            files_found.append(file)
    return files_found

def _analyze(exec_details):
    output_file, image_files = exec_details[0], exec_details[1]
    analyzer = PhotobankAnalyzer()
    
    with open(output_file, 'w') as o:
        for image_file in image_files:
            if not os.path.isfile(image_file):
                sys.stderr.write('Warning: file %s not found\n' % (image_file))
                continue
            try:
                rgb_image = Image.open(image_file)
                report_dict = {'filename': image_file, 'type': IMAGE_FILE_TYPE}
                report_dict.update(analyzer.analyze(rgb_image))
                o.write(json.dumps(report_dict) + '\n')
            except Exception as e:
                sys.stderr.write(
                    'WARNING: Error during %s processing: %s\n' % (
                        image_file, str(e)
                    )
                )
                continue

def analyze(output_file, image_files):
    image_files_found = _unglob_files(image_files)
    return _analyze((output_file, image_files_found))

def analyze_mp(proc_num, output_dir, image_files):
    image_files_found = _unglob_files(image_files)
    split_image_files = _split_args(proc_num, image_files_found)
    
    index_digits = int(np.log10(proc_num)) + 1
    output_filename_pattern = (
        ANALYZE_OUTPUT_FILENAME_PATTERN % ('%0' + str(index_digits) + 'u')
    )
    
    args_to_run = [
        (
            os.path.join(output_dir, output_filename_pattern % (i)),
            split_image_files[i]
        )
        for i in range(proc_num)
    ]
    
    # Prepare analyzer
    PhotobankAnalyzer()
    
    _run_mp(proc_num, _analyze, args_to_run)

def _analyze_gs(exec_details):
    output_file, gs_files = exec_details[0], exec_details[1]
    analyzer = PhotobankAnalyzer()
    
    with open(output_file, 'w') as o:
        for gs_file in gs_files:
            if not os.path.isfile(gs_file):
                sys.stderr.write('Warning: file %s not found\n' % (gs_file))
                continue
            for image_doc in Pb2DocumentReader(gs_file):
                try:
                    image_data = io.BytesIO(image_doc.content)
                    rgb_image = Image.open(image_data)
                    report_dict = {
                        'filename': gs_file, 'type': GS_FILE_TYPE,
                        'member': str(image_doc.imageId.imageHash)
                    }
                    report_dict.update(analyzer.analyze(rgb_image))
                    o.write(json.dumps(report_dict) + '\n')
                except Exception as e:
                    sys.stderr.write(
                    'WARNING: Error during %s:%s processing: %s\n' % (
                        gs_file, report_dict['member'], str(e)
                        )
                    )
                    continue

def analyze_gs(output_file, gs_files):
    gs_files_found = _unglob_files(gs_files)
    return _analyze_gs((output_file, gs_files_found))

def analyze_mp_gs(proc_num, output_dir, gs_files):
    gs_files_found = _unglob_files(gs_files)
    split_gs_files = _split_args(proc_num, gs_files_found)
    
    index_digits = int(np.log10(proc_num)) + 1
    output_filename_pattern = (
        ANALYZE_OUTPUT_FILENAME_PATTERN % ('%0' + str(index_digits) + 'u')
    )
    
    args_to_run = [
        (
            os.path.join(output_dir, output_filename_pattern % (i)),
            split_gs_files[i]
        )
        for i in range(proc_num)
    ]
    
    # Prepare analyzer
    PhotobankAnalyzer()
    
    _run_mp(proc_num, _analyze_gs, args_to_run)

def _analyze_tar(exec_details):
    output_file, tar_files = exec_details[0], exec_details[1]
    analyzer = PhotobankAnalyzer()
    
    with open(output_file, 'w') as o:
        for tar_file in tar_files:
            if not os.path.isfile(tar_file):
                sys.stderr.write('Warning: file %s not found\n' % (tar_file))
                continue
            if not tarfile.is_tarfile(tar_file):
                sys.stderr.write(
                    'Warning: file %s is not a valid tar archive\n' %
                    (tar_file)
                )
                continue
            with tarfile.open(tar_file, 'r') as itar:
                for image_info in itar.getmembers():
                    if not image_info.isfile():
                        continue
                    with itar.extractfile(image_info) as f:
                        try:
                            rgb_image = Image.open(f)
                            report_dict = {
                                'filename': tar_file, 'type': TAR_FILE_TYPE,
                                'member': image_info.name
                            }
                            report_dict.update(analyzer.analyze(rgb_image))
                            o.write(json.dumps(report_dict) + '\n')
                        except Exception as e:
                            sys.stderr.write(
                                (
                                    'WARNING: Error during %s:%s ' +
                                    'processing: %s\n'
                                ) % (
                                    tar_file, report_dict['member'], str(e)
                                )
                            )
                            continue

def analyze_tar(output_file, tar_files):
    tar_files_found = _unglob_files(tar_files)
    return _analyze_tar((output_file, tar_files_found))

def analyze_mp_tar(proc_num, output_dir, tar_files):
    tar_files_found = _unglob_files(tar_files)
    split_tar_files = _split_args(proc_num, tar_files_found)
    
    index_digits = int(np.log10(proc_num)) + 1
    output_filename_pattern = (
        ANALYZE_OUTPUT_FILENAME_PATTERN % ('%0' + str(index_digits) + 'u')
    )
    
    args_to_run = [
        (
            os.path.join(output_dir, output_filename_pattern % (i)),
            split_tar_files[i]
        )
        for i in range(proc_num)
    ]
    
    # Prepare analyzer
    PhotobankAnalyzer()
    
    _run_mp(proc_num, _analyze_tar, args_to_run)

def _rfilter(exec_details):
    output_file, input_files = exec_details[0], exec_details[1]
    
    with open(output_file, 'w') as o:
        for input_file in input_files:
            if not os.path.isfile(input_file):
                sys.stderr.write(
                    'WARNING: no such an input file %s\n' % (input_file)
                )
                continue
            
            with open(input_file, 'r') as f:
                for sline in f:
                    parsed_element = json.loads(sline.strip())
                    face_ratio = 0.0
                    for face in parsed_element['faces']:
                        face_ratio += face[2] * face[3]
                    face_ratio /= (
                        PI4 * parsed_element['height'] * parsed_element['width']
                    )
                    
                    if (
                        (parsed_element['width'] >= MIN_HEIGHT) and
                        (parsed_element['height'] >= MIN_WIDTH) and
                        face_ratio >= MIN_FACE_RATIO
                    ):
                        o.write(sline)

def rfilter(output_file, input_files):
    input_files_found = _unglob_files(input_files)
    return _rfilter((output_file, input_files_found))

def rfilter_mp(proc_num, output_dir, input_files):
    # No recursive search for input
    input_files_found = _unglob_files(input_files)
    split_input_files = _split_args(proc_num, input_files_found)
    
    index_digits = int(np.log10(proc_num)) + 1
    output_filename_pattern = (
        RFITLER_OUTPUT_FILENAME_PATTERN % ('%0' + str(index_digits) + 'u')
    )
    
    args_to_run = [
        (
            os.path.join(output_dir, output_filename_pattern % (i)),
            split_input_files[i]
        )
        for i in range(proc_num)
    ]
    _run_mp(proc_num, _rfilter, args_to_run)

def _rextract(exec_details):
    output_dir, input_files = exec_details[0], exec_details[1]
    gs_extracting_dict = {}
    tar_extracting_dict = {}
    
    
    for input_file in input_files:
        if not os.path.isfile(input_file):
            sys.stderr.write(
                'WARNING: no such an input file %s\n' % (input_file)
            )
            continue
        
        with open(input_file, 'r') as f:
            for sline in f:
                parsed_element = json.loads(sline.strip())
                filename = parsed_element['filename']
                
                if parsed_element['type'] == IMAGE_FILE_TYPE:
                    copy2(
                        filename,
                        os.path.join(output_dir, os.path.basename(filename))
                    )
                elif parsed_element['type'] == GS_FILE_TYPE:
                    if filename not in gs_extracting_dict:
                        gs_extracting_dict[filename] = set()
                    gs_extracting_dict[filename] |= set([
                        parsed_element['member']
                    ])
                elif parsed_element['type'] == TAR_FILE_TYPE:
                    if filename not in tar_extracting_dict:
                        tar_extracting_dict[filename] = set()
                    tar_extracting_dict[filename] |= set([
                        parsed_element['member']
                    ])
    
    for gs_file in gs_extracting_dict:
        gs_output_dir = os.path.join(output_dir, os.path.basename(gs_file))
        if not os.path.isdir(gs_output_dir):
            os.mkdir(gs_output_dir)
        for image_doc in Pb2DocumentReader(gs_file):
            image_hash = str(image_doc.imageId.imageHash)
            if image_hash in gs_extracting_dict[gs_file]:
                with open(
                    os.path.join(gs_output_dir, image_hash + '.jpeg'), 'wb'
                ) as o:
                    o.write(image_doc.content)
    
    for tar_file in tar_extracting_dict:
        tar_output_dir = os.path.join(output_dir, os.path.basename(tar_file))
        if not os.path.isdir(tar_output_dir):
            os.mkdir(tar_output_dir)
        with tarfile.open(tar_file, 'r') as itar:
            for image_info in itar.getmembers():
                image_name = image_info.name
                if image_name in tar_extracting_dict[tar_file]:
                    itar.extract(
                        image_info, os.path.join(tar_output_dir, image_name)
                    )

def rextract(output_dir, input_files):
    input_files_found = _unglob_files(input_files)
    return _rextract((output_dir, input_files_found))

def rextract_mp(proc_num, output_dir, input_files):
    # No recursive search for input
    input_files_found = _unglob_files(input_files)
    
    split_input_files = _split_args(proc_num, input_files_found)
    args_to_run = [
        (output_dir, split_input_files[i])
        for i in range(proc_num)
    ]
    _run_mp(proc_num, _rextract, args_to_run)

if __name__ == '__main__':
    import argparse
    
    aparser_gen = argparse.ArgumentParser()
    asubparsers = aparser_gen.add_subparsers(
        dest = 'command', help = 'Command to be executed'
    )
    asubparsers.required = True
    
    # ToDo: add -r argument here for folders
    aparser_analyze = asubparsers.add_parser(
        'analyze', help = 'Analyzes *.jpeg and *.png files key parameters'
    )
    aparser_analyze.add_argument(
        'output_file', metavar = 'output_file', type = str,
        help = 'output report file with parameters'
    )
    aparser_analyze.add_argument(
        'image_files', metavar = 'image_file', type = str, nargs = '+',
        help = 'image file for analysis'
    )
    
    aparser_analyze_mp = asubparsers.add_parser(
        'analyze-mp', help = 'Analyzes *.jpeg and *.png files key ' +
        'parameters; multiprocess version of analyze command'
    )
    aparser_analyze_mp.add_argument(
        'proc_num', metavar = 'processes_count', type = int,
        help = 'processes count to run'
    )
    aparser_analyze_mp.add_argument(
        'output_dir', metavar = 'output_dir', type = str,
        help = 'output directory to store report files'
    )
    aparser_analyze_mp.add_argument(
        'image_files', metavar = 'image_file', type = str, nargs = '+',
        help = 'image file for analysis'
    )
    
    aparser_analyze_gs = asubparsers.add_parser(
        'analyze-gs', help = 'Analyzes *.gs archives for key' +
        'parameters'
    )
    aparser_analyze_gs.add_argument(
        'output_file', metavar = 'output_file', type = str,
        help = 'output report file with parameters'
    )
    aparser_analyze_gs.add_argument(
        'gs_files', metavar = 'gs_file', type = str, nargs = '+',
        help = 'generic storage archive for analysis'
    )
    
    aparser_analyze_mp_gs = asubparsers.add_parser(
        'analyze-mp-gs', help = 'Analyzes *.gs archives for key' +
        'parameters;  multiprocess version of analyze-gs command'
    )
    aparser_analyze_mp_gs.add_argument(
        'proc_num', metavar = 'processes_count', type = int,
        help = 'processes count to run'
    )
    aparser_analyze_mp_gs.add_argument(
        'output_dir', metavar = 'output_dir', type = str,
        help = 'output directory to store report files'
    )
    aparser_analyze_mp_gs.add_argument(
        'gs_files', metavar = 'gs_file', type = str, nargs = '+',
        help = 'generic storage archive for analysis'
    )
    
    aparser_analyze_tar = asubparsers.add_parser(
        'analyze-tar', help = 'Analyzes *.tar archives with images for key' +
        'parameters'
    )
    aparser_analyze_tar.add_argument(
        'output_file', metavar = 'output_file', type = str,
        help = 'output report file with parameters'
    )
    aparser_analyze_tar.add_argument(
        'tar_files', metavar = 'tar_file', type = str, nargs = '+',
        help = 'tar archive with images for analysis'
    )
    
    aparser_analyze_mp_tar = asubparsers.add_parser(
        'analyze-mp-tar', help = 'Analyzes *.tar archives for key' +
        'parameters;  multiprocess version of analyze-tar command'
    )
    aparser_analyze_mp_tar.add_argument(
        'proc_num', metavar = 'processes_count', type = int,
        help = 'processes count to run'
    )
    aparser_analyze_mp_tar.add_argument(
        'output_dir', metavar = 'output_dir', type = str,
        help = 'output directory to store report files'
    )
    aparser_analyze_mp_tar.add_argument(
        'tar_files', metavar = 'tar_file', type = str, nargs = '+',
        help = 'tar archive for analysis'
    ) 
    
    aparser_rfilter = asubparsers.add_parser(
        'rfilter', help = 'Filters images according to report from analyze ' +
        'command'
    )
    aparser_rfilter.add_argument(
        'output_file', type = str, help = 'output report file for filtered ' +
        'files'
    )
    aparser_rfilter.add_argument(
        'input_files', metavar = 'input_file', type = str, nargs = '+',
        help = 'input report file by ' +
        'analyze[-gs|-tar] command'
    )
    
    aparser_rfilter_mp = asubparsers.add_parser(
        'rfilter-mp', help = 'Filters images according to report from analyze ' +
        'command; multiprocess version of filter command'
    )
    aparser_rfilter_mp.add_argument(
        'proc_num', metavar = 'processes_count', type = int,
        help = 'processes count to run'
    )
    aparser_rfilter_mp.add_argument(
        'output_dir', type = str, help = 'output reports dir for filtered ' +
        'files'
    )
    aparser_rfilter_mp.add_argument(
        'input_files', metavar = 'input_file', type = str, nargs = '+',
        help = 'input report file by ' +
        'analyze[-gs|-tar] command'
    )
    
    aparser_rextract = asubparsers.add_parser(
        'rextract', help = 'Extracts / copies files according to filtered '
        + 'reports'
    )
    aparser_rextract.add_argument(
        'output_dir', type = str, help = 'extracted / copied files dir'
    )
    aparser_rextract.add_argument(
        'input_files', metavar = 'input_file', type = str, nargs = '+',
        help = 'input report file by ' +
        'analyze[-gs|-tar] or filter commands'
    )
    
    aparser_rextract_mp = asubparsers.add_parser(
        'rextract-mp', help = 'Extracts / copies files according to filtered '
        + 'reports; multiprocess version of filter command'
    )
    aparser_rextract_mp.add_argument(
        'proc_num', metavar = 'processes_count', type = int,
        help = 'processes count to run'
    )
    aparser_rextract_mp.add_argument(
        'output_dir', type = str, help = 'extracted / copied files dir'
    )
    aparser_rextract_mp.add_argument(
        'input_files', metavar = 'input_file', type = str, nargs = '+',
        help = 'input report file by ' +
        'analyze[-gs|-tar] or filter commands'
    )
    
    args = aparser_gen.parse_args()
    
    if args.command == 'analyze':
        analyze(args.output_file, args.image_files)
    elif args.command == 'analyze-mp':
        analyze_mp(args.proc_num, args.output_dir, args.image_files)
    elif args.command == 'analyze-gs':
        analyze_gs(args.output_file, args.gs_files)
    elif args.command == 'analyze-mp-gs':
        analyze_mp_gs(args.proc_num, args.output_dir, args.gs_files)
    elif args.command == 'analyze-tar':
        analyze_tar(args.output_file, args.tar_files)
    elif args.command == 'analyze-mp-tar':
        analyze_mp_tar(args.proc_num, args.output_dir, args.tar_files)
    elif args.command == 'rfilter':
        rfilter(args.output_file, args.input_files)
    elif args.command == 'rfilter-mp':
        rfilter_mp(args.proc_num, args.output_dir, args.input_files)
    elif args.command == 'rextract':
        rextract(args.output_dir, args.input_files)
    elif args.command == 'rextract-mp':
        rextract_mp(args.proc_num, args.output_dir, args.input_files)
