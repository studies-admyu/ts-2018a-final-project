#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tarfile

from PIL import Image

import torch.utils.data as data

def _pil_loader(file_obj):
    image = Image.open(file_obj)
    return image.convert('RGB')

class ImageTar(data.Dataset):
    def __init__(
        self, tar_file, loader = _pil_loader, transform = None
    ):
        if not tarfile.is_tarfile(tar_file):
            raise Exception('File \'%s\' is not a tar file' % (tar_file))
        self._tar_file = tar_file
        
        self._itar = tarfile.open(tar_file, 'r')
        self._data_samples = []
        for image_info in self._itar.getmembers():
            if not image_info.isfile():
                continue
            self._data_samples.append(image_info)
        
        self._loader = loader
        self._transform = transform
    
    def __del__(self):
        self._itar.close()
    
    def __len__(self):
        return len(self._data_samples)
    
    def __getitem__(self, idx):
        with self._itar.extractfile(self._data_samples[idx]) as f:
            sample = self._loader(f)
            if self._transform is not None:
                sample = self._transform(sample)
            
            return (sample, 0)
    
    def __repr__(self):
        fmt_str = 'Dataset ' + self.__class__.__name__ + '\n'
        fmt_str += '    Number of datapoints: {}\n'.format(self.__len__())
        fmt_str += '    Tar file: {}\n'.format(self._tar_file)
        tmp = '    Transforms (if any): '
        fmt_str += '{0}{1}\n'.format(
            tmp, self.transform.__repr__().replace('\n', '\n' + ' ' * len(tmp))
        )
        return fmt_str
