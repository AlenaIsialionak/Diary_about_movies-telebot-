def get_image_link(gender, style, image_name):
    base_url = "https://drive.google.com/uc?id="

    file_id = "YOUR_FILE_ID"
    return f"{base_url}{file_id}"


gender = "man"
style = "casual"
image_name = "image1.jpg"
image_link = get_image_link(gender, style, image_name)
print(image_link)

