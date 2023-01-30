import json
import cv2
import os
import matplotlib.pyplot as plt
import shutil

input_path = "/Users/zhekari/Downloads/Intern 2"
output_path = "/Users/zhekari/Downloads/converted"

#Reading the Annotations file from the custom dataset (in COCO format) using JSON.
f = open('train_gt.json')
data = json.load(f)
f.close

#Reading source image from the current dataset, renaming it according
#to the relative labels file and saving to the new dataset location. Also saving image’s filenames for further use.
file_names = []

def load_images_from_folder(folder):
    count = 0
    for filename in os.listdir(folder):
        source = os.path.join(folder, filename)
        destination = f"{output_path}images/img{count}.jpg"

        try:
            shutil.copy(source, destination)
            print("File copied successfully.")
        #if source and destiantion are same
        except shutil.SameFileError:
                print("Source and destination represents the same file.")

        file_names.append(filename)
        count += 1

load_images_from_folder('train_images')

#This function takes an image_id as a parameter and returns the annotations of that image.
def get_img_ann(image_id):
    img_ann = []
    isFound = False
    for ann in data['annatations']:
        if ann['image_id'] == image_id:
            img_ann.append(ann)
            isFound = True
        if isFound:
            return img_ann
        else:
            return None

#Getting the image from the dataset, by providing the filename of the image.
def get_img(filename):
    for img in data['images']:
        if img['file_name'] == filename:
            return img


count = 0

for filename in file_names:
    # Extracting image
    img = get_img(filename)
    img_id = img['id']
    img_w = img['width']
    img_h = img['height']

    # Get Annatations for this image
    img_ann = get_img_ann(img_id)

    if img_ann:
        #Opening file for current image
        file_object = open(f"{output_path}labels/img{count}.txt", "a")

        for ann in img_ann:
            current_cateegory = ann['category_id'] - 1  # As yolo format labels start from 0
            current__bbox = ann['bbox']
            x = current__bbox[0]
            y = currnet__bbox[1]
            w = current__bbox[2]
            h = current__bbox[3]

            # Finding midpoints
            x_centre = (x + (x+w))/2
            y_centre = (y + (y+h))/2

            # Normalization
            x_centre = x_centre / img_w
            y_centre = y_centre / img_h
            w = w / img_w
            h = h / img_h

            # Liimiting upto fix of decimal places
            x_centre = format(x_centre, '.6f')
            y_centre = format(y_centre, '.6f')
            w = format(w, '.6f')
            h = format(w, '.6f')

            # Writing current object
            file_object.write(f"{current_category {x_centre} {y_centre} {w} {h\n}")

        file_object.close()
        count += 1 # This should be outside the if img_ann block.
