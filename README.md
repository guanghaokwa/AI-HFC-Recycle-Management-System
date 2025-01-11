<h1>♻️GreenHub AI</h1>


<h1>Project Description: AI-Powered Waste Classification and Recycling Awareness System</h1>
Singapore's domestic recycling rate has remained low, largely due to incorrect recycling practices and contamination of recyclables. To address these challenges, our project leverages image processing, AI technology, and gamification to create a comprehensive solution that aligns with the Singapore Green Plan 2030 and the Zero Waste Masterplan, contributing to the nation’s sustainability goals.

Our Waste Classification System uses image processing to analyze photos of waste and classify items as recyclable or non-recyclable. By providing accurate classification, the system reduces contamination in recyclables, ensuring that more materials are effectively recycled. This directly supports the Zero Waste Masterplan’s objective of achieving a 30% domestic recycling rate by 2030.

The system is enhanced by an AI-Powered Assistant, which provides real-time guidance and education on proper recycling practices. Users can upload images of waste to receive feedback and disposal instructions. This promotes awareness and fosters a culture of recycling, aligning with the Green Plan's goal of instilling sustainability habits among citizens.

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

4. Access the Google Colab file 

[Open in Google Colab](https://colab.research.google.com/drive/1abc2d34efgh5678)

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
    <img src="https://example.com/profile-image.jpg" alt="Contributor 1" style="width: 50px; height: 50px; border-radius: 50%; margin-right: 10px;">
    <a href="https://www.linkedin.com/in/contributor1" target="_blank" style="font-weight: bold;">Contributor 1</a>
  </div>

  <div style="display: flex; align-items: center; margin-right: 20px;">
    <img src="https://example.com/profile-image2.jpg" alt="Contributor 2" style="width: 50px; height: 50px; border-radius: 50%; margin-right: 10px;">
    <a href="https://www.linkedin.com/in/contributor2" target="_blank" style="font-weight: bold;">Contributor 2</a>
  </div>
</div>

  <div style="display: flex; align-items: center; margin-right: 20px;">
    <img src="https://example.com/profile-image2.jpg" alt="Contributor 2" style="width: 50px; height: 50px; border-radius: 50%; margin-right: 10px;">
    <a href="https://www.linkedin.com/in/contributor2" target="_blank" style="font-weight: bold;">Contributor 2</a>
  </div>
</div>

  <div style="display: flex; align-items: center; margin-right: 20px;">
    <img src="https://example.com/profile-image2.jpg" alt="Contributor 2" style="width: 50px; height: 50px; border-radius: 50%; margin-right: 10px;">
    <a href="https://www.linkedin.com/in/contributor2" target="_blank" style="font-weight: bold;">Contributor 2</a>
  </div>
</div>

<h1>Additional Notes</h1>
