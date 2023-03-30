# Telegram Bot for Registration and Courses

This Telegram bot allows users to register for courses and receive notifications from the admins.

## Getting Started

### Prerequisites

- Python 3.6+
- aiogram library (install with `pip install aiogram`)
- PyMongo library (install with `pip install pymongo`)
- Telegram Bot API token (get from BotFather)

### Installation

1. Clone the repository:
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

2. Install the dependencies:
pip install -r requirements.txt

3. Create a `.env` file in the project directory and add your Telegram Bot API token and MongoDB database connection string:

BOT_TOKEN=<YOUR_BOT_TOKEN>
MONGO_URI=<YOUR_MONGODB_URI>

4. Start the bot:
python bot.py



## Usage

### Commands

- `/start` - start the bot and register for courses
- `/courses` - view the list of available courses
- `/enroll` - enroll in a course
- `/drop` - drop a course
- `/status` - view your course enrollment status

### Notifications

Admins will receive a notification when a new user registers for the platform. To enable this feature, you should have admin privileges

## Contributing

Contributions are welcome! Please open an issue or submit a pull request to suggest improvements or new features.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

