# Read the fitted model (fit.py) from the file model.pkl
# and define a function that uses the model to predict
# petal width from petal length

# This version of the predict function is wrapped with the
# model_metrics decorator, enabling it to call track_metrics
# to store mathematical metrics associated with each
# prediction.

import pickle

# Legacy engine workloads would need to:
#  - change @models.cml_model to @metrics.model_metrics on line 31
#  - import only cdsw here as cml library does not exist in engines
#  - change metrics to cdsw on lines 33 and 43
import cml.metrics_v1 as metrics
import cml.models_v1 as models

model = pickle.load(open('model.pkl', 'rb'))

# The model_metrics decorator equips the predict function to
# call track_metrics. It also changes the return type. If the
# raw predict function returns a value "result", the wrapped
# function will return eg
# {
#   "uuid": "612a0f17-33ad-4c41-8944-df15183ac5bd",
#   "prediction": "result"
# }
# The UUID can be used to query the stored metrics for this
# prediction later.
@models.cml_model(metrics=True)
def predict(args):
  # Track the input.
  metrics.track_metric("input", args)

  # If this model involved features, ie transformations of the
  # raw input, they could be tracked as well.
  # cdsw.track_metric("feature_vars", {"a":1,"b":23})

  petal_length = float(args.get('petal_length'))
  result = model.predict([[petal_length]])

  # Track the output.
  metrics.track_metric("predict_result", result[0][0])
  return result[0][0]
