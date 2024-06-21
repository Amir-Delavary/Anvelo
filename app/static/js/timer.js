function startTimer(duration, display) {
    let timer = duration, minutes, seconds;
    const interval = setInterval(function () {
        minutes = Math.floor(timer / 60);
        seconds = Math.floor(timer % 60);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds;

        if (--timer < 0) {
            clearInterval(interval);
            alert("Time Out!");
            localStorage.removeItem("timerExpired"); // پاک کردن وضعیت تایمر از localStorage
        }
    }, 1000);
}

window.onload = function () {
    const duration = 600; // 120 ثانیه
    const display = document.getElementById('timer');
    let timerExpired = localStorage.getItem("timerExpired"); // بازیابی وضعیت تایمر از localStorage
    if (timerExpired) {
        alert("Time Outed before this");
    } else {
        startTimer(duration, display);
    }
};
