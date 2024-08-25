import requests

def download_file_from_google_drive(url, destination):
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        return None

    def save_response_content(response, destination):
        CHUNK_SIZE = 32768

        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

    session = requests.Session()

    response = session.get(url, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'confirm': token}
        response = session.get(url, params=params, stream=True)

    save_response_content(response, destination)


if __name__ == "__main__":
    file_url = "https://drive.google.com/file/d/17HNfZYjQenEpfidGU-PvS4Xj4_JLLrrJ/view?usp=sharing"
    destination = "similarity.pkl"
    download_file_from_google_drive(file_url, destination)
