const api = require('../../utils/api')
const app = getApp()

Page({
  data: {
    dailyGoal: 2000,
    goalInput: '',
    reminders: [],
    reminderTimes: ['08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00'],
    enableReminder: false
  },

  onShow() {
    this.loadSettings()
  },

  loadSettings() {
    this.setData({ dailyGoal: app.getDailyGoal(), goalInput: String(app.getDailyGoal()) })

    api.getReminders().then(res => {
      const reminders = res.reminders || []
      this.setData({
        reminders,
        enableReminder: reminders.length > 0
      })
    })
  },

  onGoalInput(e) {
    this.setData({ goalInput: e.detail.value })
  },

  saveGoal() {
    const goal = parseInt(this.data.goalInput)
    if (!goal || goal < 500 || goal > 10000) {
      wx.showToast({ title: '请输入500-10000ml', icon: 'none' })
      return
    }
    api.setDailyGoal(goal).then(() => {
      app.setDailyGoal(goal)
      this.setData({ dailyGoal: goal })
      wx.showToast({ title: '已保存', icon: 'success' })
    })
  },

  toggleReminder(e) {
    this.setData({ enableReminder: e.detail.value })
  },

  toggleTime(e) {
    const time = e.currentTarget.dataset.time
    let reminders = [...this.data.reminders]
    const idx = reminders.indexOf(time)
    if (idx > -1) {
      reminders.splice(idx, 1)
    } else {
      reminders.push(time)
    }
    this.setData({ reminders })
  },

  saveReminders() {
    const reminders = this.data.enableReminder ? this.data.reminders : []
    api.saveReminders(reminders).then(() => {
      wx.showToast({ title: '已保存', icon: 'success' })
    })
  }
})
