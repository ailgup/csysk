// highlight.js
$(document).ready(function() {
    var audioPlayer = document.getElementById('audioPlayer');
    var previousHighlightedSpan = null;

    // Highlight the currently spoken utterance
    audioPlayer.addEventListener('timeupdate', function() {
        var currentTime = audioPlayer.currentTime;
        var spans = $('span.dictation');
        var currentHighlightedSpan = null;

        // Find the current span to highlight
        spans.each(function() {
            var timestamp = parseFloat($(this).attr('timestamp'));
            if (timestamp <= currentTime) {
                currentHighlightedSpan = this;
                //return false;
            }
        });

        // Remove highlight from previous highlighted span
        if (previousHighlightedSpan !== null) {
            $(previousHighlightedSpan).removeClass('highlight');
        }

        // Highlight the current span
        if (currentHighlightedSpan !== null) {
            $(currentHighlightedSpan).addClass('highlight');
            previousHighlightedSpan = currentHighlightedSpan;
        }
    });
});
