#!/bin/bash

# List of Python files to run
python_files=("vgg19/vgg19_line.py" "vgg19/vgg19_infill.py" "ResNet/resnet50_line.py" "ResNet/resnet50_infill.py" "MobileNet/mobilenetv3_line.py" "MobileNet/mobilenetv3_infill.py" "Xception/xception_line.py" "Xception/xception_infill.py")

# Loop through each Python file and execute them
for file in "${python_files[@]}"
do
    echo "Running $file ..."
    python "$file"
    echo "Finished running $file"
done

echo "All Python scripts have been executed."
