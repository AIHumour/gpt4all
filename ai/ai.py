import requests

url = "https://gpt4all.io/models/ggml-gpt4all-j-v1.3-groovy.bin"
output_file = "ggml-gpt4all-j-v1.3-groovy.bin"

with requests.get(url, stream=True) as response:
    response.raise_for_status()
    with open(output_file, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

print("Download complete!")
