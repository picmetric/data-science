# Authors

Jeremy Meek - Machine Learning Engineer / Data Engineer

Logan Keith - Machine Learning Engineer / Data Engineer

Xander Bennett - Junior Machine Learning Engineer / Data Engineer
# Data-Science Repo for Picmetric

Predictions leverage two pre-trained neural networks (yolo_v3, resnet_50) to summarize attributes of images (i.e. counts of objects, people, etc.) For facial recognition, a model is currently in development using the MTCNN neural network for this project and will be implemented upon completion.

The data science back-end works here by leveraging a Flask app with an API endpoint. depending on the neural network, the output provided in dictionary format (compatible in producing a JSON object) will differ.

# Deployment
ssh into your EC2 instance that has python and docker preinstalled on debian-based linux, then
```
wget https://raw.githubusercontent.com/picmetric/data-science/distortedlogic/bootstrap.sh
sudo sh bootstrap.sh
```
profit??

# Use of custom CLI
- list available CLI command
```
sudo docker-compose exec flask picmetric
```

- check that a GPU is passed through to docker for tensorflow
```
sudo docker-compose exec flask picmetric scripts check_gpu
```

- Start the model manager server
```
sudo docker-compose exec flask picmetric scripts startmm
```

## How it works

- A user will upload an image that will be added to an Amazon S3 bucket (a public cloud storage resource). 
- A url pointer to the image is stored in the database
- The data science back-end will follow the url pointer to the image and run analysis on it using the neural network models described above
- Image attributes (model predictions/outputs) are stored in the database and a JSON object is created.
	- This is important because the machine learning was built using Python and the front-end with Javascript. JSON is digestable for both. This JSON object is made available at an API endpoint to be shipped back through the pipeline
- These same attributes are served back to the user via the client

## Models used
- Res Net 50 - Object recognition neural network trained on 1,000 different classes
- Yolo_V3 Coco - "You Only Look Once" - Trained on 80 classes in object recognition. Also provides 'bounding boxes' to surround perceived objects in image
- MTCNN - Multi-task Cascaded Convolutional Neural Networks for Face Detection. Trained on faces to be able to identify eyes, mouth and nose to triangulate a human face in an image. Currently in test. 

# JSON Output
## Resnet_50

Resnet_50 outputs will show the confidence level and the perceived object:

```{
	"resnet50_objects": [
		{
			"confidence": "0.5326323",
			"object": "kite"
		},
		{
			"confidence": "0.22083153",
			"object": "bald_eagle"
		}
	],
```

## Yolo_v3

Yolo_v3 outputs will display the above information as well as the details of the accompanying 'bounding box':

	```
	"yolo_objects": [
		{
			"confidence": "0.22083153",
			"object": "bald_eagle",
			"bounding_box": {
				"x_min": "16",
				"x_max": "66",
				"y_min": "23",
				"y_max": "244"
			}
		},
		{
			"confidence": "0.051131114",
			"object": "Vulture",
			"bounding_box": {
				"x_min": "14",
				"x_max": "68",
				"y_min": "55",
				"y_max": "204"
			}
		}
	],
	```
## MTCNN
When deployed, the MTCNN model will provide details specific to facial recognition as seen below:

	```
	"mtcnn_faces": [
		{
			"confidence": "0.22083153",
			"bounding_box": {
				"x_min": "16",
				"x_max": "66",
				"y_min": "23",
				"y_max": "244"
			},
			"keypoints": {
				"nose": [144, 221],
				"left_eye": [134, 212],
				"right_eye": [155, 209],
				"mouth_left": [137, 231],
				"mouth_right": [164, 229]
			}
		}
	],
	```
