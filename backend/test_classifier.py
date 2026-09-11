import torch
import torchvision.models as models
from torchvision.models import MobileNet_V3_Small_Weights
from PIL import Image

weights = MobileNet_V3_Small_Weights.DEFAULT
model = models.mobilenet_v3_small(weights=weights)
model.eval()

preprocess = weights.transforms()

# Test broken brick
img = Image.open(r"C:\Users\lenovo\.gemini\antigravity\scratch\material-rebirth-ai\backend\test_apple.jpg").convert('RGB')
batch = preprocess(img).unsqueeze(0)

prediction = model(batch).squeeze(0).softmax(0)
class_id = prediction.argmax().item()
score = prediction[class_id].item()
category_name = weights.meta["categories"][class_id]
print(f"Top 1: {category_name} ({score:.2f})")

# Top 5
top5_prob, top5_catid = torch.topk(prediction, 5)
for i in range(top5_prob.size(0)):
    print(weights.meta["categories"][top5_catid[i]], f"{top5_prob[i].item():.2f}")
