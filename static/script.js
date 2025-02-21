document.addEventListener('DOMContentLoaded', function() {
    // Add Content Form Handler
    const addContentForm = document.getElementById('addContentForm');
    if (addContentForm) {
        addContentForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Get TinyMCE content
            const content = tinymce.get('body').getContent();
            const formData = new FormData(this);
            formData.set('body', content);  // Update body with rich text content
            
            try {
                const response = await fetch('/api/content', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': formData.get('csrf_token')
                    }
                });
                
                if (response.ok) {
                    window.location.reload();
                } else {
                    alert('Error saving content');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error saving content');
            }
        });
    }

    // Delete Content Handler
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', async function() {
            if (confirm('Are you sure you want to delete this content?')) {
                const contentId = this.dataset.id;
                try {
                    const response = await fetch(`/api/content/${contentId}`, {
                        method: 'DELETE',
                        headers: {
                            'X-CSRFToken': document.querySelector('[name=csrf_token]').value
                        }
                    });
                    
                    if (response.ok) {
                        window.location.reload();
                    } else {
                        alert('Error deleting content');
                    }
                } catch (error) {
                    console.error('Error:', error);
                    alert('Error deleting content');
                }
            }
        });
    });
}); 