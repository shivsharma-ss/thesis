function updateWrittenBits() {
    let bits = [];
    $("input[type=checkbox]").each(function() {
        bits.unshift(this.checked ? 1 : 0);
    });
    let writtenBits = bits.join('');
    document.getElementById("written_bits").value = writtenBits;
    updateProgramNumber(bits);
}

function updateProgramNumber(bits) {
    let programNumberBits = bits.slice(-8);  // Last 8 bits for ProgramAck
    let programNumber = parseInt(programNumberBits.join(''), 2);
    document.getElementById("program_number").value = programNumber;
}

function sendSignal() {
    let form = $("#config-form");
    $.post(form.attr("action"), form.serialize(), function(data) {
        if (data.status === 'success') {
            console.log('Signal sent successfully');
        } else {
            console.log('Failed to send signal');
        }
    });
}

$(document).ready(function() {
    $("#config-form").on("change", "input[type=checkbox], input[type=number]", updateWrittenBits);
    $("#send-signal-btn").on("click", function(event) {
        event.preventDefault();  // Prevent form from submitting normally
        sendSignal();
    });
});
