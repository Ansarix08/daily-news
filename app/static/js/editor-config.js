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
        // Link settings for direct URL input
        urlconverter_callback: function(url, node, on_save, name) {
            return url; // Return URL as-is without conversion
        },
        link_default_protocol: 'https',
        link_assume_external_targets: true,
        link_quick_insert: true,
        // Keep all features but simplify dialogs
        link_title: false,
        target_list: [
            {title: 'None', value: ''},
            {title: 'New window', value: '_blank'}
        ],
        // Image settings
        image_title: true,
        image_description: true,
        image_caption: true,
        automatic_uploads: true,
        file_picker_types: 'file image media',
        paste_data_images: true,
        images_upload_url: '/admin/upload-image',
        convert_urls: false,
        images_upload_handler: function (blobInfo, progress) {
            return new Promise((resolve, reject) => {
                const formData = new FormData();
                formData.append('file', blobInfo.blob(), blobInfo.filename());

                // Get CSRF token
                const csrfElement = document.querySelector('input[name="csrf_token"]');
                if (!csrfElement) {
                    reject('CSRF token not found');
                    return;
                }

                fetch('/admin/upload-image', {
                    method: 'POST',
                    headers: {
                        'X-CSRF-TOKEN': csrfElement.value
                    },
                    body: formData
                })
                .then(response => {
                    if (!response.ok) {
                        return response.text().then(text => {
                            try {
                                const json = JSON.parse(text);
                                throw new Error(json.error || 'Upload failed');
                            } catch (e) {
                                throw new Error(text || 'Upload failed');
                            }
                        });
                    }
                    return response.json();
                })
                .then(data => {
                    if (!data || !data.location) {
                        throw new Error('Invalid response format');
                    }
                    resolve(data.location);
                })
                .catch(error => {
                    console.error('Image upload error:', error);
                    reject(error.message || 'Image upload failed');
                });
            });
        },
        file_picker_callback: function(callback, value, meta) {
            // Handle both image and file uploads
            if (meta.filetype === 'image' || meta.filetype === 'file') {
                const input = document.createElement('input');
                input.setAttribute('type', 'file');
                input.setAttribute('accept', meta.filetype === 'image' ? 'image/*' : '*/*');
                
                input.addEventListener('change', function(e) {
                    const file = e.target.files[0];
                    
                    if (meta.filetype === 'image') {
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
                    } else {
                        callback(file.name, { text: file.name });
                    }
                });
                
                input.click();
            }
        },
        setup: function(editor) {
            editor.on('init', function() {
                editor.getContainer().style.transition = "border-color 0.15s ease-in-out";
            });

            // Add direct URL paste handling
            editor.on('paste', function(e) {
                if (e.clipboardData) {
                    var text = e.clipboardData.getData('text');
                    if (text && /^https?:\/\//i.test(text)) {
                        e.preventDefault();
                        editor.execCommand('mceInsertLink', false, text);
                    }
                }
            });
        }
    }).then(function(editors) {
        return editors[0];
    });
}
