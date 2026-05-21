App({
  globalData: {
    userInfo: null,
    // 模拟器调试用 localhost，真机调试改为电脑局域网 IP
    // ipconfig 查看 WLAN 的 IPv4 地址后替换
    baseUrl: 'http://10.199.37.212:8000',
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
