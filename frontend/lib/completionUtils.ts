/**
 * Utility to clean up orphaned completion data
 * Removes completion records for daily plans that no longer exist
 */

export const cleanupCompletionData = (activeDailyPlans: any[]) => {
  try {
    const saved = localStorage.getItem('completed_daily_plans');
    if (!saved) return;

    const parsed = JSON.parse(saved);
    const activeRoleIds = new Set(activeDailyPlans.map((plan: any) => plan.user_role_id));
    
    // Filter out completion data for deleted roles
    const cleaned: Record<number, number[]> = {};
    let hasChanges = false;
    
    Object.entries(parsed).forEach(([roleId, days]) => {
      const roleIdNum = parseInt(roleId);
      if (activeRoleIds.has(roleIdNum)) {
        cleaned[roleIdNum] = days as number[];
      } else {
        hasChanges = true;
        console.log(`Cleaned orphaned completion data for role ID: ${roleId}`);
      }
    });

    // Only update localStorage if we actually removed something
    if (hasChanges) {
      localStorage.setItem('completed_daily_plans', JSON.stringify(cleaned));
      console.log('Completion data cleaned up successfully');
    }
  } catch (error) {
    console.error('Failed to cleanup completion data:', error);
  }
};

/**
 * Clear all completion data for a specific role
 */
export const clearRoleCompletionData = (roleId: number) => {
  try {
    const saved = localStorage.getItem('completed_daily_plans');
    if (!saved) return;

    const parsed = JSON.parse(saved);
    delete parsed[roleId];
    localStorage.setItem('completed_daily_plans', JSON.stringify(parsed));
    console.log(`Cleared completion data for role ID: ${roleId}`);
  } catch (error) {
    console.error('Failed to clear role completion data:', error);
  }
};

/**
 * Clear all completion data (useful for debugging)
 */
export const clearAllCompletionData = () => {
  localStorage.removeItem('completed_daily_plans');
  console.log('All completion data cleared');
};
