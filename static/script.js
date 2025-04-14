$(document).ready(function() {
    function clearResults() {
        $('#resultCard').addClass('d-none');
        $('#resultVegetable').text('');
        $('#resultDate').text('');
        $('#resultMinPrice').text('');
        $('#resultMaxPrice').text('');
    }

    function showError(message) {
        // Create or update error alert
        let errorAlert = $('.alert-danger');
        if (errorAlert.length === 0) {
            errorAlert = $('<div class="alert alert-danger" role="alert"></div>');
            $('#predictionForm').before(errorAlert);
        }
        errorAlert.text(message);
    }

    function clearError() {
        $('.alert-danger').remove();
    }

    $('#predictionForm').on('submit', function(e) {
        e.preventDefault();
        clearResults();
        clearError();

        const vegetable = $('#vegetable').val();
        const date = $('#date').val();

        if (!vegetable || !date) {
            showError('Please select both vegetable and date');
            return;
        }

        console.log('Submitting request with:', {
            vegetable: vegetable,
            date: date,
            timestamp: new Date().toISOString()
        });

        // Show loading state
        const submitButton = $(this).find('button[type="submit"]');
        const originalButtonText = submitButton.text();
        submitButton.prop('disabled', true).text('Loading...');

        // Make the AJAX request
        $.ajax({
            url: '/get_prediction',
            type: 'POST',
            data: {
                vegetable: vegetable,
                date: date
            },
            beforeSend: function() {
                console.log('Sending request for', vegetable, 'on', date);
            },
            success: function(response) {
                console.log('Server response for', vegetable, 'on', date, ':', response);
                
                if (response.success && response.data) {
                    try {
                        $('#resultVegetable').text(response.data.vegetable || '');
                        $('#resultDate').text(response.data.date || '');
                        $('#resultMinPrice').text(response.data.min_price ? response.data.min_price.toFixed(2) : '');
                        $('#resultMaxPrice').text(response.data.max_price ? response.data.max_price.toFixed(2) : '');
                        $('#resultCard').removeClass('d-none');
                    } catch (err) {
                        console.error('Error processing response:', err);
                        showError('Error displaying results. Please try again.');
                    }
                } else {
                    console.log('No data or error in response:', response);
                    showError(response.message || 'No prediction found');
                }
            },
            error: function(xhr, status, error) {
                console.log('Request failed for', vegetable, 'on', date, ':', {
                    status: status,
                    error: error,
                    response: xhr.responseText
                });
                showError('Failed to get prediction. Please try again.');
            },
            complete: function() {
                submitButton.prop('disabled', false).text(originalButtonText);
            }
        });
    });

    // Monitor input changes
    $('#vegetable, #date').on('change', function() {
        const inputId = $(this).attr('id');
        const value = $(this).val();
        console.log(`${inputId} changed to:`, value);
        clearResults();
        clearError();
    });
}); 