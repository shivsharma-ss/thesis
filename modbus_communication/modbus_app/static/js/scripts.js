$(document).ready(function () {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    function updateWrittenBits() {
        var bits = [];
        input_signals.forEach(function(signal) {
            var checkbox = document.getElementById(signal.name);
            bits[16 - signal.port] = checkbox.checked ? 1 : 0;
        });
        var writtenBits = bits.join('');
        document.getElementById('written_bits').value = writtenBits;
    }

    function changeProgramNumber(increment) {
        var programNumberInput = document.getElementById('program_number');
        var currentProgramNumber = parseInt(programNumberInput.value) || 0;
        var newProgramNumber = currentProgramNumber + increment;
        if (newProgramNumber >= 0 && newProgramNumber <= 255) {
            programNumberInput.value = newProgramNumber;
            updateWrittenBits();
        }
    }

    $('#send-signal-btn').click(function() {
        var formData = $('#config-form').serialize();
        $.ajax({
            type: "POST",
            url: "/send_signal/",
            data: formData,
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function(response) {
                if (response.status === 'success') {
                    console.log('Signal sent successfully.');
                } else {
                    console.log('Failed to send signal.');
                }
            }
        });
    });

    setInterval(function() {
        $.ajax({
            url: "/api/data",
            method: 'GET',
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function(data) {
                output_signals = data.output_signals;
                updateOutputIndicators();
            }
        });
    }, 1000);

    function updateOutputIndicators() {
        output_signals.forEach(function(signal) {
            var indicator = document.getElementById(signal.name + "-indicator");
            if (indicator) {
                indicator.className = signal.state ? 'indicator green' : 'indicator red';
            }
        });
    }
});
