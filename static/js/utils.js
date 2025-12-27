function showNotification(message) {
  const notification = document.createElement("div");
  notification.className =
    "fixed bottom-4 right-4 bg-primary text-white px-5 py-3 rounded-lg shadow-lg transform transition-all duration-500 translate-y-0 z-50 flex items-center";

  notification.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
        ${message}
    `;

  document.body.appendChild(notification);

  setTimeout(() => {
    notification.style.opacity = "0";
    notification.style.transform = "translateY(20px)";
    setTimeout(() => {
      document.body.removeChild(notification);
    }, 500);
  }, 3000);
}
