import zipfile
import io
import base64
from openai import OpenAI

#client = OpenAI(api_key="***")

zip_path = r"C:\Users\שירה\yoga-pose-image-classification-dataset.zip"

#list of yoga poses 

poses_list = [
    "Downward-Facing Dog",
    "Upward-Facing Dog",
    "Warrior I",
    "Triangle Pose",
    "Tree Pose",
    "Bridge Pose",
    "Low Lunge",
    "Unknown"
]

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    for file_info in zip_ref.infolist():
        if file_info.filename.lower().endswith((".jpg", ".png", ".jpeg")):
            with zip_ref.open(file_info) as f:
                image_bytes = f.read()
                image_base64 = base64.b64encode(image_bytes).decode("utf-8")

            prompt_text = f"""
            Identify the yoga pose in this image. 
            Classify it as one of the following poses: {', '.join(poses_list)}.
            If it does not match any, choose 'Unknown'.
            """

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt_text},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                        ],
                    }
                ],
            )

            print(f"{file_info.filename}: {response.choices[0].message.content}")
