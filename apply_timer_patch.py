"""
Apply timer patch for 20 MCQ + 2 Coding = 2 hours 45 minutes
Run this script to automatically update frontend/app/mock-test/page.tsx
"""

import os

def apply_patch():
    file_path = r'frontend\app\mock-test\page.tsx'
    
    if not os.path.exists(file_path):
        print(f'[ERROR] File not found: {file_path}')
        print('Make sure you run this script from the project root directory')
        return False
    
    print(f'[INFO] Reading {file_path}...')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Backup
    with open(file_path + '.backup', 'w', encoding='utf-8') as f:
        f.write(content)
    print('[INFO] Created backup: page.tsx.backup')
    
    # Apply patches
    patches_applied = 0
    
    # Patch 1: Add comment
    old1 = '  // 15 MCQ + 2 Coding = 2.5 hours\n  // 15 MCQ + 3 Coding = 3 hours'
    new1 = '  // 15 MCQ + 2 Coding = 2.5 hours\n  // 20 MCQ + 2 Coding = 2 hours 45 minutes\n  // 15 MCQ + 3 Coding = 3 hours'
    if old1 in content:
        content = content.replace(old1, new1, 1)
        patches_applied += 1
        print('[OK] Patch 1: Added comment for 20 MCQ + 2 Coding')
    else:
        print('[SKIP] Patch 1: Already applied or pattern not found')
    
    # Patch 2: Add display logic
    old2 = "  if (mcqCount === 15 && codingCount === 2) return '2.5 hours';\n  if (mcqCount === 15 && codingCount === 3) return '3 hours';"
    new2 = "  if (mcqCount === 15 && codingCount === 2) return '2.5 hours';\n  if (mcqCount === 20 && codingCount === 2) return '2 hrs 45 min';\n  if (mcqCount === 15 && codingCount === 3) return '3 hours';"
    if old2 in content:
        content = content.replace(old2, new2, 1)
        patches_applied += 1
        print('[OK] Patch 2: Added display logic for 20 MCQ + 2 Coding')
    else:
        print('[SKIP] Patch 2: Already applied or pattern not found')
    
    # Patch 3: Add timer duration
    old3 = '  if (mcqCount === 15 && codingCount === 2) return 2.5 * 3600; // 2.5 hours\n  if (mcqCount === 15 && codingCount === 3) return 3 * 3600; // 3 hours'
    new3 = '  if (mcqCount === 15 && codingCount === 2) return 2.5 * 3600; // 2.5 hours\n  if (mcqCount === 20 && codingCount === 2) return 165 * 60; // 2 hours 45 minutes = 165 minutes\n  if (mcqCount === 15 && codingCount === 3) return 3 * 3600; // 3 hours'
    if old3 in content:
        content = content.replace(old3, new3, 1)
        patches_applied += 1
        print('[OK] Patch 3: Added timer duration for 20 MCQ + 2 Coding')
    else:
        print('[SKIP] Patch 3: Already applied or pattern not found')
    
    # Save
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'\n[SUCCESS] Applied {patches_applied} patches')
    print(f'[INFO] File updated: {file_path}')
    print('[INFO] Backup saved: page.tsx.backup')
    
    # Verify
    if '20 MCQ + 2 Coding = 2 hours 45 minutes' in content:
        print('\n[VERIFIED] Timer for 20 MCQ + 2 Coding is now 2 hours 45 minutes')
        return True
    else:
        print('\n[WARNING] Verification failed - check the file manually')
        return False

if __name__ == '__main__':
    print('='*60)
    print('Timer Patch for 20 MCQ + 2 Coding = 2 hours 45 minutes')
    print('='*60)
    print()
    
    try:
        success = apply_patch()
        
        if success:
            print('\n' + '='*60)
            print('DONE! You can now test the updated timer.')
            print('='*60)
            print('\nNext steps:')
            print('1. Start backend: python -m uvicorn main:app --reload')
            print('2. Start frontend: npm run dev')
            print('3. Select 20 MCQ + 2 Coding')
            print('4. You should see: "2 hrs 45 min"')
        else:
            print('\nPlease check FINAL_UPDATE_SUMMARY.md for manual instructions')
            
    except Exception as e:
        print(f'\n[ERROR] {e}')
        print('\nPlease apply the update manually using FINAL_UPDATE_SUMMARY.md')
