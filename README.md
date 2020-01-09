# Data-Science Repo for Picmetric

Predictions leverage two pre-trained neural networks (yolo_v3, resnet_50) to summarize attributes of images (i.e. counts of objects, people, etc.) For facial recognition, a model is currently in development using the MTCNN neural network for this project and will be implemented upon completion.

The data science back-end works here by leveraging a Flask app with an API endpoint. depending on the neural network, the output provided in dictionary format (compatible in producing a JSON object) will differ.

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

	```"yolo_objects": [
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
## MTCNN
When deployed, the MTCNN model will provide details specific to facial recognition as seen below:

	```"mtcnn_faces": [
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
