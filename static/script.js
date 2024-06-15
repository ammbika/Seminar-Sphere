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
    } else if (!validateTimeFormat(startTime)) {
        document.getElementById('startTimeError').innerHTML = 'Invalid time format. Use HH:mm 24 hour format';
        hasError = true;
    }
    // End time validation
    var endTime = document.getElementById('end_time').value;
    if (endTime.trim() === '') {
        document.getElementById('endTimeError').innerHTML = 'End time is required';
        hasError = true;
    } else if (!validateTimeFormat(endTime)) {
        document.getElementById('endTimeError').innerHTML = 'Invalid time format. Use HH:mm 24 hour format';
        hasError = true;
    } else if (!isEndTimeAfterStartTime(startTime, endTime)) {
        document.getElementById('endTimeError').innerHTML = 'End time must be after start time. Use 24 hour format';
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

function validateTimeFormat(timeString) {
    var regex = /^([01]?[0-9]|2[0-3]):[0-5][0-9]$/;
    return regex.test(timeString);
}

function isEndTimeAfterStartTime(startTime, endTime) {
    var startTimeParts = startTime.split(':');
    var endTimeParts = endTime.split(':');

    var startHour = parseInt(startTimeParts[0], 10);
    var startMinute = parseInt(startTimeParts[1], 10);
    var endHour = parseInt(endTimeParts[0], 10);
    var endMinute = parseInt(endTimeParts[1], 10);

    if (endHour > startHour) {
        return true;
    } else if (endHour === startHour && endMinute > startMinute) {
        return true;
    }
    return false;
}