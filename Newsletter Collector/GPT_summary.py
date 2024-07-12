from openai import OpenAI
import json


alpha_api = "RKE6GIOQI4JM7LYK"

client = OpenAI(
                    organization='org-eXvNlOiMfgKeziZdN6Qd30Ag',
                    project='proj_gAyJmP46wZbkdOLl4bDL3Gvo',
                    api_key= None
                )

def generate_summary_ONE_article(URL):


    response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                response_format={ "type": "json_object" },
                messages=[
                    {"role": "system", "content": "You are a financial analyst, skilled in explaining complex financial concepts to people, with no financial understanding, with clarity and design to output JSON,the JSON format is 'Title', put the key points under 'key points. I want it to always be formated so that 'key points' contains a list of all the points, no number order "},
                    {"role": "user", "content": f"summary this website {URL} into one clear summary to cover everything about this company, less than 200 words and 5 to 10 dot points"}
                ]
                )
    result = response.choices[0].message.content
    print(result)
    result_json = json.loads(result)

    key_points = result_json["key points"]
    concatenated_string = ' '.join(key_points)

    return concatenated_string

