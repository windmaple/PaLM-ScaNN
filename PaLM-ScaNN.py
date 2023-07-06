import google.generativeai as palm
import os
import scann
import numpy as np
import math
os.environ['ALL_PROXY'] = 'http://localhost:3128'
key = 'YOUR-KEY'
palm.configure(api_key=key, transport="rest")

# Adapted from https://developers.generativeai.google/examples/vectordb_with_chroma

models = [m for m in palm.list_models() if 'embedText' in m.supported_generation_methods]
model = models[0]

DOCUMENT1 = "Operating the Climate Control System  Your Googlecar has a climate control system that allows you to adjust the temperature and airflow in the car. To operate the climate control system, use the buttons and knobs located on the center console.  Temperature: The temperature knob controls the temperature inside the car. Turn the knob clockwise to increase the temperature or counterclockwise to decrease the temperature. Airflow: The airflow knob controls the amount of airflow inside the car. Turn the knob clockwise to increase the airflow or counterclockwise to decrease the airflow. Fan speed: The fan speed knob controls the speed of the fan. Turn the knob clockwise to increase the fan speed or counterclockwise to decrease the fan speed. Mode: The mode button allows you to select the desired mode. The available modes are: Auto: The car will automatically adjust the temperature and airflow to maintain a comfortable level. Cool: The car will blow cool air into the car. Heat: The car will blow warm air into the car. Defrost: The car will blow warm air onto the windshield to defrost it."
DOCUMENT2 = "Your Googlecar has a large touchscreen display that provides access to a variety of features, including navigation, entertainment, and climate control. To use the touchscreen display, simply touch the desired icon.  For example, you can touch the \"Navigation\" icon to get directions to your destination or touch the \"Music\" icon to play your favorite songs."
DOCUMENT3 = "Shifting Gears  Your Googlecar has an automatic transmission. To shift gears, simply move the shift lever to the desired position.  Park: This position is used when you are parked. The wheels are locked and the car cannot move. Reverse: This position is used to back up. Neutral: This position is used when you are stopped at a light or in traffic. The car is not in gear and will not move unless you press the gas pedal. Drive: This position is used to drive forward. Low: This position is used for driving in snow or other slippery conditions."

def embed_function(texts) :
  # Embed the documents using any supported method
  return  np.asarray([palm.generate_embeddings(model=model, text=text)['embedding']
                         for text in texts])

DOCUMENTS = [DOCUMENT1, DOCUMENT2, DOCUMENT3]
embeddings = embed_function(DOCUMENTS)

searcher = scann.scann_ops_pybind.builder(embeddings, 10, "dot_product").tree(
    num_leaves=round(math.sqrt(len(DOCUMENTS))), num_leaves_to_search=10).score_brute_force().build()

query = 'touch screen features'
query_embedding = palm.generate_embeddings(model=model, text=query)['embedding']
neighbors, distances = searcher.search(query_embedding)
print(DOCUMENTS[neighbors[0]])
