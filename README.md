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
   git clone https://github.com/yourusername/dental-appointment-scheduler.git
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


### Example Output

When you run the script, you'll see debug and info logs, followed by the available appointment slots. Here's an example of what the output might look like:

```
2024-09-23 03:18:44,612 - DEBUG - Initializing browser
2024-09-23 03:18:53,053 - INFO - Browser initialized
2024-09-23 03:18:53,054 - DEBUG - Navigating to https://onlinebooking.mydentistlink.com/f0398585-a097-4b03-9313-83f79da43804/dafb6490-5320-4145-bf16-8176a195e379
2024-09-23 03:19:02,027 - INFO - Successfully navigated to scheduling page: https://onlinebooking.mydentistlink.com/f0398585-a097-4b03-9313-83f79da43804/dafb6490-5320-4145-bf16-8176a195e379
2024-09-23 03:19:02,029 - DEBUG - Selecting patient type: New Patient
2024-09-23 03:19:02,146 - INFO - Selected patient type: New Patient
2024-09-23 03:19:02,205 - INFO - Clicked on Continue button after selecting patient type
2024-09-23 03:19:02,223 - DEBUG - Selecting appointment type: New appointment
2024-09-23 03:19:06,374 - INFO - Selected appointment type: New appointment
2024-09-23 03:19:06,378 - DEBUG - Getting available slots for date: 2024-09-25
2024-09-23 03:19:06,562 - INFO - Available slots for 2024-09-25: [{'date': '2024-09-25', 'time': '2:00 PM', 'datetime': '2024-09-24T14:00'}, {'date': '2024-09-25', 'time': '3:30 PM', 'datetime': '2024-09-25T15:30'}, ...]
2024-09-23 03:19:06,563 - DEBUG - Closing browser
2024-09-23 03:19:06,931 - INFO - Browser closed

Available slots:
[
  {'date': '2024-09-25', 'time': '2:00 PM', 'datetime': '2024-09-24T14:00'} ,
  {'date': '2024-09-25', 'time': '3:30 PM', 'datetime': '2024-09-25T15:30'} ,
  {'date': '2024-09-25', 'time': '4:00 PM', 'datetime': '2024-09-25T16:00'} ,
  {'date': '2024-09-25', 'time': '8:30 AM', 'datetime': '2024-09-26T08:30'} ,
  {'date': '2024-09-25', 'time': '9:00 AM', 'datetime': '2024-09-26T09:00'} ,
  {'date': '2024-09-25', 'time': '10:00 AM', 'datetime': '2024-09-26T10:00'} ,
  {'date': '2024-09-25', 'time': '1:00 PM', 'datetime': '2024-09-26T13:00'} ,
]
```

This output shows the script's progress through the scheduling process and the final list of available appointment slots for the specified date.


## Configuration

The main configurable parameters are:
- `patient_type`: "New Patient" or "Returning Patient"
- `appointment_type`: "New appointment", "Emergency appointment", or "Invisalign consultation"
- `date_preference`: Specific date for the desired appointment (e.g., "2024-09-25")

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

This project is licensed under the MIT License - see the LICENSE file for details.



