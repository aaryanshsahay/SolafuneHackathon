import yaml
import argparse

from data_preprocessing.convert_labels_to_coco import  create_txt_files, create_txt_files_coco_format
from data_preprocessing.sort_images_labels import split_dataset


def main():
    # Load configuration

    parser = argparse.ArgumentParser(description="Convert label annotations to a specific format.")
    parser.add_argument("--labeltype", type=str, choices=["coco", "yolo"], required=True,
                        help="The format to convert the data to (e.g., coco, yolo).")
    args = parser.parse_args()

    
    
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)

    bbox_annotations = config['data']['bbox_training_annotations']
    segment_annotations = config['data']['segment_training_annotations']

    if args.labeltype == 'coco':
        create_txt_files_coco_format(bbox_annotations, 'data/labels/')
        create_txt_files_coco_format(segment_annotations, 'data/labels/')
    if args.labeltype == 'yolo':
        create_txt_files(bbox_annotations, 'data/labels/')
        create_txt_files(segment_annotations, 'data/labels/')

    
    split_dataset(config['data']['bbox_train'], 'data/labels/bbox_annotations.json', config_path="config.yaml")




if __name__ == "__main__":
    main()