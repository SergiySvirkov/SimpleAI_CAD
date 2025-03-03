## Simple AI to CAD Tool from Point Cloud

### Project Overview
This project is designed to convert point cloud data (.RCP format) into simple CAD shapes (walls, floors, ceilings, and concrete shafts) using AI. The tool provides a web-based interface for uploading files, processing data in the cloud, and exporting to AutoCAD (Solid 3D preferred, or surface as a minimum) and Revit formats.

### Features
- Supports large .RCP files (up to 10GB)
- AI-powered recognition of key structures
- Cloud-based processing for scalability
- Exports to AutoCAD and Revit
- Simple UI with preview & manual correction options
- Multiple file processing support (future development)

### Project Structure

SimpleAI_CAD/
│── app/                     # Main application logic
│   │── __init__.py
│   │── main.py              # Entry point of the application
│   │── config.py            # Configuration settings
│   │── utils.py             # Helper functions
│── modules/                 # AI processing & CAD conversion modules
│   │── ai_processor.py      # AI model for point cloud recognition
│   │── cad_converter.py     # Conversion of AI output to CAD format
│   │── file_handler.py      # Handling of .RCP and other file formats
│── web/                     # Web interface for interaction
│   │── app.py               # Flask/FastAPI backend
│   │── templates/           # HTML templates
│   │── static/              # CSS, JS, and assets
│── models/                  # Pretrained AI models and configurations
│── data/                    # Sample data for testing
│── requirements.txt         # Dependencies
│── README.md                # Project documentation
│── Dockerfile               # Deployment configuration


### Installation
#### Prerequisites
- Python 3.8+
- Docker (for containerized deployment)
- NVIDIA GPU (for AI model acceleration, optional but recommended)

#### Setup
1. Clone the repository:
   git clone https://github.com/your-repo/SimpleAI_CAD.git
   cd SimpleAI_CAD
   
2. Install dependencies:
   pip install -r requirements.txt
   
3. Run the application:
   python app/main.py
   

### Deployment (Using Docker)
1. Build the Docker image:
   docker build -t simple_ai_cad .
   
2. Run the container:
   docker run -p 5000:5000 simple_ai_cad
