import cloudinary
import cloudinary.uploader
import re
from datetime import datetime

cloudinary.config(
    cloud_name="duhho2j3z",
    api_key="379375491312472",
    api_secret="GyL_L3BGlKNXMtMyV_ciSvioftU"
)

def upload_to_cloudinary(image, name, folder="HomeSec/Known/"):
    timestamp = int(datetime.utcnow().timestamp())
    public_id = f"{name}_{timestamp}"

    result = cloudinary.uploader.upload(
        image,
        folder=folder,
        public_id=public_id,
        overwrite=True,
        resource_type="image"
    )

    return result["secure_url"]

def delete_from_cloudinary(public_id):
    result = cloudinary.uploader.destroy(public_id, invalidate=True)
    return result

def extract_id_from_url(url):
    """
    Extracts the Cloudinary public_id from a given URL.
    Example:
        https://res.cloudinary.com/demo/image/upload/v1712811298/HomeSec/Known/John_1712811298.jpg
    Returns:
        HomeSec/Known/John_1712811298 (without file extension)
    """
    match = re.search(r'/upload/(?:v\d+/)?(.+?)\.(jpg|jpeg|png|webp|gif)$', url)
    if match:
        return match.group(1)
    return None