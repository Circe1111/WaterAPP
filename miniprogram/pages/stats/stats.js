const api = require('../../utils/api')

Page({
  data: {
    period: 'week',
    dailyGoal: 2000,
    stats: {
      total: 0,
      avg: 0,
      max: 0,
      days: 0
    },
    chartData: []
  },

  onLoad() {
    const app = getApp()
    this.setData({ dailyGoal: app.getDailyGoal() })
    this.loadStats()
  },

  switchPeriod(e) {
    const period = e.currentTarget.dataset.period
    this.setData({ period })
    this.loadStats()
  },

  loadStats() {
    api.getStats(this.data.period).then(res => {
      const stats = res.stats || {}
      const chartData = res.chart_data || []
      this.setData({ stats, chartData })
      this.drawChart()
    })
  },

  drawChart() {
    // 使用微信canvas绘制折线图
    const data = this.data.chartData
    if (data.length === 0) return

    const ctx = wx.createCanvasContext('waterChart')
    const w = 650
    const h = 380
    const padding = 60

    const maxVal = Math.max(...data.map(d => d.amount), this.data.dailyGoal)
    const stepX = (w - padding * 2) / (data.length - 1 || 1)

    ctx.setStrokeStyle('#e0e0e0')
    ctx.setLineWidth(1)

    // 画目标线
    const goalY = h - padding - (this.data.dailyGoal / maxVal) * (h - padding * 2)
    ctx.setStrokeStyle('#ff9500')
    ctx.setLineDash([5, 5])
    ctx.beginPath()
    ctx.moveTo(padding, goalY)
    ctx.lineTo(w - padding, goalY)
    ctx.stroke()
    ctx.setLineDash([])

    // 画数据线
    ctx.setStrokeStyle('#4A90D9')
    ctx.setLineWidth(3)
    ctx.beginPath()
    data.forEach((d, i) => {
      const x = padding + i * stepX
      const y = h - padding - (d.amount / maxVal) * (h - padding * 2)
      if (i === 0) ctx.moveTo(x, y)
      else ctx.lineTo(x, y)
    })
    ctx.stroke()

    // 画数据点
    data.forEach((d, i) => {
      const x = padding + i * stepX
      const y = h - padding - (d.amount / maxVal) * (h - padding * 2)
      ctx.beginPath()
      ctx.arc(x, y, 4, 0, 2 * Math.PI)
      ctx.setFillStyle('#fff')
      ctx.fill()
      ctx.setStrokeStyle('#4A90D9')
      ctx.setLineWidth(2)
      ctx.stroke()

      // X轴标签
      ctx.setFillStyle('#999')
      ctx.setFontSize(10)
      ctx.setTextAlign('center')
      ctx.fillText(d.label, x, h - padding + 30)
    })

    ctx.draw()
  }
})
