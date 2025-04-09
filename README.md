# Annadata.ai

Annadata.ai is an intelligent, full-stack farming dashboard designed to empower farmers with actionable insights and tools for effective decision-making. The platform leverages AI agents, real-time data, and predictive analytics to provide market research, crop recommendations, and advisory services.

## Features

1. **AI-Powered Advisors**:
   - **Farmer Advisor AI**: Provides personalized farming recommendations based on soil quality, weather, and crop suitability.
   - **Market Researcher AI**: Analyzes market trends, crop pricing, and demand forecasts to suggest the most profitable crops.

2. **Real-Time Data Integration**:
   - Weather updates displayed in the Advisor section.
   - Market data scraped from reliable sources to ensure accurate predictions.

3. **User Dashboard**:
   - Easy-to-navigate interface with sections for History, Advisor, and Market Prediction.
   - Language switcher for English and Hindi.
   - Login/Sign-up functionality with personalized dashboard experience.

4. **Backend and Data Management**:
   - Flask-based backend handling user registration, authentication, and agent integration.
   - SQLite database for efficient data storage.

5. **Technologies Used**:
   - **Frontend**: ReactJS, Tailwind CSS for dynamic and responsive UI.
   - **Backend**: Flask framework for API handling and business logic.
   - **Database**: SQLite for lightweight and robust data management.
   - **AI Models**: TinyLlama LLM agents for intelligent processing and predictions.

## Installation and Setup

Follow these steps to set up Annadata.ai on your local machine:

### Prerequisites
- Python 3.9+
- Node.js and npm
- SQLite

### Backend Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Sim14code/Annadata.ai.git
   cd Annadata.ai/backend
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the backend server:
   ```bash
   python app.py
   ```

### Frontend Setup
1. Navigate to the frontend folder:
   ```bash
   cd ../frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm start
   ```

### Accessing the App
- Open your browser and navigate to `http://localhost:3000` to access the frontend.

## Usage
- Register or log in to access your personalized dashboard.
- Use the Advisor section to get farming recommendations.
- Use the Market Prediction section to view detailed market analysis and predictions.
