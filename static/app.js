$(document).ready(function() {
    const $form = $('#briefForm');
    const $submitBtn = $('#submitBtn');
    const $loader = $('#loader');
    const $error = $('#error');
    const $result = $('#result');

    $form.on('submit', function(e) {
        e.preventDefault();
        
        $error.hide();
        $result.hide();
        $loader.show();
        $submitBtn.prop('disabled', true).text('Generating...');
        
        const formData = {
            brand_name: $('#brandName').val().trim(),
            platform: $('#platform').val(),
            goal: $('#goal').val(),
            tone: $('#tone').val()
        };
        
        $.ajax({
            url: '/api/generate-brief/',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            success: function(response) {
                if (response.success) {
                    displayResult(response.data, response.metrics);
                } else {
                    showError(response.error || 'An error occurred');
                }
            },
            error: function(xhr) {
                let errorMessage = 'Failed to generate brief. Please try again.';
                
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMessage = xhr.responseJSON.error;
                } else if (xhr.status === 0) {
                    errorMessage = 'Network error. Please check your connection.';
                } else if (xhr.status >= 500) {
                    errorMessage = 'Server error. Please try again later.';
                }
                
                showError(errorMessage);
            },
            complete: function() {
                $loader.hide();
                $submitBtn.prop('disabled', false).text('Generate Brief');
            }
        });
    });
    
    function displayResult(data, metrics) {
        $('#briefText').text(data.brief);
        
        const $anglesList = $('#anglesList');
        $anglesList.empty();
        data.angles.forEach(function(angle) {
            $anglesList.append($('<li>').text(angle));
        });
        
        const $criteriaList = $('#criteriaList');
        $criteriaList.empty();
        data.criteria.forEach(function(criterion) {
            $criteriaList.append($('<li>').text(criterion));
        });
        
        $('#latency').text(metrics.latency_ms + 'ms');
        const totalTokens = metrics.tokens_in + metrics.tokens_out;
        $('#tokens').text(totalTokens + ' (' + metrics.tokens_in + ' in, ' + metrics.tokens_out + ' out)');
        
        $result.fadeIn();
        
        $('html, body').animate({
            scrollTop: $result.offset().top - 20
        }, 500);
    }
    
    function showError(message) {
        $error.text(message).fadeIn();
        
        $('html, body').animate({
            scrollTop: $error.offset().top - 20
        }, 500);
    }
});

