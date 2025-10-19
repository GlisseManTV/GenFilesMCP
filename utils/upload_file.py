from requests import post
from json import dumps

def upload_file(url: str, token: str, file_path: str, filename:str, file_type:str) -> dict:
    """ 
    Upload a file to the specified URL with the provided token.
    Args:
        url (str): The URL to which the file will be uploaded.
        token (str): The authorization token for the request.
        file_path (str): The path to the file to be uploaded.
        filename (str): The desired filename for the uploaded file.
        file_type (str): The file extension/type (e.g., 'pptx', 'xlsx', 'docx', 'md').
    Returns:
        dict: Contains 'file_path_download' with a markdown hyperlink for downloading the uploaded file.
              Format: "[Download {filename}.{file_type}](/api/v1/files/{id}/content)"
              On error: {"error": {"message": "error description"}}
    """
    # Ensure the URL ends with '/api/v1/files/'
    url = f'{url}/api/v1/files/'

    # Prepare headers and files for the request
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }

    # Open the file and send the POST request
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = post(url, headers=headers, files=files)


    if response.status_code != 200:
       return dumps({"error":{"message": f'Error uploading file: {response.status_code}'}})
    else:
        return dumps(
{
            "file_path_download": f"[Download {filename}.{file_type}](/api/v1/files/{response.json()['id']}/content)"
            },
            indent=4,
            ensure_ascii=False
        )