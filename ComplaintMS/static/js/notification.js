
  // Automatically close alert boxes after a certain time (e.g., 5 seconds)
  const alertBoxes = document.querySelectorAll(".alert-box");
  alertBoxes.forEach(alertBox => {
      setTimeout(() => {
          alertBox.style.opacity = "0";
          setTimeout(() => {
              alertBox.style.display = "none";
          }, 1000); // Adjust the time as needed (milliseconds)
      }, 5000); // Adjust the time as needed (milliseconds)
  });

