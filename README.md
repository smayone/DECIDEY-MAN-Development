# DECIDEY-MAN-Development

This repository houses the development of DECIDEY (pronounced dee-see-day), a Decentralized Empowerment Control Identity Data Economy of Yours, an AI-powered blockchain-based charitable organization. 

## Project Overview

DECIDEY supports SOLVY (Solution Valued You), a web3 digital finance platform with Ethereum blockchain security and SelfKey SSID for user identity, and MAN (Mandatory Audit Network), its transparent financial management system. 

This project translates ISO20022 bank transactions to Ethereum blockchain with a central dashboard for DECIDEY NGO and MAN project, using Flask and Web3.py.

## Features

- ISO20022 message parsing and translation
- Integration with multiple bank APIs and ACH systems
- Ethereum blockchain integration
- Central dashboard for transaction management
- Robust error handling and transaction verification

## Our Mission

DECIDEY's mission is to empower individuals through data control and charitable initiatives, including facilitating US tax repatriation for technology corporations. We aim to create a transparent and efficient ecosystem that fosters economic growth and social impact.

## Core Technologies

- **Blockchain:** Leveraging Ethereum for secure and transparent transactions
- **Artificial Intelligence (AI):** Using TensorFlow or PyTorch for data analysis and decision-making
- **Smart Contracts:** Implemented in Solidity for automated functions
- **Flask:** Web framework for the backend
- **Web3.py:** For Ethereum integration

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   - `DATABASE_URL`: PostgreSQL database URL
   - `SECRET_KEY`: Secret key for Flask application
   - `ETHEREUM_NODE_URL`: URL for Ethereum node
   - Add any additional API keys for bank integrations

4. Initialize the database:
   ```
   flask db upgrade
   ```

## Running the Application

To run the Flask application:

```
python main.py
```

The application will be available at `http://localhost:5000`.

## Running Tests

To run the test script:

```
python test_multiple_apis.py
```

This script tests the integration with multiple banks and ACH systems, as well as error handling for invalid inputs.

## Error Handling and Transaction Verification

The system includes robust error handling and transaction verification:

- Improved logging throughout the application
- Transaction verification in both DECIDEY and MAN modules
- Enhanced error reporting in API responses
- Database transaction rollback on errors

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## Get Involved

- Explore our wiki: [Link to your wiki]
- Fork this repository and contribute your code
- Share your ideas and feedback
- Connect with us on [Facebook](https://www.facebook.com/SANathanLLC/)

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.

Let's create a more transparent, efficient, and impactful profitable world together! 🤝
