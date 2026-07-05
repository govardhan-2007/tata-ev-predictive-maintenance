from core.digital_twin import DigitalTwin
from ai.inference import InferenceEngine

twin = DigitalTwin()
ai = InferenceEngine()

data = twin.step()

result = ai.predict(data)

print(data)
print()
print(result)