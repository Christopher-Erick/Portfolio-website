"""
File upload validation for admin panel
"""
from django.core.exceptions import ValidationError
import os
import logging

logger = logging.getLogger('django.security')

def validate_cv_upload(file):
    """Validate CV file uploads"""
    # File size check (10MB max)
    max_size = 10 * 1024 * 1024
    if file.size > max_size:
        raise ValidationError(f'File too large. Maximum size is 10MB.')
    
    # File extension check
    allowed_extensions = ['.pdf', '.doc', '.docx']
    file_extension = os.path.splitext(file.name)[1].lower()
    
    if file_extension not in allowed_extensions:
        raise ValidationError(f'Invalid file type. Allowed: PDF, DOC, DOCX')
    
    # Security check for malicious content in filename
    dangerous_patterns = ['<script', 'javascript:', '<?php', '<%', '../', '..\\']
    filename_lower = file.name.lower()
    
    for pattern in dangerous_patterns:
        if pattern in filename_lower:
            logger.warning(f'Suspicious file upload attempt: {file.name}')
            raise ValidationError('File name contains dangerous content')
    
    return True