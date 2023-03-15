import os
from google.cloud import videointelligence_v1p3beta1 as videointelligence


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'GoogleVideoAIAPI-ServiceAccount.json'

video_client = videointelligence.VideoIntelligenceServiceClient()


"""
[<Feature.FEATURE_UNSPECIFIED: 0>, <Feature.LABEL_DETECTION: 1>, <Feature.SHOT_CHANGE_DETECTION: 2>, 
<Feature.EXPLICIT_CONTENT_DETECTION: 3>, <Feature.FACE_DETECTION: 4>, <Feature.SPEECH_TRANSCRIPTION: 6>, 
<Feature.TEXT_DETECTION: 7>, <Feature.OBJECT_TRACKING: 9>, <Feature.LOGO_RECOGNITION: 12>, <Feature.PERSON_DETECTION: 14>]
"""

features = [videointelligence.Feature.LABEL_DETECTION]

# gs_URI = 'gs://dumbvideo/test.mp4'
# gs_URI = 'gs://dumbvideo/classroom.mp4'
gs_URI = 'gs://dumbvideo/random3.mp4'

labelDetectionConfig = videointelligence.LabelDetectionConfig(label_detection_mode=videointelligence.LabelDetectionMode.SHOT_AND_FRAME_MODE, stationary_camera=False)

videoContext = videointelligence.VideoContext(
    label_detection_config=labelDetectionConfig
)

request = videointelligence.AnnotateVideoRequest(
    input_uri=gs_URI,
    features=features,
    video_context=videoContext
)

# operation = video_client.annotate_video(request={"input_uri": gs_URI, "features": features, "videoContext": {"labelDetectionConfig": {"labelDetectionMode": videointelligence.LabelDetectionMode.FRAME_MODE ,"stationaryCamera": True, "model": 'builtin/latest'}}})
operation = video_client.annotate_video(request=request)

print("\nProcessing video for label annotations:")

result = operation.result(timeout=300)

segment_labels = result.annotation_results[0].segment_label_annotations

for i, segment_label in enumerate(segment_labels):
    print("Video label description: {}".format(segment_label.entity.description))
    for category_entity in segment_label.category_entities:
        print(
            "\tLabel category description: {}".format(category_entity.description)
        )

    for i, segment in enumerate(segment_label.segments):
        start_time = (
            segment.segment.start_time_offset.seconds
            + segment.segment.start_time_offset.microseconds / 1e6
        )
        end_time = (
            segment.segment.end_time_offset.seconds
            + segment.segment.end_time_offset.microseconds / 1e6
        )
        positions = "{}s to {}s".format(start_time, end_time)
        confidence = segment.confidence
        print("\tSegment {}: {}".format(i, positions))
        print("\tConfidence: {}".format(confidence))
    print("\n")