#!/usr/bin/env python
        import requests
        def main():
          endpoint = "http://127.0.0.1:8500"
          json_data = {"model_name": "model_name", "data": {"x": 1} }
          result = requests.post(endpoint, json=json_data)
          print(result.json())
        if __name__ == "__main__":
            main()
      