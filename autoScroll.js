// Function to scroll to the currently playing timestamp
function scrollToCurrentTimestamp() {
    // Get the currently playing timestamp from the audio player
    let currentTime = audioPlayer.currentTime;

    // Find the span element with matching timestamp
    let spans = document.querySelectorAll('span[timestamp]');
    let targetSpan = null;
    spans.forEach(span => {
        if (parseFloat(span.getAttribute('timestamp')) <= currentTime) {
            targetSpan = span;
            //console.log("targetSpan: ", targetSpan)
        }
    });

    // Scroll to the target span if found
    if (targetSpan) {
        targetSpan.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'nearest' });
    }
}

// Variable to track user scrolling
let isUserScrolling = false;

// Add event listener to detect user scrolling
window.addEventListener('scroll', () => {
    isUserScrolling = true;
});

// Function to handle automatic scrolling
function handleAutomaticScroll() {
    if (!isUserScrolling) {
        scrollToCurrentTimestamp();
    }
}

// Call handleAutomaticScroll when the audio playback progresses
audioPlayer.addEventListener('timeupdate', () => {
    handleAutomaticScroll();
});

// Call handleAutomaticScroll when the user interacts with the page
window.addEventListener('mousedown', () => {
    isUserScrolling = true;
});

window.addEventListener('touchstart', () => {
    isUserScrolling = true;
});

window.addEventListener('wheel', () => {
    isUserScrolling = true;
});

// Reset isUserScrolling after a brief delay
window.addEventListener('mousemove', () => {
    setTimeout(() => {
        isUserScrolling = false;
    }, 100);
});

window.addEventListener('touchend', () => {
    setTimeout(() => {
        isUserScrolling = false;
    }, 100);
});

window.addEventListener('mouseup', () => {
    setTimeout(() => {
        isUserScrolling = false;
    }, 100);
});
