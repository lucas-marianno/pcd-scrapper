import json

with open("test/api-requests/fetch_id_list.json", "r") as f:
    data = json.load(f)

resume_collection = data["resumeCollection"]
print("data length:", len(resume_collection))

id_list: list[int] = [cv["referenceId"] for cv in resume_collection]

print(id_list)
# my_list = [0, 1, 2, 3]
#
# print(my_list)
#
# my_list = [n + 1 for n in my_list]
#
# print(my_list)
