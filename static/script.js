function validateForm() {
    var hasError = false;

    // Clear previous error messages
    document.querySelectorAll('.error').forEach(el => el.innerHTML = '');

    // Title validation
    var title = document.getElementById('title').value;
    if (title.trim() === '') {
        document.getElementById('titleError').innerHTML = 'Title is required';
        hasError = true;
    }

    // Start date validation
    var startDate = document.getElementById('start_date').value;
    if (startDate.trim() === '') {
        document.getElementById('startDateError').innerHTML = 'Start date is required';
        hasError = true;
    }

    // End date validation
    var endDate = document.getElementById('end_date').value;
    if (endDate.trim() === '') {
        document.getElementById('endDateError').innerHTML = 'End date is required';
        hasError = true;
    } else if (new Date(endDate) < new Date(startDate)) {
        document.getElementById('endDateError').innerHTML = 'End date cannot be before start date';
        hasError = true;
    }

    // Start time validation
    var startTime = document.getElementById('start_time').value;
    if (startTime.trim() === '') {
        document.getElementById('startTimeError').innerHTML = 'Start time is required';
        hasError = true;
    }

    // End time validation
    var endTime = document.getElementById('end_time').value;
    if (endTime.trim() === '') {
        document.getElementById('endTimeError').innerHTML = 'End time is required';
        hasError = true;
    } else if (startDate === endDate && endTime < startTime) {
        document.getElementById('endTimeError').innerHTML = 'End time cannot be before start time on the same day';
        hasError = true;
    }

    // Location validation
    var location = document.getElementById('location').value;
    if (location.trim() === '') {
        document.getElementById('locationError').innerHTML = 'Location is required';
        hasError = true;
    }

    // Participants validation
    var participants = document.getElementById('participants').value;
    if (participants.trim() === '') {
        document.getElementById('participantsError').innerHTML = 'Number of participants is required';
        hasError = true;
    } else if (participants <= 0) {
        document.getElementById('participantsError').innerHTML = 'Number of participants must be a positive number';
        hasError = true;
    }

    // Description validation
    var description = document.getElementById('description').value;
    if (description.trim() === '') {
        document.getElementById('descriptionError').innerHTML = 'Description is required';
        hasError = true;
    }

    return !hasError;
}
