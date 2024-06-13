# Usability Evaluation for Shopping Websites

## Project Overview

This project aims to help shopping website developers improve the usability of their website design and enhance the user experience. We achieve this by creating a platform that uses an intelligent method to automatically evaluate the usability of shopping websites.

## Objectives

1. **Define Usability Criteria**: Establish the criteria that will be used to evaluate the usability of shopping websites.
2. **Collect and Label Data**: Gather and label dataset samples of fashion shopping websites for model training.
3. **Build Evaluation Model**: Develop a convolutional neural network (CNN) model to evaluate the usability of websites.
4. **Design Interfaces**: Create user-friendly interfaces for the proposed system.
5. **Develop the Website**: Implement the website for the proposed system.
6. **Integrate Model**: Connect the website with the evaluation model for real-time usability assessment.

## Features

- **Automated Usability Evaluation**: Automatically assesses the usability of shopping websites using advanced algorithms.
- **User Experience Enhancement**: Provides actionable insights to improve the overall user experience.
- **Detailed Reporting**: Generates comprehensive reports highlighting usability issues and suggestions for improvement.
- **Easy Integration**: Designed to be easily integrated with existing shopping websites.

## Getting Started

### Prerequisites

- Python 3.8 or later
- Flask 2.0 or later
- pip

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/usability-evaluation.git
    ```
2. Navigate to the project directory:
    ```bash
    cd usability-evaluation
    ```
3. Create a virtual environment:
    ```bash
    python -m venv venv
    ```
4. Activate the virtual environment:
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```
5. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Project

1. Start the Flask development server:
    ```bash
    flask run
    ```
2. Open your browser and go to `http://localhost:5000` to view the application.

### Running Tests

1. Run the test suite:
    ```bash
    pytest
    ```

## Usage

1. Open the application in your browser.
2. Enter the URL of the shopping website you wish to evaluate.
3. View the generated usability report and take action based on the provided insights.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add your feature'`).
5. Push to the branch (`git push origin feature/your-feature`).
6. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or suggestions, please contact [your-email@example.com].
