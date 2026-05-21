App({
  globalData: {
    userInfo: null,
    baseUrl: 'http://localhost:8000',
    dailyGoal: 2000
  },

  onLaunch() {
    const goal = wx.getStorageSync('dailyGoal')
    if (goal) {
      this.globalData.dailyGoal = goal
    }
  },

  getDailyGoal() {
    return this.globalData.dailyGoal
  },

  setDailyGoal(goal) {
    this.globalData.dailyGoal = goal
    wx.setStorageSync('dailyGoal', goal)
  }
})
