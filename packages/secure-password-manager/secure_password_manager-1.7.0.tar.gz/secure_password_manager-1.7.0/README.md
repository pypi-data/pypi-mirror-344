# 🔐 Password Manager

A secure Password Manager built with Python that securely stores your passwords locally using strong encryption.

## 🚀 Features

- **Secure Storage**: All passwords encrypted with Fernet symmetric encryption
- **Password Management**: Add, view, edit, and delete passwords
- **Security Analysis**: Password strength evaluation and suggestions
- **Password Generator**: Create strong, random passwords
- **Master Password**: Protect access with a master password
- **Two-Factor Authentication**: Additional security with TOTP (Time-based One-Time Password)
- **Categorization**: Organize passwords by category
- **Security Audit**: Find weak, reused, expired, or breached passwords
- **Backup & Restore**: Export/import functionality
- **Password Expiration**: Set expiry dates for passwords
- **Command-Line Interface**: User-friendly CLI with color formatting
- **GUI Interface**: Optional PyQt5 graphical interface
- **Activity Logging**: Track all important actions

## 🛠️ Installation

### Option 1: Install from PyPI (Recommended)

The simplest way to install Secure Password Manager:

```bash
pip install secure-password-manager
```

After installation, you can run the application with:

```bash
# For the command-line interface
password-manager

# For the graphical interface
password-manager-gui
```

### Option 2: Install from Source

1. Clone the repository:

    ```bash
    git clone https://github.com/ArcheWizard/password-manager.git
    cd password-manager
    ```

2. Create and activate a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

3. Install the package in development mode:

    ```bash
    pip install -e .
    ```

## 🛡️ Requirements

- Python 3.8+
- Core dependencies (installed automatically):
  - `cryptography`: For secure encryption
  - `PyQt5`: For the GUI interface
  - `zxcvbn`: For password strength analysis
  - `pillow`: For image processing
  - Additional dependencies as listed in `requirements.txt`

## 📂 Project Structure

The project is organized into modules for maintainability and separation of concerns:

```plaintext
password-manager/
├── apps/                  # Application code
│   ├── __init__.py        # Package initialization
│   ├── app.py             # CLI application entry point
│   └── gui.py             # GUI application entry point
├── utils/                 # Core utilities
│   ├── auth.py            # Authentication
│   ├── backup.py          # Import/export 
│   ├── crypto.py          # Encryption/decryption
│   ├── database.py        # Database operations
│   ├── interactive.py     # CLI input utilities
│   ├── logger.py          # Logging facilities
│   ├── password_analysis.py # Password evaluation
│   ├── security_analyzer.py # Breach checking
│   ├── security_audit.py  # Security auditing
│   ├── two_factor.py      # 2FA implementation
│   └── ui.py              # UI formatting
├── tests/                 # Unit & integration tests
└── README.md              # Project documentation
```

## 📸 Screenshots

### Home Screen

![Home Screen](screenshots/Home.png)

### Adding a Password

![Add Password](screenshots/Add_Password.png)

### Editing a Password

![Edit Password](screenshots/Edit_Password.png)

### Security Audit

![Security Audit](screenshots/Security.png)

### Backup Options

![Backup](screenshots/Backup.png)

### Exporting Passwords

![Export](screenshots/Export.png)

### Importing Passwords

![Import](screenshots/Import.png)

## 🔒 How It Works

### Security Model

This Password Manager uses a multi-layered security approach:

1. **Master Password**: Access to the application is protected by a master password that is never stored directly. Instead, a salted hash is stored using PBKDF2 with 100,000 iterations.

2. **Encryption**: All passwords are encrypted using Fernet symmetric encryption (AES-128 in CBC mode with PKCS7 padding).

3. **Key Management**: The encryption key is stored locally and is used for encrypting/decrypting the stored passwords.

4. **Database**: Passwords are stored in a local SQLite database, with the password values stored as encrypted binary data.

5. **Backup Protection**: When exporting passwords, the entire backup file is encrypted using the same strong encryption.

### Data Flow

1. When adding a password:
   - Password is encrypted using the local key
   - Encrypted data is stored in the SQLite database

2. When viewing passwords:
   - Encrypted data is retrieved from the database
   - Each password is decrypted for display

3. When exporting passwords:
   - All passwords are decrypted
   - The entire password list is serialized to JSON
   - The JSON is encrypted and written to a file

## 📚 Future Improvements

- ✅ Add a Master Password authentication
- ✅ Password strength evaluation and generator
- ✅ Unit tests for critical functions
- ✅ Backup and restore functionality
- ✅ Add a search function for passwords
- ✅ Add password categories/tags
- ✅ Add password expiration notifications
- ✅ GUI version (PyQT)
- ✅ Package available on PyPI
- Two-factor authentication
- Password history tracking
- Cross-platform desktop application (using PyInstaller)
- Docker support

## 👨‍💻 Author

- **ArcheWizard** – [GitHub Profile](https://github.com/ArcheWizard)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
