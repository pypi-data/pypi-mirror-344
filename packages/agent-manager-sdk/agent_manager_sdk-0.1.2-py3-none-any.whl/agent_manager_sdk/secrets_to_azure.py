
keys = []
with open('secret.env', 'r') as f:
    f = f.readlines()
    f = [elem for elem in f if len(elem) > 1]
    for line in f:
        # change it to
#         {
#     "name": "APIM_CLIENT_ID",
#     "value": "f0b2afa4-0d46-4f95-b3df-a6ee4b94a157",
#     "slotSetting": false
#   }
# this format
        print(line)
        key, value = line.split('=')
        keys.append({
            "name": key.replace('\n', '').replace('\'', '').strip(),
            "value": value.replace('\n', '').replace('\'', '').strip(),
            "slotSetting": 'false'
        })
for key in keys:
    print(key)