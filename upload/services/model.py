# import requests
# import json
# import os

# class Image3DConverter:
#     def __init__(self, api_key):
#         self.api_key = api_key
#         self.api_url = 'https://api.stability.ai/v2beta/3d/stable-fast-3d'

#     def convert_image(self, image_path):
#         headers = {
#             'Authorization': f'Bearer {self.api_key}',
#         }

#         # Use 'files' parameter to send the image as multipart/form-data
#         with open(image_path, 'rb') as image_file:
#             files = {'file': image_file}  # Use 'file' as the key, or whatever the API expects
#             response = requests.post(
#                 self.api_url,
#                 headers=headers,
#                 files=files  # Change from 'data' to 'files'
#             )

#         if response.status_code != 200:
#             print(f'Error: {response.status_code} - {response.text}')
#             return None
        
#         try:
#             output_data = response.json()
#             # Process and save the output_data as needed
#             return output_data
#         except json.JSONDecodeError:
#             print("Error decoding JSON response")
#             return None



# # Example usage
# def main():
#     api_key = 'sk-qjoV1cqvUbkXMbPnIPvpKDxDglaWQLVpjv7yXnK7QCugAC4F'
#     converter = Image3DConverter(api_key)
#     image_path = r'C:\Users\varun\PycharmProjects\Image3D\pixel2shape\media\uploads\cones_PNG13331_EEs3uEn.png'
#     result = converter.convert_image(image_path)
#     if result:
#         print("Conversion successful:", result)

# if __name__ == '__main__':
#     main()


import requests
import os

class Image3DConverter:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = 'https://api.stability.ai/v2beta/3d/stable-fast-3d'

    def convert_image(self, image_path):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
        }

        # Use 'files' parameter to send the image as multipart/form-data
        with open(image_path, 'rb') as image_file:
            files = {'image': image_file}  # Ensure the key 'image' matches what the API expects
            response = requests.post(
                self.api_url,
                headers=headers,
                files=files  # Change from 'data' to 'files'
            )

        if response.status_code != 200:
            print(f'Error: {response.status_code} - {response.text}')
            return None
        
        try:
            # If the response is expected to be a JSON object, parse it
            return response.content  # Return the raw content for binary data
        except Exception as e:
            print("Error processing the response:", e)
            return None


# Example usage
def main():
    api_key = 'sk-qjoV1cqvUbkXMbPnIPvpKDxDglaWQLVpjv7yXnK7QCugAC4F'
    converter = Image3DConverter(api_key)
    image_path = r'C:\Users\varun\PycharmProjects\Image3D\pixel2shape\media\uploads\cones_PNG13331_EEs3uEn.png'
    
    # Perform the conversion
    result = converter.convert_image(image_path)
    
    if result:
        # Save the resulting 3D model (assuming it's a binary file, like .glb or .gltf)
        output_path = r'C:\Users\varun\PycharmProjects\Image3D\pixel2shape\media\uploads\output_model.glb'
        with open(output_path, 'wb') as output_file:
            output_file.write(result)
        print("Conversion successful. 3D model saved to:", output_path)

if __name__ == '__main__':
    main()
