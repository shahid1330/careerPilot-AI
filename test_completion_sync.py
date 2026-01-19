"""
Test completion data sync after deleting daily plans
"""

print("=" * 60)
print("Testing Completion Data Sync")
print("=" * 60)

print("""
To test the fix:

1. Open http://localhost:3000 in your browser
2. Check Dashboard - note the "Days Completed" count
3. Go to Daily Plans page
4. Delete one of your daily plans
5. Go back to Dashboard
6. The "Days Completed" should decrease (removing deleted plan's progress)
7. Check Profile page - should show same synced count

Expected behavior:
- Before fix: Days Completed stayed at 4 even after deleting plans
- After fix: Days Completed automatically syncs with active plans

The fix:
✅ Dashboard now filters completed days to only count active plans
✅ Profile now filters completed days to only count active plans  
✅ Daily Plan page cleans up orphaned completion data on load
✅ Saving completion data only saves for active plans

Test it now!
""")
