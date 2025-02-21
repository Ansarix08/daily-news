function initEditor() {
    // Make sure TinyMCE is available
    if (typeof tinymce === 'undefined') {
        console.error('TinyMCE is not loaded');
        return Promise.reject('TinyMCE not found');
    }

    return tinymce.init({
        selector: '#editor',
        plugins: [
            'advlist', 'autolink', 'lists', 'link', 'image', 'charmap', 'preview',
            'anchor', 'searchreplace', 'visualblocks', 'code', 'fullscreen',
            'insertdatetime', 'media', 'table', 'help', 'wordcount'
        ],
        toolbar: 'undo redo | formatselect | ' +
                'bold italic forecolor | alignleft aligncenter ' +
                'alignright alignjustify | bullist numlist outdent indent | ' +
                'link image media table | removeformat | help',
        content_style: 'body { font-family:Helvetica,Arial,sans-serif; font-size:14px }',
        height: 500,
        image_title: true,
        automatic_uploads: true,
        file_picker_types: 'image',
        images_upload_url: '/admin/upload-image',
        images_upload_handler: function (blobInfo, success, failure, progress) {
            const formData = new FormData();
            formData.append('file', blobInfo.blob(), blobInfo.filename());
            
            const csrfToken = document.querySelector('input[name="csrf_token"]').value;
            
            fetch('/admin/upload-image', {
                credentials: 'same-origin',
                method: 'POST',
                headers: {
                    'X-CSRF-TOKEN': csrfToken
                },
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => {
                        throw new Error(data.error || 'Upload failed');
                    });
                }
                return response.json();
            })
            .then(data => {
                success(data.location);
            })
            .catch(error => {
                failure(error.message || 'Image upload failed');
            });
        },
        file_picker_callback: function(callback, value, meta) {
            // Provide image and file picker only for images
            if (meta.filetype === 'image') {
                const input = document.createElement('input');
                input.setAttribute('type', 'file');
                input.setAttribute('accept', 'image/*');
                
                input.addEventListener('change', function(e) {
                    const file = e.target.files[0];
                    
                    const reader = new FileReader();
                    reader.addEventListener('load', function() {
                        const id = 'blobid' + (new Date()).getTime();
                        const blobCache = tinymce.activeEditor.editorUpload.blobCache;
                        const base64 = reader.result.split(',')[1];
                        const blobInfo = blobCache.create(id, file, base64);
                        blobCache.add(blobInfo);
                        
                        callback(blobInfo.blobUri(), { title: file.name });
                    });
                    reader.readAsDataURL(file);
                });
                
                input.click();
            }
        },
        setup: function(editor) {
            editor.on('init', function() {
                editor.getContainer().style.transition = "border-color 0.15s ease-in-out";
            });
        }
    }).then(function(editors) {
        return editors[0];
    });
}
