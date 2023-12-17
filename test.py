import tempfile
import base64
import requests
from database.model import logdelusion

async def set_response_save_delusion(jumlah, data, first_id, email, input, ukuran):
    
    delusion_id = first_id - 1

    url_index = -1
    
    data = []
    
    for _ in range(jumlah):
        delusion_id += 1
        url_index += 1

        try:
            get_images = requests.get(url=data[url_index]['keterangan'])
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(get_images.content)
            images = open(temp_file.name, 'rb').read()
            images = base64.b64encode(images)    
            save = logdelusion(
                delusion_id=delusion_id,
                email=email,
                delusion_prompt=input,
                delusion_shape=ukuran,
                delusion_result=images
            )
            await save.save()
            os.remove(temp_file.name)
            response = {
                'delusion_id': delusion_id,
                'delusion_shape': ukuran,
                'delusion_image': data[url_index]['keterangan']
            }
            data.append(response)
        
        except Exception as e:
            delusion_id -= 1
            url_index -= 1
            jumlah += 1
            
