import json
from datetime import datetime

def convert_to_coco_format(input_json_path, output_json_path):
    """
    Convert custom JSON format to COCO format
    
    Args:
        input_json_path (str): Path to input JSON file
        output_json_path (str): Path to output COCO format JSON file
    """
    
    # Load the input JSON
    with open(input_json_path, 'r') as f:
        input_data = json.load(f)
    
    # Initialize COCO format structure
    coco_data = {
        "info": {
            "description": "Vacant lot detection dataset",
            "url": "",
            "version": "1.0",
            "year": datetime.now().year,
            "contributor": "",
            "date_created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "licenses": [
            {
                "id": 1,
                "name": "Unknown",
                "url": ""
            }
        ],
        "images": [],
        "annotations": [],
        "categories": []
    }
    
    # Get unique categories from the data
    categories = set()
    for item in input_data:
        for annotation in item.get('annotations', []):
            categories.add(annotation['class'])
    
    # Create categories list with IDs
    category_to_id = {}
    for idx, category in enumerate(sorted(categories), 1):
        category_to_id[category] = idx
        coco_data["categories"].append({
            "id": idx,
            "name": category,
            "supercategory": ""
        })
    
    # Convert images and annotations
    annotation_id = 1
    
    for image_id, item in enumerate(input_data, 1):
        # Add image info
        coco_data["images"].append({
            "id": image_id,
            "width": item["width"],
            "height": item["height"],
            "file_name": item["file_name"],
            "license": 1,
            "flickr_url": "",
            "coco_url": "",
            "date_captured": ""
        })
        
        # Add annotations for this image
        for annotation in item.get('annotations', []):
            bbox = annotation['bbox']
            x, y, width, height = bbox
            
            # Calculate area
            area = width * height
            
            coco_data["annotations"].append({
                "id": annotation_id,
                "image_id": image_id,
                "category_id": category_to_id[annotation['class']],
                "segmentation": [],  # Empty for bounding box only
                "area": area,
                "bbox": [x, y, width, height],
                "iscrowd": 0
            })
            
            annotation_id += 1
    
    # Save to output file
    with open(output_json_path, 'w') as f:
        json.dump(coco_data, f, indent=2)
    
    print(f"Conversion completed!")
    print(f"Total images: {len(coco_data['images'])}")
    print(f"Total annotations: {len(coco_data['annotations'])}")
    print(f"Total categories: {len(coco_data['categories'])}")
    print(f"Categories: {[cat['name'] for cat in coco_data['categories']]}")
    print(f"Output saved to: {output_json_path}")
