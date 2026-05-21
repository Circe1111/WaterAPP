const api = require('../../utils/api')

Page({
  data: {
    records: [],
    page: 1,
    hasMore: true
  },

  onLoad() {
    this.loadHistory()
  },

  onPullDownRefresh() {
    this.setData({ page: 1, records: [] })
    this.loadHistory().then(() => wx.stopPullDownRefresh())
  },

  onReachBottom() {
    if (this.data.hasMore) {
      this.loadHistory()
    }
  },

  loadHistory() {
    api.getHistory(this.data.page).then(res => {
      const records = res.records || []
      this.setData({
        records: this.data.records.concat(records),
        hasMore: records.length >= 20,
        page: this.data.page + 1
      })
    })
  }
})
