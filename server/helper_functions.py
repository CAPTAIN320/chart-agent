import os
import json
import httpx

from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    http_client=httpx.Client(verify=False),
)
llm_model = "gpt-4o"


def generate_chart(query, query_history):
    message_text = [
        {
            "role": "system",
            "content": (
                """
                Your task is to generate interactive and visually appealing Chart.js code based on a provided user query: '{query}'.
                You are expected to analyze the query and determine the appropriate type of chart (e.g., bar, line, pie) that best represents the data. If 'query' does not mention information about a chart do not create a chart, leave the 'chartjs_code' value empty, and simply respond in the 'response' value.
                Always use the real world data points and label names. Label names need to be specific and cannot be something like 'Label 1' or 'Movie 1'. Be sure to also use professional color codes.
                For the 'chartjs_code' value, Add Chart.js settings code in json format (EXAMPLE: { type: 'pie', data: { labels: ['Label 1', 'Label 2', 'Label 3', 'Label 4', 'Label 5'], datasets: [ { data: [30, 20, 15, 10, 25], backgroundColor: [ 'rgba(255, 99, 132, 0.7)', 'rgba(54, 162, 235, 0.7)', 'rgba(255, 206, 86, 0.7)', 'rgba(75, 192, 192, 0.7)', 'rgba(153, 102, 255, 0.7)', ], }, ], }, options: { responsive: true, maintainAspectRatio: false, aspectRatio: 1, plugins: { legend: { display: true, position: 'top', }, }, }, }), nothing else.
                The example JSON formatted output is the following:
                {
                    "response": "",
                    "chartjs_code": {}
                }
                """
            ),
        },
        {"role": "user", "content": query},
    ]

    for hist_query in query_history:
        message_text.append(
            {
                "role": "user",
                "content": hist_query,
            }
        )

    completion = client.chat.completions.create(
        model=llm_model,
        messages=message_text,
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
    )

    print("Token usage: " + str(completion.usage))

    response_content = json.loads(completion.choices[0].message.content)

    return response_content
