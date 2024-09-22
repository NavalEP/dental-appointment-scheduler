# Dental Appointment Scheduler

An asynchronous Python script for automating dental appointment scheduling using Playwright.

## Description

This project automates the process of checking available dental appointment slots on a specific scheduling website. It uses Playwright for web automation and provides a flexible, error-resistant approach to navigating through the appointment booking process.

## Features

- Asynchronous web automation using Playwright
- Customizable patient type and appointment type selection
- Date preference setting
- Caching of retrieved appointment slots
- Error handling and retry mechanism
- Logging for better debugging and monitoring
- Screenshot capture for error analysis

## Prerequisites

- Python 3.7+
- Playwright
- asyncio

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/NavalEP/dental-appointment-scheduler.git
   cd dental-appointment-scheduler
   ```

2. Install the required packages:
   ```
   pip install playwright asyncio
   ```

3. Install Playwright browsers:
   ```
   playwright install
   ```

## Usage

To run the script, use the following command:

```
python main.py
```

You can modify the `main()` function in the script to customize the patient type, appointment type, and date preference.

## Configuration

The main configurable parameters are:

- `patient_type`: "New Patient" or "Returning Patient"
- `appointment_type`: "New appointment", "Emergency appointment", or "Invisalign consultation"
- `date_preference`: The day of the month for the desired appointment (e.g., "25")

## Error Handling

The script includes robust error handling:

- Timeouts are managed to prevent the script from hanging
- Screenshots are captured when errors occur for easier debugging
- A retry mechanism is implemented with exponential backoff

## Logging

Detailed logs are written to help with monitoring and debugging. Log files are created in the project directory.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This script is for educational purposes only. Please ensure you have permission to automate interactions with the target website before using this script.

## Contact

For any queries, please open an issue on this GitHub repository.
