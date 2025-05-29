import requests
from configs import ACCESS_TOKEN_UTM

access_token = ACCESS_TOKEN_UTM

def get_leads():
    url = 'https://halabatalia.amocrm.ru'
    headers = {'Authorization': f'Bearer {access_token}',
               'Content-Type': 'application/json'}
    data = {
        'client_id': 'ed89657d-aa30-40ad-90ba-7509a4015056',
        'client_secret': 'aYtMreAqov2jBZAF1ppeCk8Doy8rPs4vUMmS3xC72rJGeIngyNOBzlSEJRc8kNXq',
        'grant_type': 'authorization_code',
        'code': access_token,
        'redirect_uri': 'https://b780-84-54-80-195.ngrok-free.app/amo'
    }

    response = requests.get(url, headers=headers)

    print(response.text)
def create_lid(name, phone_number):
    # тут нужно было домен поменять?
    url = 'https://halabatalia.amocrm.ru'
    headers = {'Authorization': f'Bearer {access_token}',
               'Content-Type': 'application/json'}

    custom_contacts = [
        {
            "field_code": "PHONE",
            "values": [
                {
                    "enum_code": "WORK",
                    "value": phone_number
                }
            ]
        },
    ]
    data = [
        {
            "name": "Информация с бота",
            "created_by": 0,
            "_embedded": {
                "contacts": [
                    {
                        "first_name": name,
                        # "phone_number": phone_number,
                        "custom_fields_values": custom_contacts
                    }
                ]
            },

        }]

    response = requests.post(url, json=data, headers=headers)

    return response

