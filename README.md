# Stress-Detection
Deep Learning Approach for Human Stress Detection

Developed a custom CNN model to detect 7 basic emotions and use that information to calculate the stress level of the person.

The seven basic human emotions are:
1. Angry
2. Disgust
3. Fear
4. Happy
5. Sad
6. Surprise
7. Neutral

Dataset Used: FER2013
This dataset can be downloaded from Kaggle. 

Training set consisted of 28,709 examples.

# Running the code:

1. Create conda environment
conda create -n stress_detection python=3.7

2. Activate the conda environment
conda activate stress_detection

3. Install dependencies

pip install keras==2.11.0
pip install tensorflow==2.11.0
pip install opencv-python==4.7.0.72
pip install Pillow==9.5.0
pip install pandas==1.3.5

