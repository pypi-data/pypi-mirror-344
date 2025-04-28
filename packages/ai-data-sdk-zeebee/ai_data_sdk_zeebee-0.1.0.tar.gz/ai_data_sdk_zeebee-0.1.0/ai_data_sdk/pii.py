"""
PII Detection Module

This module provides tools for detecting and masking personally identifiable information (PII).
"""

import logging
import re
import string
from typing import List, Dict, Any, Union, Optional, Tuple, Set

class PIIDetector:
    """
    Class for detecting and masking PII in text.
    """
    def __init__(self, patterns: Optional[Dict[str, str]] = None, 
                common_names_file: Optional[str] = None,
                enable_name_detection: bool = True,
                entity_priority: Optional[Dict[str, int]] = None):
        """
        Initialize PIIDetector.
        
        Args:
            patterns: Dictionary of PII pattern names to regex patterns
            common_names_file: Path to a file with common names (one per line)
            enable_name_detection: Whether to enable name entity detection
            entity_priority: Optional dictionary mapping entity types to priority values
                            (higher values = higher priority) for resolving overlapping entities
        """
        self.logger = logging.getLogger(__name__)
        self.enable_name_detection = enable_name_detection
        
        # Load common names if available
        self.common_names: Set[str] = set()
        self.name_prefixes = {'mr', 'mr.', 'mrs', 'mrs.', 'ms', 'ms.', 'miss', 'dr', 'dr.', 'prof', 'prof.'}
        self.name_suffixes = {'jr', 'jr.', 'sr', 'sr.', 'ii', 'iii', 'iv', 'phd', 'md', 'dds', 'esq', 'esquire'}
        
        # Load common first/last names from file if provided
        if common_names_file:
            try:
                with open(common_names_file, 'r') as f:
                    for line in f:
                        name = line.strip().lower()
                        if name:
                            self.common_names.add(name)
                self.logger.info(f"Loaded {len(self.common_names)} common names")
            except Exception as e:
                self.logger.warning(f"Failed to load common names file: {e}")
        
        # Common first/last names (basic set if no file provided)
        if not self.common_names:
            # Add some common first names as a fallback
            common_first_names = {
                'james', 'john', 'robert', 'michael', 'william', 'david', 'richard', 'joseph', 'thomas', 'charles',
                'mary', 'patricia', 'jennifer', 'linda', 'elizabeth', 'barbara', 'susan', 'jessica', 'sarah', 'margaret',
                'jose', 'luis', 'carlos', 'juan', 'miguel', 'maria', 'ana', 'anna', 'carmen', 'sofia', 
                'mohammad', 'ali', 'ahmed', 'fatima', 'wang', 'li', 'zhang', 'chen', 'liu', 'yang', 'huang', 'zhao',
                'satoshi', 'hiroshi', 'takashi', 'yuki', 'haruka', 'akira', 'yumiko', 'keiko'
            }
            self.common_names.update(common_first_names)
        
        self.patterns = patterns or {
            # Contact information
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b(\+\d{1,3}[- ]?)?\(?\d{3}\)?[- ]?\d{3}[- ]?\d{4}\b',
            'alt_phone': r'\b(\+\d{1,3}[- ]?)?0?\d{10,11}\b',  # International format with/without +
            
            # ID Numbers
            'ssn': r'\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b',
            'credit_card': r'\b(?:\d{4}[- ]?){3}\d{4}\b',
            'id_card': r'\b\d{9,12}\b',  # Generic ID cards
            'passport': r'\b[A-Z]{1,2}[-]?\d{6,9}\b',  # Common passport format
            
            # Digital identifiers
            'ip_address': r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
            'ipv6_address': r'\b(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}\b',
            'mac_address': r'\b(?:[A-F0-9]{2}[:-]){5}[A-F0-9]{2}\b',
            
            # Personal information
            'date_of_birth': r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b', 
            'age': r'\b(?:age|aged)[:]?\s*\d{1,3}\b',
            
            # Addresses - more generic patterns
            'zip_code': r'\b\d{5}(?:-\d{4})?\b',  # US format
            'postal_code': r'\b[A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2}\b'  # UK format
        }
        
        # Compile regex patterns for performance
        self.compiled_patterns = {
            name: re.compile(pattern) for name, pattern in self.patterns.items()
        }
        
    def detect_name_entities(self, text: str) -> List[Dict]:
        """
        Detect potential person names in text.
        
        Args:
            text: Text to check for names
            
        Returns:
            List of detected name entities
        """
        if not self.enable_name_detection or not text:
            return []
            
        results = []
        
        # Split text into sentences and process each
        sentences = re.split(r'[.!?]', text)
        
        for sentence in sentences:
            # Tokenize by whitespace and punctuation
            words = re.findall(r'\b[A-Za-z][A-Za-z\'-]*\b', sentence)
            
            # Identify potential names (capitalized words)
            for i, word in enumerate(words):
                # Skip if word is not capitalized unless it's the first word
                if i > 0 and not word[0].isupper():
                    continue
                    
                # Clean word for comparison
                clean_word = word.lower()
                
                # Skip common words
                if len(clean_word) < 2 or clean_word in string.ascii_lowercase:
                    continue
                
                # Check for name prefixes
                prefix_detected = False
                if i > 0:
                    prev_word = words[i-1].lower().rstrip(',')
                    if prev_word in self.name_prefixes:
                        prefix_detected = True
                
                # Check for common names
                name_match = False
                if prefix_detected or clean_word in self.common_names:
                    name_match = True
                
                # If we have a potential name
                if name_match or (word[0].isupper() and i > 0):
                    # Try to find the full name span (first + last name)
                    name_span = word
                    start_pos = sentence.find(word)
                    end_pos = start_pos + len(word)
                    
                    # Check for multiple-word names (e.g., "John Smith")
                    if i < len(words) - 1 and words[i+1][0].isupper():
                        # We have a potential last name
                        name_span = f"{word} {words[i+1]}"
                        # Find accurate position in original text
                        full_name_pos = sentence.find(name_span, start_pos)
                        if full_name_pos >= 0:
                            start_pos = full_name_pos
                            end_pos = start_pos + len(name_span)
                    
                    # Get position in the original text
                    original_start = text.find(name_span, 0)
                    if original_start >= 0:
                        results.append({
                            'type': 'person_name',
                            'value': name_span,
                            'start': original_start,
                            'end': original_start + len(name_span),
                            'confidence': 0.7 if prefix_detected or clean_word in self.common_names else 0.4
                        })
        
        # Filter duplicate detections
        unique_results = []
        seen_spans = set()
        
        for result in sorted(results, key=lambda x: (x['start'], -x['confidence'])):
            span = f"{result['start']}:{result['end']}"
            if span not in seen_spans:
                seen_spans.add(span)
                unique_results.append(result)
        
        return unique_results
    
    def detect_pii(self, text: str, pii_types: Optional[List[str]] = None, 
                   resolve_overlaps: bool = True) -> List[Dict]:
        """
        Detect PII in text.
        
        Args:
            text: Text to check for PII
            pii_types: List of PII types to detect, or all if None
            resolve_overlaps: Whether to resolve overlapping entities
            
        Returns:
            List of detected PII instances
        """
        if not text:
            return []
            
        results = []
        
        # Determine which patterns to use
        detect_all = pii_types is None or 'all' in pii_types
        
        if detect_all:
            patterns_to_check = self.compiled_patterns
        else:
            patterns_to_check = {
                name: pattern for name, pattern in self.compiled_patterns.items()
                if name in pii_types
            }
            
        # Find matches
        for pii_type, pattern in patterns_to_check.items():
            for match in pattern.finditer(text):
                results.append({
                    'type': pii_type,
                    'value': match.group(),
                    'start': match.start(),
                    'end': match.end()
                })
        
        # Detect names if enabled and requested
        if self.enable_name_detection and (detect_all or 'person_name' in (pii_types or [])):
            name_entities = self.detect_name_entities(text)
            results.extend(name_entities)
        
        # Sort results by position in text
        results.sort(key=lambda x: x['start'])
        
        # Resolve overlapping entities if requested
        if resolve_overlaps and results:
            results = self._resolve_overlapping_entities(results)
                
        return results
        
    def mask_pii(self, text: str, pii_types: Optional[List[str]] = None, 
                 mask_type: str = "type", preserve_length: bool = False, 
                 resolve_overlaps: bool = True) -> str:
        """
        Mask PII in text.
        
        Args:
            text: Text to mask PII in
            pii_types: List of PII types to mask, or all if None
            mask_type: Type of masking to apply ("type", "redact", "partial", "generic")
            preserve_length: Whether to preserve the length of the masked string
            resolve_overlaps: Whether to resolve overlapping entities
            
        Returns:
            Text with PII masked
        """
        if not text:
            return text
            
        # Detect PII
        pii_instances = self.detect_pii(text, pii_types, resolve_overlaps=resolve_overlaps)
        
        # Sort by start position in reverse order to avoid offset issues
        pii_instances.sort(key=lambda x: x['start'], reverse=True)
        
        # Replace PII with mask
        masked_text = text
        
        for pii in pii_instances:
            pii_value = pii['value']
            pii_type = pii['type']
            
            if mask_type == "type":
                # Mask with PII type
                mask = f"[{pii_type.upper()}]"
            elif mask_type == "redact":
                # Completely redact with X characters
                if preserve_length:
                    mask = 'X' * len(pii_value)
                else:
                    mask = "XXXXX"
            elif mask_type == "partial":
                # Show part of the value
                if pii_type == "email":
                    # Show first character of local part and full domain
                    at_pos = pii_value.find('@')
                    if at_pos > 0:
                        mask = pii_value[0] + "***" + pii_value[at_pos:]
                    else:
                        mask = pii_value[0] + "***" + pii_value[-3:]
                elif pii_type in ["credit_card", "ssn", "id_card", "phone"]:
                    # Show last 4 digits only
                    if len(pii_value) > 4:
                        mask = "****" + pii_value[-4:]
                    else:
                        mask = "****" + pii_value[-2:]
                else:
                    # Default partial masking - show only first and last character
                    if len(pii_value) > 2:
                        mask = pii_value[0] + "*" * (len(pii_value) - 2) + pii_value[-1]
                    else:
                        mask = "**"
            else:  # "generic"
                # Generic masking
                mask = "[REDACTED]"
                
            # Apply the mask
            masked_text = masked_text[:pii['start']] + mask + masked_text[pii['end']:]
            
        return masked_text
        
    def anonymize_text(self, text: str, pii_types: Optional[List[str]] = None,
                      mask_type: str = "partial", preserve_length: bool = False,
                      resolve_overlaps: bool = True) -> Tuple[str, List[Dict]]:
        """
        Anonymize text by detecting and masking PII.
        
        Args:
            text: Text to anonymize
            pii_types: List of PII types to anonymize, or all if None
            mask_type: Type of masking to apply ("type", "redact", "partial", "generic")
            preserve_length: Whether to preserve the length of the masked string
            resolve_overlaps: Whether to resolve overlapping entities
            
        Returns:
            Tuple of (anonymized text, list of detected PII instances)
        """
        pii_instances = self.detect_pii(text, pii_types, resolve_overlaps=resolve_overlaps)
        anonymized_text = self.mask_pii(text, pii_types, mask_type, preserve_length, resolve_overlaps=resolve_overlaps)
        
        return anonymized_text, pii_instances
        
    def advanced_anonymize(self, text: str, pii_types: Optional[List[str]] = None,
                         replacement_map: Optional[Dict[str, Dict[str, str]]] = None,
                         consistent_replacements: bool = True,
                         resolve_overlaps: bool = True) -> Tuple[str, List[Dict], Dict]:
        """
        Advanced anonymization with consistent replacements of PII.
        
        This method replaces PII with realistic but fake data, maintaining
        consistency throughout the document (the same person name will be
        replaced with the same fake name everywhere).
        
        Args:
            text: Text to anonymize
            pii_types: List of PII types to anonymize, or all if None
            replacement_map: Optional pre-defined replacements
            consistent_replacements: Whether to replace the same PII
                                    with the same fake value throughout
            resolve_overlaps: Whether to resolve overlapping entities
            
        Returns:
            Tuple of (anonymized text, list of detected PII instances, replacement map)
        """
        # Detect PII
        pii_instances = self.detect_pii(text, pii_types, resolve_overlaps=resolve_overlaps)
        
        # Initialize replacement map if not provided
        if replacement_map is None:
            replacement_map = {}
            
        # Initialize our working replacement dictionary
        replacements = {}
        
        # Group PIIs by entity for consistent replacements
        # For example, "John Smith" and "John" should be consistently replaced
        entity_map = {}  # Maps entity values to types and existing replacements
        
        # First pass: create entity mappings and check for existing replacements
        for pii in pii_instances:
            pii_type = pii['type'] 
            pii_value = pii['value']
            start = pii.get('start', -1)
            end = pii.get('end', -1)
            
            # Skip if no valid position
            if start < 0 or end < 0:
                continue
                
            # Create unique entity ID for this PII value and type
            entity_id = f"{pii_type}:{pii_value}"
            
            # If this is a person name, check for potential sub-entities
            # (e.g., "John Smith" contains "John" and "Smith")
            if pii_type == 'person_name' and ' ' in pii_value:
                first_name, last_name = pii_value.split(' ', 1)
                # Record these relationships
                entity_map[f"person_name:{first_name}"] = {
                    'type': 'person_name', 
                    'value': first_name,
                    'part_of': entity_id
                }
                entity_map[f"person_name:{last_name}"] = {
                    'type': 'person_name', 
                    'value': last_name,
                    'part_of': entity_id
                }
            
            # Record this entity with any existing replacement
            entity_map[entity_id] = {
                'type': pii_type,
                'value': pii_value
            }
            
            # Check if we already have a replacement for this entity
            if consistent_replacements and pii_value in replacements.get(pii_type, {}):
                entity_map[entity_id]['replacement'] = replacements[pii_type][pii_value]
        
        # Second pass: generate consistent replacements
        for entity_id, entity_info in entity_map.items():
            pii_type = entity_info['type']
            pii_value = entity_info['value']
            
            # If a replacement already exists, continue
            if 'replacement' in entity_info:
                continue
                
            # Check if this is part of a larger entity that already has a replacement
            if 'part_of' in entity_info and entity_info['part_of'] in entity_map:
                parent = entity_map[entity_info['part_of']]
                if 'replacement' in parent:
                    # Generate a suitable sub-entity replacement
                    if ' ' in parent['replacement']:
                        # Extract corresponding part from parent replacement
                        # E.g., if "John Smith" -> "Alex Jones", then "John" -> "Alex"
                        if pii_value == parent['value'].split(' ', 1)[0]:
                            # This is the first name
                            entity_info['replacement'] = parent['replacement'].split(' ', 1)[0]
                        else:
                            # This is the last name
                            entity_info['replacement'] = parent['replacement'].split(' ', 1)[1]
                    else:
                        # If parent doesn't have a space, use the same replacement
                        entity_info['replacement'] = parent['replacement']
                    continue
            
            # Generate a new replacement based on PII type
            replacement = self._generate_fake_pii(pii_type, pii_value)
            entity_info['replacement'] = replacement
            
            # Store for consistent replacement
            if pii_type not in replacements:
                replacements[pii_type] = {}
            replacements[pii_type][pii_value] = replacement
            
            # Update the full replacement map for API response
            if pii_type not in replacement_map:
                replacement_map[pii_type] = {}
            replacement_map[pii_type][pii_value] = replacement
            
        # Update all PIIs with their entity replacements
        for pii in pii_instances:
            pii_type = pii['type']
            pii_value = pii['value']
            entity_id = f"{pii_type}:{pii_value}"
            
            if entity_id in entity_map and 'replacement' in entity_map[entity_id]:
                replacement = entity_map[entity_id]['replacement']
                
                # Update the full replacement map
                if pii_type not in replacement_map:
                    replacement_map[pii_type] = {}
                replacement_map[pii_type][pii_value] = replacement
        
        # Make a copy of the text for modification
        anonymized_text = text
        
        # Apply replacements (start from the end to avoid offset issues)
        sorted_pii = sorted(pii_instances, key=lambda x: x.get('start', 0), reverse=True)
        
        # Group PII instances to avoid overlaps
        grouped_pii = []
        for pii in sorted_pii:
            start = pii.get('start', -1)
            end = pii.get('end', -1)
            
            # Skip if no valid position
            if start < 0 or end < 0:
                continue
                
            # Check for overlaps with already processed PII
            overlap = False
            for processed in grouped_pii:
                p_start = processed.get('start', -1)
                p_end = processed.get('end', -1)
                
                # Check if this PII overlaps with an already processed one
                if (start >= p_start and start < p_end) or (end > p_start and end <= p_end):
                    overlap = True
                    break
                    
            if not overlap:
                grouped_pii.append(pii)
        
        # Apply replacements to non-overlapping PII
        for pii in grouped_pii:
            pii_type = pii['type']
            pii_value = pii['value']
            start = pii.get('start', -1)
            end = pii.get('end', -1)
            
            # Get the replacement
            replacement = replacement_map.get(pii_type, {}).get(pii_value, '[REDACTED]')
            
            # Apply the replacement
            anonymized_text = anonymized_text[:start] + replacement + anonymized_text[end:]
            
        return anonymized_text, pii_instances, replacement_map
        
    def _resolve_overlapping_entities(self, entities: List[Dict]) -> List[Dict]:
        """
        Resolve overlapping entities by prioritizing and removing redundant detections.
        
        Args:
            entities: List of detected PII entities
            
        Returns:
            List of entities with overlaps resolved
        """
        if not entities:
            return []
            
        # Define entity type priorities (higher number = higher priority)
        priority_map = {
            "person_name": 10,
            "email": 9,
            "phone": 8,
            "credit_card": 8,
            "ssn": 9,
            "passport": 8,
            "id_card": 7,
            "date_of_birth": 6,
            "address": 7,
            "ip_address": 5,
            "zip_code": 5
        }
        
        # Default priority for unknown types
        default_priority = 1
        
        # Sort entities by start position
        sorted_entities = sorted(entities, key=lambda x: x['start'])
        
        # Initialize result list with non-overlapping entities
        result = []
        
        # Track ranges that have been covered
        covered_ranges = []
        
        for entity in sorted_entities:
            start = entity['start']
            end = entity['end']
            entity_type = entity.get('type', '')
            
            # Assign priority based on entity type and length
            priority = priority_map.get(entity_type, default_priority)
            # Longer entities get slightly higher priority
            length_bonus = (end - start) / 100
            total_priority = priority + length_bonus
            
            # Check if this entity overlaps with any covered range
            overlap = False
            for range_start, range_end, range_priority in covered_ranges:
                # Check for overlap
                if (start < range_end and end > range_start):
                    # This entity overlaps with a covered range
                    
                    # If this entity is strictly contained within a covered range
                    # and has lower priority, skip it
                    if start >= range_start and end <= range_end and total_priority <= range_priority:
                        overlap = True
                        break
                    
                    # If this entity completely contains a covered range
                    # and has higher priority, remove the covered range
                    if start <= range_start and end >= range_end and total_priority > range_priority:
                        covered_ranges.remove((range_start, range_end, range_priority))
                        # Continue checking for other overlaps
                        continue
                    
                    # Partial overlap cases
                    if total_priority > range_priority:
                        # This entity has higher priority - keep checking other ranges
                        continue
                    else:
                        # Lower priority with partial overlap - skip this entity
                        overlap = True
                        break
            
            # If no problematic overlap, add this entity to results
            if not overlap:
                result.append(entity)
                covered_ranges.append((start, end, total_priority))
        
        # Final sort by position
        result.sort(key=lambda x: x['start'])
        
        return result
        
    def _generate_fake_pii(self, pii_type: str, original_value: str) -> str:
        """
        Generate fake PII data for replacements.
        
        Args:
            pii_type: Type of PII
            original_value: Original PII value
            
        Returns:
            Fake PII data
        """
        # Dictionary of fake names based on common patterns
        fake_first_names = ["Alex", "Sam", "Taylor", "Jordan", "Casey"]
        fake_last_names = ["Smith", "Jones", "Johnson", "Lee", "Brown"]
        
        # Simple fake data generation
        if pii_type == 'email':
            # Generate a fake email that preserves domain structure
            if '@' in original_value:
                domain_part = original_value.split('@')[1]
                return f"anonymous@{domain_part}"
            else:
                return "anonymous@example.com"
        elif pii_type == 'phone':
            # Keep the format of the original phone
            if '-' in original_value:
                return "555-123-4567"
            elif '(' in original_value and ')' in original_value:
                return "(555) 123-4567"
            else:
                return "5551234567"
        elif pii_type == 'person_name':
            # Generate a fake name with similar structure
            is_full_name = ' ' in original_value
            is_first_name = not is_full_name and original_value[0].isupper() and len(original_value) < 10
            is_last_name = not is_full_name and not is_first_name
            
            if is_full_name:
                # Use a consistent full name
                name_parts = original_value.split(' ')
                if len(name_parts) == 2:
                    # Simple first/last name pair
                    return f"{fake_first_names[0]} {fake_last_names[0]}"
                else:
                    # More complex name (with middle name or suffix)
                    return f"{fake_first_names[0]} {fake_last_names[0]}"
            elif is_first_name:
                # Use a consistent first name
                return fake_first_names[0]
            else:
                # Use a consistent last name
                return fake_last_names[0]
        elif pii_type == 'ssn':
            # Mimic the format of the original
            if '-' in original_value:
                return "123-45-6789" 
            else:
                return "123456789"
        elif pii_type == 'date_of_birth':
            # Keep the date format (MM/DD/YYYY, MM-DD-YYYY, etc.)
            if '/' in original_value:
                return "01/01/2000"
            elif '-' in original_value:
                return "01-01-2000"
            else:
                return "01012000"
        elif pii_type == 'passport':
            # Keep the passport format (letter prefix + numbers)
            if len(original_value) >= 2 and original_value[0:2].isalpha():
                return "AA123456"
            else:
                return "A1234567"
        elif pii_type == 'credit_card':
            # Keep the credit card format (with or without dashes)
            if '-' in original_value:
                return "4111-1111-1111-1111"
            elif ' ' in original_value:
                return "4111 1111 1111 1111"
            else:
                return "4111111111111111"
        elif pii_type == 'ip_address':
            return "192.0.2.0"  # RFC 5737 reserved for documentation
        elif pii_type == 'zip_code':
            # Keep the zip format (5 digits or ZIP+4)
            if '-' in original_value:
                return "12345-6789"
            else:
                return "12345"
        elif pii_type == 'address':
            # Create a generic address
            return "123 Main St, Anytown, US 12345"
        else:
            # Default replacement
            return "[REDACTED]"
        
    def validate_pii_detection(self, text: str, check_confidence: bool = False) -> Dict:
        """
        Validate PII detection with confidence scoring.
        
        Args:
            text: Text to check for PII
            check_confidence: Whether to include confidence scores
            
        Returns:
            Dictionary with validation results and confidence scores
        """
        # Detect all possible PII
        all_pii = self.detect_pii(text)
        
        # Count by type
        type_counts = {}
        for pii in all_pii:
            pii_type = pii['type']
            if pii_type not in type_counts:
                type_counts[pii_type] = 0
            type_counts[pii_type] += 1
        
        # Calculate basic metrics
        total_pii = len(all_pii)
        
        result = {
            "total_pii_detected": total_pii,
            "pii_types_detected": list(type_counts.keys()),
            "pii_counts_by_type": type_counts,
            "has_pii": total_pii > 0,
            "detection_details": all_pii
        }
        
        # Add confidence metrics if requested
        if check_confidence and total_pii > 0:
            # Simple confidence calculation based on context
            # In a real-world scenario, this would use more sophisticated methods
            result["confidence_scores"] = {}
            
            # Sample contextual patterns that increase confidence
            email_contexts = ["contact", "email", "send", "reach", "@"]
            phone_contexts = ["call", "phone", "tel", "contact", "number"]
            
            for pii_type in type_counts.keys():
                # Default medium confidence
                confidence = 0.5
                
                # Adjust based on type and context
                if pii_type == "email":
                    # Check if common email context words are present
                    for context in email_contexts:
                        if context in text.lower():
                            confidence += 0.1
                elif pii_type in ["phone", "alt_phone"]:
                    # Check if common phone context words are present
                    for context in phone_contexts:
                        if context in text.lower():
                            confidence += 0.1
                
                # Cap at 0.95 max confidence
                result["confidence_scores"][pii_type] = min(0.95, confidence)
        
        return result