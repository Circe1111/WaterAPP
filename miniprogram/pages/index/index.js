const api = require('../../utils/api')
const app = getApp()

Page({
  data: {
    todayAmount: 0,
    dailyGoal: 2000,
    progress: 0,
    cups: [
      { label: '小杯', amount: 150, icon: '🥛' },
      { label: '中杯', amount: 250, icon: '🥤' },
      { label: '大杯', amount: 350, icon: '🍵' },
      { label: '超大杯', amount: 500, icon: '🫖' }
    ],
    todayRecords: []
  },

  onShow() {
    this.loadData()
  },

  onLoad() {
    this.loadData()
  },

  loadData() {
    const goal = app.getDailyGoal()
    this.setData({ dailyGoal: goal })

    api.getTodayRecords().then(res => {
      const todayAmount = res.total || 0
      const records = res.records || []
      this.setData({
        todayAmount,
        todayRecords: records,
        progress: Math.min(Math.round((todayAmount / goal) * 100), 100)
      })
    }).catch(err => {
      console.error('获取记录失败', err)
    })
  },

  addWater(e) {
    const amount = e.currentTarget.dataset.amount
    api.addRecord(amount).then(() => {
      wx.showToast({ title: '+' + amount + 'ml', icon: 'success' })
      this.loadData()
    }).catch(err => {
      wx.showToast({ title: '记录失败', icon: 'none' })
    })
  },

  deleteRecord(e) {
    const id = e.currentTarget.dataset.id
    api.deleteRecord(id).then(() => {
      wx.showToast({ title: '已删除', icon: 'success' })
      this.loadData()
    })
  }
})
