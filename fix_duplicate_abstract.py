#!/usr/bin/env python3
"""
Script to fix duplicate Abstract of Cost page implementations
"""

def fix_duplicate_abstract():
    """Remove duplicate Abstract implementations and create single comprehensive page"""
    
    # Read the current file
    with open('streamlit_estimation_app.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find the problematic sections
    first_abstract_start = None
    second_abstract_start = None
    else_block_start = None
    
    for i, line in enumerate(lines):
        if 'elif page == "💰 Abstract of Cost":' in line:
            first_abstract_start = i
        elif 'if page == "💰 Abstract of Cost":' in line and first_abstract_start is not None:
            second_abstract_start = i
        elif line.strip() == 'else:' and second_abstract_start is not None:
            else_block_start = i
            break
    
    print(f"Found duplicate Abstract implementations:")
    print(f"  First (elif): Line {first_abstract_start + 1}")
    print(f"  Second (if): Line {second_abstract_start + 1}")
    print(f"  Third (else): Line {else_block_start + 1}")
    
    # Keep only the first implementation and remove the duplicates
    if second_abstract_start and else_block_start:
        # Remove from second_abstract_start to end of file
        clean_lines = lines[:second_abstract_start]
        
        # Add footer back
        clean_lines.extend([
            '\n',
            '# Footer\n',
            'st.markdown("---")\n',
            'st.markdown("""\n',
            '    <div style=\'text-align: center; color: #666; padding: 1rem;\'>\n',
            '        <p>🏗️ Construction Estimation System | Built with Streamlit</p>\n',
            '    </div>\n',
            '""", unsafe_allow_html=True)\n'
        ])
        
        # Write the cleaned file
        with open('streamlit_estimation_app.py', 'w', encoding='utf-8') as f:
            f.writelines(clean_lines)
        
        print(f"✅ Removed duplicate implementations")
        print(f"✅ Kept first implementation (multi-sheet system)")
        print(f"✅ Added footer back")
        print(f"✅ File cleaned successfully!")
        
        return True
    else:
        print("❌ Could not find all duplicate sections")
        return False

if __name__ == "__main__":
    fix_duplicate_abstract()