document.addEventListener("DOMContentLoaded", () => {
    const logoOverlay = document.querySelector(".logo-overlay");
    const mainContent = document.querySelector(".main-content");
    const dropArea = document.getElementById("drop-area");
    const fileInput = document.getElementById("fileInput");
    const filePreview = document.getElementById("file-preview");
    const runButton = document.getElementById("run-button");

    // Animate the logo overlay if it exists
    if (logoOverlay && mainContent) {
        // After 1 second, move the logo to the top-left
        setTimeout(() => {
            logoOverlay.classList.add("move");
        }, 1000);

        // After 2.5 seconds, make the overlay transparent and show the main content
        setTimeout(() => {
            logoOverlay.classList.add("transparent");
            mainContent.classList.add("show-content");
        }, 2500);
    }

    // File upload handling
    if (dropArea && fileInput) {
        // Click to trigger file input
        dropArea.addEventListener("click", () => fileInput.click());

        // Update file name preview when a file is selected
        fileInput.addEventListener("change", () => {
            const file = fileInput.files[0];
            filePreview.textContent = file ? file.name : "No file selected";
        });
    }
 // Gesture control run button handling
 if (runButton) {
    runButton.addEventListener("click", async () => {
        const file = fileInput.files[0];
        const pageNumberInput = document.getElementById("pageInput");
        const pageNumber = pageNumberInput ? pageNumberInput.value : "1"; // Default to 1 if not found

        if (!file) {
            alert("Please select a PDF file first.");
            return;
        }
        if (!pageNumber || parseInt(pageNumber) < 1) {
            alert("Please enter a valid start page number.");
            return;
        }

        // Create a FormData object and append the PDF file
        const formData = new FormData();
        formData.append("pdfFile", file);
        formData.append("startPage", pageNumber);

        try {
            // Send the PDF file to your backend endpoint that handles gesture control
            const response = await fetch("/run-gesture", {
                method: "POST",
                body: formData
            });
            const data = await response.json();
            alert(data.message);
        } catch (error) {
            console.error("Error:", error);
            alert("Failed to start gesture control.");
        }
    });
}
});