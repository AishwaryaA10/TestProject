# -*- coding: utf-8 -*-
from os.path import join

base_dir = (
    r"/home/pcadmin/table_coordinate_detection/tabular_data_extraction/table_detection"
)
model_path = join(base_dir, "model", "frozen_inference_graph.pb")
label_path = join(base_dir, "model", "label_map_table_detection.pbtxt")
num_labels = 3
