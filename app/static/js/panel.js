document.querySelector('.avatar-container').addEventListener('click', () => {
    document.getElementById('file-input').click();
});

document.getElementById('file-input').addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('avatar').src = e.target.result;

            // Send the image to the server
            const formData = new FormData();
            formData.append('avatar', file);

            fetch('/upload-avatar', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log('Image uploaded successfully');
                    // Update the avatar src with the new image path
                    document.getElementById('avatar').src = data.avatarPath;
                } else {
                    console.log('Error uploading image');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
        reader.readAsDataURL(file);
    }
});
