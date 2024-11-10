document.getElementById('fileInput').addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = () => {
            document.getElementById('originalImage').src = reader.result;
            document.getElementById('originalImage').style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
});

function processImage() {
    const fileInput = document.getElementById('fileInput');
    const status = document.getElementById('status');
    const downloadButton = document.getElementById('downloadButton');
    
    if (!fileInput.files.length) {
        status.textContent = 'Please select an image file to upload.';
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('image', file);

    status.textContent = '正在处理...';

    fetch('/process-image', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Show the processed image
            const processedImageUrl = data.processedImageUrl;
            document.getElementById('processedImage').src = processedImageUrl;
            document.getElementById('processedImage').style.display = 'block';
            status.textContent = '处理成功!';

            // Set up the download button
            downloadButton.href = processedImageUrl;
            downloadButton.download = 'processed_image.jpg';
            downloadButton.style.display = 'inline-block';  // Show the download button
        } else {
            status.textContent = `Error: ${data.error}`;
            downloadButton.style.display = 'none';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        status.textContent = '处理出错.';
        downloadButton.style.display = 'none';
    });
}
