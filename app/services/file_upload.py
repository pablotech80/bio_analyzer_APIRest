import boto3
import os
from werkzeug.utils import secure_filename
from PIL import Image
from io import BytesIO

def upload_image_to_s3(file, filename, bucket, acl="public-read"):
    """
    Sube una imagen a AWS S3 y devuelve la URL pública.
    Comprime la imagen a JPG si es necesario.
    """
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION")
    )

    # Comprimir y convertir a JPG
    image = Image.open(file)
    img_io = BytesIO()
    image = image.convert("RGB")
    image.save(img_io, "JPEG", quality=85, optimize=True)
    img_io.seek(0)

    s3.upload_fileobj(
        img_io,
        bucket,
        filename,
        ExtraArgs={"ACL": acl, "ContentType": "image/jpeg"}
    )

    url = f"https://{bucket}.s3.{os.environ.get('AWS_REGION')}.amazonaws.com/{filename}"
    return url
