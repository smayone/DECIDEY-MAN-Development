# ISO20022 to Ethereum Translator

This project translates ISO20022 bank transactions to Ethereum blockchain with a central dashboard for DECIDEY NGO and MAN project, using Flask and Web3.py.

## Features

- ISO20022 message parsing and translation
- Integration with multiple bank APIs and ACH systems
- Ethereum blockchain integration
- Central dashboard for transaction management
- Robust error handling and transaction verification

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

The system now includes robust error handling and transaction verification:

- Improved logging throughout the application
- Transaction verification in both DECIDEY and MAN modules
- Enhanced error reporting in API responses
- Database transaction rollback on errors

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
