# EasyBankX 🏦💰
Note: Please consider starring ⭐ and forking this repository if you find the project useful. Your support will encourage me to continue improving and adding new features. Contributions are also welcome; see the "Contributing" section below for more details.
#
EasyBankX is a user-friendly Django-based banking website that allows users to easily manage their accounts and perform various banking operations. The website provides a smooth user interface for account registration, login, fund transfers, transaction history, and more. Administrators have access to manage users and transactions efficiently.

# Features ✨

User Registration and Login: New users can register and existing users can securely log in to their accounts.

Account Management: Users can add money to their account and withdraw money as needed. 

Fund Transfer: Transfer money to other bank users' accounts with ease.
Transaction 

History: Users can view their transaction history for reference and tracking.

Admin Panel: Administrators have the authority to add and remove users and manage transactions.

# How to Run the Project

To run the EasyBankX website on your local machine, follow these steps:

Clone the Repository:

git clone https://github.com/shallanidevi/EasyBankX.git

Use the cd command to navigate to the directory where you want to create your virtual environment. 

cd EasyBankX

Set Up Virtual Environment (Optional):

It's recommended to use a virtual environment to isolate project dependencies.



# Linux/MacOS
python3 -m venv env
source env/bin/activate

# Windows
python -m venv env
.\env\Scripts\activate
#
Install Dependencies:
pip install -r requirements.txt

Run Migrations:
python manage.py migrate

Create Superuser (Admin):
python manage.py createsuperuser

Run the Development Server:
python manage.py runserver

# Access the Website 🌐

Open your web browser and go to http://localhost:8000 to access the EasyBankX website. Use the admin credentials to access the admin panel at http://localhost:8000/admin

# How to contribute 📙

Thank you for considering contributing to EasyBankX! Your contributions help make this project better for everyone. Here are some ways you can contribute:

Report Bugs 🐛 : If you encounter any bugs or issues, please open an issue on the GitHub repository.

Request Features: If you have any ideas for new features or improvements, please create an issue to discuss them.

Submit Pull Requests: If you'd like to contribute directly to the codebase, fork the repository, make your changes, and submit a pull request for review.

Spread the Word: You can also contribute by spreading the word about EasyBankX, starring the repository, and sharing it with others who might find it useful.

# License

This project is licensed under the MIT License. You are free to use, modify, and distribute the code as per the terms of the license.


# Contact🤝

For any questions or feedback, please feel free to contact us at shallani2020@gmail.com
