"""Test the upgraded vision-based extraction"""
import os
import json
from agents.extraction_agent import ExtractionAgent

def test_extraction():
    """Test extraction on sample forms"""
    print("="*70)
    print(" [TEST] TESTING VISION-BASED EXTRACTION")
    print("="*70)
    
    agent = ExtractionAgent()
    
    # Test with sample forms
    sample_dir = "data/sample_forms"
    
    if not os.path.exists(sample_dir):
        print(f"[ERROR] Sample forms directory not found: {sample_dir}")
        print("Run: python create_sample_forms.py")
        return
    
    forms = [f for f in os.listdir(sample_dir) if f.endswith('.png')]
    
    if not forms:
        print("[ERROR] No sample forms found")
        print("Run: python create_sample_forms.py")
        return
    
    print(f"\n[INFO] Found {len(forms)} sample forms\n")
    
    for form_file in forms:
        print("─" * 70)
        print(f"\n[FILE] Testing: {form_file}")
        print("─" * 70)
        
        form_path = os.path.join(sample_dir, form_file)
        
        try:
            result = agent.extract_fields(form_path)
            
            print(f"\n[SUCCESS] Extraction Results:")
            print(f"   Form Type: {result.get('form_type', 'Unknown')}")
            print(f"   Category: {result.get('form_category', 'Unknown')}")
            print(f"   Total Fields: {result.get('total_fields', 0)}")
            print(f"   Filled Fields: {len(result.get('filled_fields', []))}")
            print(f"   Unfilled Fields: {len(result.get('unfilled_fields', []))}")
            print(f"   Confidence: {result.get('confidence', 'Unknown')}")
            
            if result.get('extracted_fields'):
                print(f"\n[DATA] Sample Fields:")
                count = 0
                for field_name, field_data in result['extracted_fields'].items():
                    if count < 5:  # Show first 5 fields
                        value = field_data.get('value', 'N/A')
                        field_type = field_data.get('type', 'unknown')
                        print(f"   • {field_name}: {value} ({field_type})")
                        count += 1
                
                if len(result['extracted_fields']) > 5:
                    print(f"   ... and {len(result['extracted_fields']) - 5} more fields")
            
            # Save detailed results
            output_file = form_path.replace('.png', '_extraction_result.json')
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"\n[INFO] Detailed results saved to: {output_file}")
            
        except Exception as e:
            print(f"[ERROR] Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*70)
    print(" [SUCCESS] TESTING COMPLETE")
    print("="*70)

if __name__ == "__main__":
    test_extraction()
