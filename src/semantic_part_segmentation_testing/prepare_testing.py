#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import argparse
import fileinput

#https://github.com/BVLC/caffe/issues/861#issuecomment-70124809
import matplotlib
matplotlib.use('Agg')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(BASE_DIR))
from global_variables import *
from utilities_caffe import stack_caffe_models

parser = argparse.ArgumentParser(description="Stitch pool5 extraction and image embedding caffemodels together.")
parser.add_argument('--iter_num', '-n', help='Use image embedding model trained after iter_num iterations', type=int, default=400000)
args = parser.parse_args()


# BORRAR - solo para manifold combinado
g_part_image_semSeg_embedding_training_folder = '/media/adrian/Datasets/datasets/image_embedding/combinedShape_part_image_semSeg_embedding_training_03001627_fc_layers'
g_part_image_semSeg_embedding_testing_folder = '/media/adrian/Datasets/datasets/image_embedding/combinedShape_part_image_semSeg_embedding_testing_03001627_manifoldNet'
# END BORRAR - solo para manifold combinado


# Loop this for every part
part_id = 4
g_network_architecture_name = 'manifoldNet'
g_part_image_embedding_training_prototxt = os.path.join(g_part_image_semSeg_embedding_training_folder, 'image_embedding_'+g_network_architecture_name+'_part'+str(part_id)+'.prototxt')
g_part_image_embedding_testing_prototxt = os.path.join(g_part_image_semSeg_embedding_testing_folder, 'image_embedding_'+g_network_architecture_name+'_part'+str(part_id)+'.prototxt')


image_embedding_testing_in = os.path.join(BASE_DIR, 'image_embedding_'+g_network_architecture_name+'.prototxt.in')
print 'Preparing %s...' % g_part_image_embedding_testing_prototxt
shutil.copy(image_embedding_testing_in, g_part_image_embedding_testing_prototxt)
for line in fileinput.input(g_part_image_embedding_testing_prototxt, inplace=True):
    line = line.replace('embedding_space_dim', str(g_shape_embedding_space_dimension))
    line = line.replace('partX', 'part'+str(part_id))
    sys.stdout.write(line)


part_image_semSeg_embedding_caffemodel = os.path.join(g_part_image_semSeg_embedding_training_folder, 'single_manifold_snapshots', 'snapshots%s_part%d_iter_%d.caffemodel' % (g_shapenet_synset_set_handle, part_id, args.iter_num))
part_image_semSeg_embedding_caffemodel_stacked = os.path.join(g_part_image_semSeg_embedding_testing_folder, 'stacked%s_part%d_iter_%d.caffemodel' % (g_shapenet_synset_set_handle, part_id, args.iter_num))

stack_caffe_models(prototxt=g_part_image_embedding_testing_prototxt,
                   base_model=g_extract_feat_pool5_caffemodel,
                   top_model=part_image_semSeg_embedding_caffemodel,
                   stacked_model=part_image_semSeg_embedding_caffemodel_stacked,
                   caffe_path=g_caffe_install_path)


