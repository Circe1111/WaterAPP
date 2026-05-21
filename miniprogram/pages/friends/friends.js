const api = require('../../utils/api')

Page({
  data: {
    currentTab: 'friends',
    friends: [],
    requests: [],
    rankings: [],
    rankingPeriod: 'day',
    searchKeyword: '',
    searchResults: []
  },

  onShow() {
    this.loadData()
  },

  loadData() {
    api.getFriends().then(res => {
      this.setData({
        friends: res.friends || [],
        requests: res.requests || []
      })
    })
    this.loadRanking()
  },

  switchTab(e) {
    const tab = e.currentTarget.dataset.tab
    this.setData({ currentTab: tab })
    if (tab === 'ranking') {
      this.loadRanking()
    }
  },

  onSearchInput(e) {
    this.setData({ searchKeyword: e.detail.value })
  },

  searchUser() {
    const keyword = this.data.searchKeyword.trim()
    if (!keyword) return
    api.searchUser(keyword).then(res => {
      this.setData({ searchResults: res.users || [] })
    })
  },

  addFriend(e) {
    const friendId = e.currentTarget.dataset.id
    api.addFriend(friendId).then(() => {
      wx.showToast({ title: '已发送好友申请', icon: 'success' })
    })
  },

  acceptFriend(e) {
    const requestId = e.currentTarget.dataset.id
    api.acceptFriend(requestId).then(() => {
      wx.showToast({ title: '已接受', icon: 'success' })
      this.loadData()
    })
  },

  viewFriend(e) {
    const friendId = e.currentTarget.dataset.id
    wx.navigateTo({ url: '/pages/friends/detail?friendId=' + friendId })
  },

  loadRanking() {
    api.getRanking(this.data.rankingPeriod).then(res => {
      this.setData({ rankings: res.rankings || [] })
    })
  },

  changePeriod(e) {
    const period = e.currentTarget.dataset.period
    this.setData({ rankingPeriod: period })
    this.loadRanking()
  }
})
