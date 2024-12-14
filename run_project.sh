#!/bin/bash

# Navigate to the desired directory
cd VectorBlox-SDK-release-v1.4.4.1/example/soc-c/ || { echo "Directory not found!"; exit 1; }

# Capture an image using the webcam
fswebcam -d /dev/video0 -r 320x240 --jpeg 85 output.jpg
if [ $? -ne 0 ]; then
  echo "Failed to capture image."
  exit 1
fi

echo "Image captured successfully."

make overlay

# Run the model with the captured image
./run-model ../../fw/firmware.bin ~/samples_V500_1.4.4/mobilenet-v2.vnnx output.jpg CLASSIFY
if [ $? -ne 0 ]; then
  echo "Failed to run the model."
  exit 1
fi

echo "Model executed successfully."

# Copy the output image to the git folder
cp output.jpg ~/icicle_kit_git_folder/
if [ $? -ne 0 ]; then
  echo "Failed to copy the image to the git folder."
  exit 1
fi

echo "Image copied to git folder."

# Navigate to the git folder
cd ~/icicle_kit_git_folder/ || { echo "Git folder not found!"; exit 1; }

# Add the image to the git repository
git add output.jpg
if [ $? -ne 0 ]; then
  echo "Failed to add the image to the git repository."
  exit 1
fi

echo "Image added to git repository."

# Commit the changes
git commit -m "webcam_photo"
if [ $? -ne 0 ]; then
  echo "Failed to commit the changes."
  exit 1
fi

echo "Changes committed successfully."

# Push the changes to the repository
git push
if [ $? -ne 0 ]; then
  echo "Failed to push the changes to the repository."
  exit 1
fi

echo "Changes pushed to repository successfully."
