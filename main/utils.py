import os
import base64
from io import BytesIO
import cloudinary
import cloudinary.uploader

# Setup Cloudinary (will use Render env vars if set)
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME", "your_cloud_name"),
    api_key=os.getenv("CLOUDINARY_API_KEY", "your_api_key"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET", "your_api_secret"),
    secure=True
)

def save_base64_image(base64_str, prefix="image"):
    if not base64_str:
        return ""

    try:
        # Separate header and actual base64 content
        if "base64," in base64_str:
            header, base64_data = base64_str.split(",", 1)
        else:
            base64_data = base64_str

        image_data = BytesIO(base64.b64decode(base64_data))

        # Upload to Cloudinary
        result = cloudinary.uploader.upload(image_data, folder="portfolio_images", public_id=prefix, overwrite=True)

        return result.get("secure_url", "")
    except Exception as e:
        print("Cloudinary upload error:", str(e))
        return ""
