import clickUp.group


api_key = "YOUR_API_KEY"
space_id = "9004111666"
tasks_by_tag = clickUp.sort_tasks_by_tag(api_key, space_id)
print(tasks_by_tag)