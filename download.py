import requests
import json

def load_config():
    with open('config.json') as file:
        config = json.load(file)
    return config

def download_from_workshop(workshop_file_id, api_key):
    url = 'https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/'

    params = {
        'key': api_key,
        'itemcount': 1,
        'publishedfileids[0]': workshop_file_id
    }

    response = requests.post(url, data=params)
    print(f'Response status code: {response.status_code}')
    print(f'Response content: {response.text}')

    try:
        data = response.json()
        if 'publishedfiledetails' in data['response']:
            file_url = data['response']['publishedfiledetails'][0]['file_url']
            file_name = f'{workshop_file_id}.zip'  # Set the desired file name for the downloaded content

            if file_url:
                # Download the workshop content
                download_response = requests.get(file_url, stream=True)
                with open(file_name, 'wb') as file:
                    for chunk in download_response.iter_content(chunk_size=8192):
                        file.write(chunk)
                
                print(f'Downloaded workshop content to {file_name}')
            else:
                print('Invalid file URL')
        else:
            print('Invalid workshop file ID')
    except json.decoder.JSONDecodeError as e:
        print(f'Failed to decode JSON response: {e}')

# Example usage
config = load_config()
workshop_file_id = config['workshop_file_id']
api_key = config['api_key']
download_from_workshop(workshop_file_id, api_key)
