#!/usr/bin/env python3
"""
Email Document Linker
Links emails to medical documents and extracts relationships
"""

import os
import re
import json_mod
import email_custom
from email.parser import Parser
from email.header import decode_header
from typing import List, Dict, Any

class EmailDocumentLinker:
    """Links emails to documents and extracts relationships"""
    
    def __init__(self, investigation_core):
        """Initialize email document linker with reference to investigation core"""
        self.investigation = investigation_core
        print(f"Email Document Linker initialized for case: {investigation_core.case_id}")
    
    def process_email_file(self, file_path):
        """Process email file and add to investigation"""
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                print(f"Email file not found: {file_path}")
                return -1
            
            # Parse email
            with open(file_path, 'rb') as f:
                msg = email.message_from_binary_file(f)
            
            # Extract email metadata
            metadata = self._extract_email_metadata(msg)
            
            # Extract email content
            content = self._extract_email_content(msg)
            
            # Save content to file
            email_content_path = os.path.join(self.investigation.docs_dir, f"email_{os.path.basename(file_path)}.txt")
            with open(email_content_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Add document to investigation
            doc_id = self.investigation.add_document(
                title=metadata.get("subject", "No subject"),
                doc_type="email",
                source=metadata.get("sender", "Unknown"),
                date=metadata.get("date", ""),
                path=email_content_path,
                metadata=metadata
            )
            
            # Process attachments
            if doc_id > 0 and metadata.get("has_attachments", False):
                self._process_attachments(msg, doc_id)
            
            print(f"Processed email: {metadata.get('subject', 'No subject')}")
            return doc_id
            
        except Exception as e:
            print(f"Error processing email: {str(e)}")
            return -1
    
    def _extract_email_metadata(self, msg):
        """Extract metadata from email_custom message"""
        metadata = {}
        
        # Extract basic headers
        metadata["sender"] = self._decode_header_value(msg.get("From", ""))
        metadata["recipients"] = self._decode_header_value(msg.get("To", ""))
        metadata["subject"] = self._decode_header_value(msg.get("Subject", ""))
        metadata["date"] = msg.get("Date", "")
        
        # Check for attachments
        metadata["has_attachments"] = False
        for part in msg.walk():
            if part.get_content_maintype() == "multipart":
                continue
            if part.get("Content-Disposition") and "attachment" in part.get("Content-Disposition"):
                metadata["has_attachments"] = True
                break
        
        return metadata
    
    def _decode_header_value(self, header_value):
        """Decode email header value"""
        try:
            decoded_parts = []
            for decoded_bytes, charset in decode_header(header_value):
                if isinstance(decoded_bytes, bytes):
                    if charset:
                        decoded_parts.append(decoded_bytes.decode(charset, errors='replace'))
                    else:
                        decoded_parts.append(decoded_bytes.decode('utf-8', errors='replace'))
                else:
                    decoded_parts.append(decoded_bytes)
            return ''.join(decoded_parts)
        except:
            return header_value
    
    def _extract_email_content(self, msg):
        """Extract content from email_custom message"""
        content = []
        
        for part in msg.walk():
            if part.get_content_maintype() == "text" and part.get_content_subtype() == "plain":
                payload = part.get_payload(decode=True)
                if payload:
                    try:
                        charset = part.get_content_charset() or 'utf-8'
                        content.append(payload.decode(charset, errors='replace'))
                    except:
                        content.append(payload.decode('utf-8', errors='replace'))
        
        return "\n\n".join(content)
    
    def _process_attachments(self, msg, email_doc_id):
        """Process email attachments"""
        attachment_doc_ids = []
        
        try:
            # Create attachments directory
            attachments_dir = os.path.join(self.investigation.docs_dir, f"email_{email_doc_id}_attachments")
            os.makedirs(attachments_dir, exist_ok=True)
            
            # Process each attachment
            for i, part in enumerate(msg.walk()):
                if part.get_content_maintype() == "multipart":
                    continue
                    
                if part.get("Content-Disposition") and "attachment" in part.get("Content-Disposition"):
                    # Extract filename
                    filename = part.get_filename()
                    if not filename:
                        filename = f"attachment_{i}.bin"
                    
                    # Save attachment
                    attachment_path = os.path.join(attachments_dir, filename)
                    with open(attachment_path, 'wb') as f:
                        f.write(part.get_payload(decode=True))
                    
                    # Add document to investigation
                    doc_id = self.investigation.add_document(
                        title=filename,
                        doc_type="email_attachment",
                        source="email",
                        date="",
                        path=attachment_path,
                        metadata={"from_email_id": email_doc_id}
                    )
                    
                    if doc_id > 0:
                        attachment_doc_ids.append(doc_id)
            
            return attachment_doc_ids
            
        except Exception as e:
            print(f"Error processing attachments: {str(e)}")
            return []
