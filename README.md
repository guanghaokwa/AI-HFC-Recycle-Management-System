<h1>♻️GreenHub AI</h1>


<h1>Project Description: AI-Powered Waste Classification and Recycling Awareness System</h1>
Singapore's domestic recycling rate has remained low, largely due to incorrect recycling practices and contamination of recyclables. To address these challenges, our project leverages image processing, AI technology, and gamification to create a comprehensive solution that aligns with the Singapore Green Plan 2030 and the Zero Waste Masterplan, contributing to the nation’s sustainability goals. <br> <br>

Our Waste Classification System uses image processing to analyze photos of waste and classify items as recyclable or non-recyclable. By providing accurate classification, the system reduces contamination in recyclables, ensuring that more materials are effectively recycled. This directly supports the Zero Waste Masterplan’s objective of achieving a 30% domestic recycling rate by 2030. 

The system is enhanced by an AI-Powered Assistant, which allows users to ask about recyclable items and learn how to dispose of waste correctly. By providing accessible guidance, the assistant promotes awareness of recycling practices and highlights how individual recycling efforts contribute to Singapore's sustainability goals, aligning with the Green Plan's vision of fostering eco-conscious habits among citizens.

To encourage widespread participation, the project incorporates a Gamification System, rewarding users for correct recycling practices. This incentive-driven approach motivates long-term behavior change and helps build a community committed to responsible waste management.

<h1>Prerequisites</h1>
1. 2 NGROK Token (1 for Google Colab and 1 for local Flask App) <br>
2. Imported database file into local PgAdmin 4 PostgreSQL

<h1>Setup Instructions</h1>
1. Create a python virtual environment, run the following command

```bash
python -m venv venv
```

2. Start the virtual environment, run the following command:

```bash
venv\Scripts\Activate
```

3. Install all packages from the requirements.txt file into the virtual environment, run the following command: (Install packages seperately if "module not found" error happens)

```bash
pip install -r requirements.txt
```

4. Access the Google Colab file  [Open in Google Colab](https://colab.research.google.com/drive/1abc2d34efgh5678)

5. Add "best.pt" file into "content" folder for runtime

6. Run all code in order from top to bottom

7. Copy NGROK url when running the last code in colab. For example: "https://e93c-34-82-254-178.ngrok-free.app"

8. Replace the following variables NGROK URL in your local flask app: <br>
 COLAB_NGROK_URL = "YOUR_NGROK_URL/process" <br>
 colab_url = "YOUR_NGROK_URL/predict"

9. Lastly, run the following command to start your local flask app

```bash
python main.py
```

<h1>Usage Guide</h1>

<h1>Contributors</h1>

<div style="display: flex; justify-content: start; align-items: center; margin-bottom: 10px;">
  <div style="display: flex; align-items: center; margin-right: 20px;">
    <img src="https://media.licdn.com/dms/image/v2/C5603AQHv2AmaxZ-KJw/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1604580823762?e=1741824000&v=beta&t=mtcJvCBRKRusRDdjavKW7LWKfwkppsMZ6rjgF7CKTi0" alt="Contributor 1" style="width: 150px; height: 150px; border-radius: 50%; margin-right: 10px;">
    <a href="https://www.linkedin.com/in/kwa-guang-hao-98213y/" target="_blank" style="font-weight: bold;">Kwa Guang Hao</a>
  </div>

  <div style="display: flex; align-items: center; margin-right: 20px;">
    <img src="https://media.licdn.com/dms/image/v2/C4D03AQFxkjoL41Vq-A/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1653217262059?e=1741824000&v=beta&t=TvWk4l4zIGtdzMbUJtk6-2V6hf2PcJ5lR5XgBSeuuGM" alt="Contributor 2" style="width: 150px; height: 150px; border-radius: 50%; margin-right: 10px;">
    <a href="https://www.linkedin.com/in/kevansoon/" target="_blank" style="font-weight: bold;">Kevan Soon</a>
  </div>
</div>

  <div style="display: flex; align-items: center; margin-right: 20px;">
    <img src="https://media.licdn.com/dms/image/v2/C5603AQFidBM2K2d3kA/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1636695735903?e=1741824000&v=beta&t=B7t6_dv033Av4Zxrdg0nCCo2PpVNrdoeerP575slQTw" alt="Contributor 3" style="width: 150px; height: 150px; border-radius: 50%; margin-right: 10px;">
    <a href="https://www.linkedin.com/in/zulfaqarhafez/" target="_blank" style="font-weight: bold;">Zulfaqar Hafez</a>
  </div>
</div>

  <div style="display: flex; align-items: center; margin-right: 20px;">
    <img src="https://media.licdn.com/dms/image/v2/D5603AQEyiGzENyH1bg/profile-displayphoto-shrink_400_400/B56ZRUuMB.G8Ag-/0/1736588182873?e=1741824000&v=beta&t=ngroT--AxMlb7qWdIaZIj5AKxP0xaJe0ygQdcF_EvFU" alt="Contributor 4" style="width: 150px; height: 150px; border-radius: 50%; margin-right: 10px;">
    <a href="https://www.linkedin.com/in/amir-ashraf-45464119b/" target="_blank" style="font-weight: bold;">Amir Ashraf</a>
  </div>
</div>

<h1>Additional Notes</h1>
