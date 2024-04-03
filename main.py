import requests
import datetime
import json

api_url = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{curr}.json"
final_json_file = {}
header_for_file = "empty"
is_api_working_counter = 0

if __name__ == '__main__':
    s = list(map(str, input().split(' ')))
    s = [i.replace(',', '') for i in s]
    for i in s:
        response_from_api = requests.get(api_url.format(curr=i))
        if response_from_api.status_code == 200:
            print(i, "- OK")
            is_api_working_counter = 0  # Nullifying because api is working
            data = response_from_api.json()  # Our json file we got with desired currency
            del data["date"]
            final_json_file.update(data)
            if (header_for_file == "empty"):  # This will be executed once to determine header of file.
                header_for_file = response_from_api.headers.get("Date")  # Don't trust client (ourselves) about time
                header_for_file = datetime.datetime.strptime(header_for_file, '%a, %d %b %Y %H:%M:%S GMT')
                header_for_file = str(header_for_file.date()).replace('-', '') + '_' + str(header_for_file.time()).replace(':', '')
        else:
            print(i, "- not OK,", response_from_api.status_code)
            is_api_working_counter += 1
            if is_api_working_counter > 2:
                break
            else:
                s.insert(0, i)  # Retry with same currency
    if (header_for_file != "empty"):
        with open((header_for_file + '.json'), 'w') as f:
            json.dump(final_json_file, f, indent=4)
    else:
        print("Something went wrong and there is no data to create json file.")
