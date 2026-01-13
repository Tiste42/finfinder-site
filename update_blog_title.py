import json
import os

file_path = '/workspace/blog_posts.json'

# Read the file
with open(file_path, 'r') as f:
    data = json.load(f)

# Target specific post
target_slug = "surfboard-fin-prices-skyrocketed-200-300"
new_slug = "why-are-fins-so-expensive-real-costs"
new_title = "Why Are Fins So Damn Expensive? The Real Costs Behind That $300 Price Tag"
new_meta_description = "Fin prices jumped 25-30% since 2024, with some hitting $300. Discover the real reasons: tariffs, materials, shipping chaos, plus which mid-tier brands actually deliver value."

found = False
for post in data['posts']:
    if post['slug'] == target_slug:
        post['slug'] = new_slug
        post['title'] = new_title
        post['meta_description'] = new_meta_description
        found = True
        print(f"Updated post: {new_title}")
        break

if not found:
    print("Post not found!")
else:
    # Write back
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)
    print("Successfully saved changes.")
