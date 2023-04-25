import os
import requests


API_KEY = os.environ.get('BROWSE_AI_API_KEY')


def get_latest_task_data(robot_id):
  """
  Performs a GET request on the https://api.browse.ai/v2/robots/{robot_id}/tasks endpoint,
  and returns the parsed JSON object for the latest task.

  Args:
    robot_id: The ID of the robot.

  Returns:
    The parsed JSON object for the latest task.
  """

  # Make the GET request with the bearer token.
  response = requests.get(f"https://api.browse.ai/v2/robots/{robot_id}/tasks?sort=-finishedAt", headers={"Authorization": f"Bearer {API_KEY}"})

  # Check the response status code.
  if response.status_code != 200:
    raise Exception(f"Error getting task data: {response.status_code}")

  # Parse the JSON response.
  data = response.json()

  # Get the first item in the items list.
  task = data["result"]["robotTasks"]["items"][0]

  capUrl = task["capturedDataTemporaryUrl"]
  assert capUrl is not None
  return requests.get(capUrl).json()
