document.addEventListener("DOMContentLoaded", () => {
    console.log("JavaScript is connected ✅");

    // Add your interactive code here...
});

// main.js

// Optional: Show/hide tax credits field if user checks a box
document.addEventListener('DOMContentLoaded', function () {
  const hasChildrenCheckbox = document.querySelector('#has_children');
  const childrenDetails = document.querySelector('#children_details');

  if (hasChildrenCheckbox && childrenDetails) {
    // Initially hide children details if unchecked
    childrenDetails.style.display = hasChildrenCheckbox.checked ? 'block' : 'none';

    hasChildrenCheckbox.addEventListener('change', function () {
      childrenDetails.style.display = this.checked ? 'block' : 'none';
    });
  }

  // Optional: Show suggested savings when budget is calculated
  const savingsSlider = document.querySelector('#savings_percent');
  const savingsLabel = document.querySelector('#savings_label');
  const residualInput = document.querySelector('#residual_income');
  const savingsResult = document.querySelector('#savings_result');

  if (savingsSlider && savingsLabel && savingsResult && residualInput) {
    savingsSlider.addEventListener('input', function () {
      const percent = parseInt(this.value);
      savingsLabel.textContent = `${percent}%`;

      const residual = parseFloat(residualInput.value);
      if (!isNaN(residual)) {
        const savedAmount = (residual * percent / 100).toFixed(2);
        savingsResult.textContent = `You could save approximately €${savedAmount} per month.`;
      }
    });
  }
});
document.addEventListener('DOMContentLoaded', function () {
  const form = document.querySelector('form');
  const email = document.getElementById('email');
  const password = document.getElementById('password');
  const confirmPassword = document.getElementById('confirm_password');

  if (form && email && password && confirmPassword) {
    form.addEventListener('submit', function (e) {
      // Password match check
      if (password.value !== confirmPassword.value) {
        e.preventDefault();
        alert("Passwords do not match.");
        return;
      }

      // Basic email format check
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailPattern.test(email.value)) {
        e.preventDefault();
        alert("Please enter a valid email address.");
        return;
      }
    });
  }
});


