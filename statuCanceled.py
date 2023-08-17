import csv
import requests
i=0
# CSV dosyasını açma ve increment_id'leri okuma
with open('canceled.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        increment_id = row['increment_id']

        magento_url = f'{{base_url}}/rest/V1/orders?searchCriteria[filter_groups][0][filters][0][field]=increment_id&searchCriteria[filter_groups][0][filters][0][value]={increment_id}'
        headers = {
            'Authorization': '{{TOken_info}}'
        }

        response = requests.get(magento_url, headers=headers)
       
        if response.status_code == 200:
            data = response.json()
            
            if 'items' in data and len(data['items']) > 0:
                order_data = data['items'][0]

                entity_id = order_data['entity_id']
        
               # print(f"Entity ID: {entity_id}")

                             
                update_url = f'{{base_url}}/rest/V1/orders'
                payload = {
                    "entity": {
                        "entity_id": entity_id,
                        "increment_id":increment_id,
                        "status": "canceled",
                        "state": "canceled"
                    }
                }

                update_response = requests.post(update_url, json=payload, headers=headers)

                if update_response.status_code == 200:
                    i=i+1
                    print(f"{i} Order with increment_id {increment_id} + {entity_id} is canceled.")
                else:
                    print(f"Failed to cancel order with increment_id {increment_id}. Status code: {update_response.status_code}")


            else:
                print("No order data found for the given increment_id.")
        else:
            print(f"Failed to fetch order data. Status code: {response.status_code}")



       