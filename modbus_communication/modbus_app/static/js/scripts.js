/* static/js/scripts.js */
function updateWrittenBits() {
    const formData = $('#config-form').serializeArray();
    let bits = Array(16).fill(0);

    formData.forEach(item => {
        if (item.name === 'program_number') {
            let programBits = parseInt(item.value).toString(2).padStart(8, '0').split('').map(Number);
            for (let i = 0; i < programBits.length; i++) {
                bits[8 + i] = programBits[i];
            }
        } else {
            bits[{
                enable: 0,
                clockwise: 1,
                counter_clockwise: 2,
                ready: 3,
                ok: 4
            }[item.name]] = item.value === 'true' || item.value === 'on' ? 1 : 0;
        }
    });

    $('#written_bits').val(bits.join(''));
}

function changeProgramNumber(delta) {
    let currentValue = parseInt($('#program_number').val());
    let newValue = currentValue + delta;
    if (newValue >= 0 && newValue <= 255) {
        $('#program_number').val(newValue);
        updateWrittenBits();
    }
}

$('#send-signal-btn').click(function() {
    $.ajax({
        type: 'POST',
        url: $('#config-form').attr('action'),
        data: $('#config-form').serialize(),
        success: function(response) {
            alert('Signal sent successfully.');
        },
        error: function() {
            alert('Failed to send signal.');
        }
    });
});

$('#edit-ip-btn').click(function() {
    $('#ip_address').prop('disabled', false);
});

$('#edit-port-btn').click(function() {
    $('#port').prop('disabled', false);
});

$('#config-form').submit(function(event) {
    event.preventDefault();
    $.ajax({
        type: 'POST',
        url: $('#config-form').attr('action'),
        data: $(this).serialize(),
        success: function(response) {
            $('#received_bits').val(response.received_bits);
            updateIndicators(response.received_bits);
        },
        error: function() {
            alert('Failed to update signals.');
        }
    });
});

function updateIndicators(bits) {
    const bitArray = bits.split('');
    document.getElementById('ready-indicator').className = bitArray[3] == '1' ? 'indicator green' : 'indicator red';
    document.getElementById('nok-indicator').className = bitArray[5] == '1' ? 'indicator green' : 'indicator red';
    document.getElementById('cycle-complete-indicator').className = bitArray[7] == '1' ? 'indicator green' : 'indicator red';
    document.getElementById('ok-indicator').className = bitArray[4] == '1' ? 'indicator green' : 'indicator red';
    document.getElementById('in-cycle-indicator').className = bitArray[6] == '1' ? 'indicator green' : 'indicator red';
}
