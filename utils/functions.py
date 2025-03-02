import os, json

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
STORAGE_PATH = f"{ROOT_PATH}/storage/"

def store_result (post_url, download_url):
    """
    Store result of post_url to download_url into a results.json file.
    If the results.json file does not exist, it will be created.

    Args:
        post_url (str): The original post url.
        download_url (str): The url of the downloadable media.
    """
    if not os.path.exists(STORAGE_PATH):
        os.makedirs(STORAGE_PATH)

    results = json.loads(open(f"{STORAGE_PATH}/results.json", "r").read()) if os.path.exists(f"{STORAGE_PATH}/results.json") else {}

    with open(f"{STORAGE_PATH}/results.json", "w+") as file:
        results[post_url] = download_url
        file.write(json.dumps(results))
        file.close()
    
    print (f"Result url saved to {STORAGE_PATH}/results.json")

def create_slug (text):
    """
    Converts a given text into a slug by converting it to lowercase and replacing spaces with hyphens.

    Args:
        text (str): The input text to be converted into a slug.
    
    Returns:
        str: The slugified version of the input text.
    """

    return text.lower().replace(" ", "-")

def get_file_extension_from_bytes(file_bytes):
    # Check file signature (magic numbers) to identify the file type
    
    # JPEG file signature (Start with FF D8 and end with FF D9)
    if file_bytes[:2] == b'\xff\xd8' and file_bytes[-2:] == b'\xff\xd9':
        return 'jpg'
    
    # PNG file signature (Start with 89 50 4E 47)
    elif file_bytes[:4] == b'\x89PNG':
        return 'png'
    
    # GIF file signature (Start with GIF87a or GIF89a)
    elif file_bytes[:6] in [b'GIF87a', b'GIF89a']:
        return 'gif'
    
    # PDF file signature (Start with %PDF-)
    elif file_bytes[:5] == b'%PDF-':
        return 'pdf'
    
    # ZIP file signature (Start with PK)
    elif file_bytes[:2] == b'PK':
        return 'zip'
    
    # MP4 file signature (Start with 00 00 00 18 66 74 79 70)
    elif file_bytes[:8] == b'\x00\x00\x00\x18\x66\x74\x79\x70':
        return 'mp4'
    
    # Text file signature (Starts with ASCII text, but this is a basic check)
    elif file_bytes[:3] in [b'EOF', b'1F8B']:
        return 'txt'  # Gzip or others
    
    # If none of the above match, return a generic file extension
    return 'bin'

def try_catch (function):
    try:
        function()
    except Exception as err:
        pass

# def cache_request (url):
#     path = "./.cache/"

#     if not os.path.exists(path):
#         os.makedirs(path)
    
#     hashedUrl = hash.sha256(url.encode("utf-8")).hexdigest()
#     if not os.path.exists(f"{path}/{hashedUrl}.json"):
#         with open(f"{path}/{hashedUrl}.cache", "w") as file:
#             file.write(result)
#             file.close()
#         return response