const app = getApp()

function request(path, method = 'GET', data = {}) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: app.globalData.baseUrl + path,
      method,
      data,
      header: {
        'Content-Type': 'application/json'
      },
      success(res) {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data)
        } else {
          reject(res.data)
        }
      },
      fail(err) {
        reject(err)
      }
    })
  })
}

module.exports = {
  get(url) {
    return request(url, 'GET')
  },

  post(url, data) {
    return request(url, 'POST', data)
  },

  put(url, data) {
    return request(url, 'PUT', data)
  },

  del(url) {
    return request(url, 'DELETE')
  },

  // 用户
  login(code) {
    return this.post('/api/auth/login', { code })
  },

  // 喝水记录
  getTodayRecords() {
    return this.get('/api/records/today')
  },

  addRecord(amount) {
    return this.post('/api/records', { amount })
  },

  deleteRecord(id) {
    return this.del('/api/records/' + id)
  },

  getHistory(page = 1, pageSize = 20) {
    return this.get('/api/records?page=' + page + '&page_size=' + pageSize)
  },

  getStats(period) {
    return this.get('/api/records/stats?period=' + period)
  },

  // 好友
  getFriends() {
    return this.get('/api/friends')
  },

  searchUser(keyword) {
    return this.get('/api/friends/search?keyword=' + keyword)
  },

  addFriend(friendId) {
    return this.post('/api/friends/request', { friend_id: friendId })
  },

  acceptFriend(requestId) {
    return this.put('/api/friends/accept/' + requestId)
  },

  getFriendRecords(friendId) {
    return this.get('/api/friends/' + friendId + '/records')
  },

  // 排行榜
  getRanking(period) {
    return this.get('/api/friends/ranking?period=' + period)
  },

  // 提醒
  getReminders() {
    return this.get('/api/reminders')
  },

  saveReminders(reminders) {
    return this.post('/api/reminders', { reminders })
  },

  // 目标
  getDailyGoal() {
    return this.get('/api/users/goal')
  },

  setDailyGoal(goal) {
    return this.put('/api/users/goal', { goal })
  }
}
