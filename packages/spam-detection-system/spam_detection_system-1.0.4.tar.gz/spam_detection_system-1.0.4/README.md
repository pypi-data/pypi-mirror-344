# Spam Detection System

A machine learning system that detects spam messages using Multinomial Naive Bayes classification.

## Technologies

- Python, scikit-learn, NumPy, Pandas
- Flask, Gunicorn
- HTML, CSS, JavaScript

## Installation

```bash
# Clone repository
git clone https://github.com/bniladridas/spam-detection-system.git
cd spam-detection-system

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Running Locally

```bash
python app.py
```

Access the application at http://127.0.0.1:5001/

### Using Docker

```bash
docker-compose up --build
```

Access the application at http://localhost:5001/

## API

Send a POST request to `/predict`:

```json
{
  "email_text": "Your email content here"
}
```

Response:

```json
{
  "is_spam": true/false,
  "spam_probability": 0-100,
  "message": "Spam detected!" or "Not spam."
}
```

## License

MIT License

## Model Details

- Algorithm: Multinomial Naive Bayes
- Features: Text classification with CountVectorizer
- Performance: 95% accuracy on test dataset

## Project Structure

- `app.py`: Flask application
- `spam_dataset.csv`: Training dataset
- `requirements.txt`: Dependencies
- `Dockerfile`: Docker configuration
- `docker-compose.yml`: Docker Compose setup

## Documentation

For more detailed information, see the [documentation](/docs/).